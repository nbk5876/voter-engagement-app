# Tax Data Evaluator - Development Environment

A simple Python web application that collects tax data through an HTML form and uses OpenAI API to provide tax insights.

## Features

✅ Mobile-friendly responsive design  
✅ Flask backend with Python  
✅ OpenAI API integration  
✅ Clean, modern UI  
✅ Real-time form submission  
✅ Error handling  

## Project Structure

```
tax-app/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # HTML form page
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
└── README.md           # This file
```

## Setup Instructions

### 1. Install Python Dependencies

Make sure you have Python 3.8+ installed, then install the required packages:

```bash
cd tax-app
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
cd tax-app
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

1. Get your API key from https://platform.openai.com/api-keys
2. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

3. Edit `.env` and add your actual API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Alternative:** Set the environment variable directly:

```bash
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

### 3. Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 4. Access the Application

Open your browser and go to:
- **Local:** http://localhost:5000
- **Network access:** http://your-local-ip:5000 (for testing on mobile devices on the same network)

## How It Works

1. **User fills out the form** with income and deductions
2. **Form data is submitted** to the Flask backend via AJAX
3. **Flask processes the data** and sends it to OpenAI API
4. **OpenAI analyzes the tax information** and returns insights
5. **Results are displayed** at the bottom of the same page

## API Usage

The app uses OpenAI's Chat Completions API:
- Model: `gpt-4o-mini` (cost-effective) or `gpt-4` (better quality)
- Max tokens: 500
- Temperature: 0.7

## Mobile Optimization

The interface is fully responsive and mobile-friendly:
- Viewport meta tag for proper scaling
- Touch-friendly input fields
- Responsive grid layout
- Works well on screens from 320px to 4K

## Customization Ideas

### Add More Fields

Edit `templates/index.html` to add more form fields:
```html
<div class="form-group">
    <label for="state">State</label>
    <select id="state" name="state">
        <option value="CA">California</option>
        <!-- Add more states -->
    </select>
</div>
```

Then update `app.py` to handle the new field:
```python
state = request.form.get('state', '')
```

### Change the AI Model

In `app.py`, modify the model parameter:
```python
response = client.chat.completions.create(
    model="gpt-4",  # Use GPT-4 for better results
    # ... rest of the code
)
```

### Adjust the Prompt

Modify the prompt in `app.py` to change how the AI analyzes the data:
```python
prompt = f"""Your custom prompt here...

Income: ${income}
Deductions: ${deductions}
"""
```

## Security Notes

⚠️ **Important for Production:**

1. Never commit `.env` file to version control
2. Use HTTPS in production
3. Implement rate limiting
4. Add input validation and sanitization
5. Consider user authentication
6. Monitor API usage and costs
7. Add CORS headers if needed for cross-origin requests

## Troubleshooting

### "OPENAI_API_KEY not set" error
Make sure you've created a `.env` file with your API key or set the environment variable.

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Network access not working
Make sure your firewall allows connections on port 5000, or use `0.0.0.0` as the host.

## Testing on Mobile Devices

To test on your phone/tablet:

1. Make sure your computer and phone are on the same WiFi network
2. Find your computer's local IP address:
   - **Mac/Linux:** `ifconfig | grep inet`
   - **Windows:** `ipconfig`
3. On your phone, navigate to: `http://YOUR-IP:5000`

## Next Steps

- Add database storage for tax calculations
- Implement user accounts and history
- Add PDF export functionality
- Create multiple calculation pages
- Add data visualization charts
- Deploy to a web server (Heroku, AWS, etc.)

## License

This is a development/testing environment. Modify as needed for your use case.

## Support

For questions about:
- **Flask:** https://flask.palletsprojects.com/
- **OpenAI API:** https://platform.openai.com/docs
- **Python:** https://docs.python.org/
