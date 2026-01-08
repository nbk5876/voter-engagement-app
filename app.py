"""
Name: app.py
Simple Flask application for voter engagement response using OpenAI API
"""
from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
# You'll need to set your OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

#---------------------------------
# /respond route
#---------------------------------
@app.route('/respond', methods=['POST'])
def respond_to_voter():
    """
    Handle form submission and call OpenAI API to generate response
    """
    try:
        # Get form data
        name = request.form.get('name', '')
        voter_id = request.form.get('voter_id', '')
        comment = request.form.get('comment', '')
        
        # Validate input
        if not name or not voter_id or not comment:
            return jsonify({'error': 'Please provide name, voter ID, and comment'}), 400
        
        # Create prompt for OpenAI
        prompt = f"""You are responding to a voter engagement comment. Please provide a thoughtful, respectful response. 

It is January 2026 and you are responding for Kshama Sawant who is an Economist and former Member of the Seattle City Council.

Kshama Sawant, the socialist who served a decade on the Seattle City Council, launched a “working-class, antiwar, anti-genocide” campaign Monday to unseat incumbent Democratic U.S. Rep. Adam Smith in the 2026 election. 

At her campaign kick-off in Seattle, Sawant called for a $25 an hour minimum wage, universal health care and a halt in U.S. military aid to Israel for its ongoing offensive against Hamas. Sawant did not seek re-election in 2023 as she established Workers Strike Back, an activist group focused on pro-labor causes and other issues.

The Seattle resident vowed, if elected, to “flip the script on how to use elected office” as she did as a city leader from 2014 to 2024.  

My socialist city council office went to war for working people to defeat the strenuous opposition from both big business and the Democratic Party,” she said in a statement. “Our experience in Seattle shows that we can defeat the rich and their political servants.

Sawant filed as an independent with the Federal Election Commission.

Voter Name: {name}
Voter ID: {voter_id}
Comment: {comment}

Provide a helpful and engaging response that:
1. Acknowledges their comment
2. Addresses any questions or concerns raised
3. Encourages continued civic participation
4. Is respectful and non-partisan
"""
        # Print the prompt sent to ChatGPT
        print(f"\n{'='*60}\nPROMPT SENT TO AI:\n{'='*60}\n{prompt}\n{'='*60}\n")

        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4" for better results
            messages=[
                {"role": "system", "content": "You are a helpful civic engagement assistant. Provide clear, respectful, and non-partisan responses to voter comments and questions. Encourage democratic participation and provide factual information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        

        # Extract the response
        ai_response = response.choices[0].message.content

        # Print the response from ChatGPT
        print(f"\n{'='*60}\nAI RESPONSE:\n{'='*60}\n{ai_response}\n{'='*60}\n")
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'input': {
                'name': name,
                'voter_id': voter_id,
                'comment': comment
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
    else:
        print("✓ OpenAI API key loaded successfully")
    
    # Run the development server
    #app.run(debug=True, host='0.0.0.0', port=5000)

    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", "5000")))
