#!/usr/bin/env python3
"""
Simplified tax evaluator using Python's built-in HTTP server
This version doesn't require Flask - just the OpenAI library
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tax Evaluator (Standalone)</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-radius: 12px 12px 0 0;
        }
        .form-container { padding: 30px 20px; }
        .form-group { margin-bottom: 20px; }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input {
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { opacity: 0.9; }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            display: none;
        }
        .loading { display: none; text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Tax Evaluator</h1>
            <p>Standalone Version</p>
        </div>
        <div class="form-container">
            <form id="taxForm">
                <div class="form-group">
                    <label>Annual Income ($)</label>
                    <input type="number" name="income" required>
                </div>
                <div class="form-group">
                    <label>Total Deductions ($)</label>
                    <input type="number" name="deductions" required>
                </div>
                <button type="submit" class="btn">Analyze</button>
            </form>
            <div class="loading" id="loading">Analyzing...</div>
            <div class="result" id="result"></div>
        </div>
    </div>
    <script>
        document.getElementById('taxForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/api/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: new URLSearchParams(formData)
                });
                const data = await response.json();
                document.getElementById('loading').style.display = 'none';
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = data.error ? `<strong>Error:</strong> ${data.error}` : data.response;
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Error: ' + error.message);
            }
        };
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/api/evaluate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            income = params.get('income', [''])[0]
            deductions = params.get('deductions', [''])[0]
            
            try:
                if not client.api_key:
                    raise Exception("OPENAI_API_KEY not set")
                
                prompt = f"Analyze: Income ${income}, Deductions ${deductions}. Provide brief tax insights."
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a tax advisor. Be concise."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                
                result = {
                    'success': True,
                    'response': response.choices[0].message.content
                }
            except Exception as e:
                result = {'error': str(e)}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    print(f"Server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  WARNING: OPENAI_API_KEY not set!")
    server.serve_forever()
