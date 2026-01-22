"""
Name: votereng.py
Simple Flask application for voter engagement response using OpenAI API

PR #2:
- Candidate personality selection via query parameter (?ca=)
- DEV/TST mode support via (?mode=DEV|TST)

PR #3:
- Google authentication (planned)
- Change "Civic Unit" to "Civic Group" (planned)

PR #4:
- MailGun email integration to send AI responses to voters
"""

from flask import Flask, render_template, request, jsonify
import os
import requests  # Added for MailGun API
from openai import OpenAI
from dotenv import load_dotenv

from personality import (
    get_candidate,
    load_candidate_context,
    should_show_debug,
)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------------------------------
# MailGun Email Function
# --------------------------------------------------
def send_email_via_mailgun(to_email, voter_name, voter_id, comment, ai_response, candidate_name):
    """
    Send AI response to voter via MailGun.
    
    Args:
        to_email: Recipient email address
        voter_name: Name of the voter
        voter_id: Voter ID
        comment: Original comment from voter
        ai_response: The AI-generated response text
        candidate_name: Name of the candidate personality
    
    Returns:
        dict: Response from MailGun API or error details
    """
    try:
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")
        
        if not mailgun_api_key or not mailgun_domain:
            return {"success": False, "error": "MailGun credentials not configured"}
        
        # Build email body with voter information and response
        email_body = f"""Hi {voter_name},

Thank you for your comment. Here's a summary of your inquiry and our response:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {voter_name}
Voter ID: {voter_id}

Your Comment:
{comment}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{ai_response}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is an automated response from the Voter Engagement platform.
"""
        
        response = requests.post(
            f"{mailgun_base_url}/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={
                "from": f"Voter Engagement <noreply@{mailgun_domain}>",
                "to": to_email,
                "subject": f"Response from {candidate_name}",
                "text": email_body,
            }
        )
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("id")}
        else:
            return {
                "success": False, 
                "error": f"MailGun error: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}


# --------------------------------------------------
# /
# --------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """
    Render the main form page.

    PR #2:
    - Reads ?ca= and ?mode=
    - Displays selected personality only in DEV/TST mode
    """
    candidate = get_candidate(request.args)
    show_debug = should_show_debug(request.args)

    return render_template(
        "index.html",
        show_debug=show_debug,
        candidate_key=candidate.key,
        candidate_name=candidate.display_name,
    )


# --------------------------------------------------
# /respond
# --------------------------------------------------
@app.route("/respond", methods=["POST"])
def respond_to_voter():
    """
    Handle form submission and call OpenAI API to generate response.

    PR #2:
    - Reads ?ca= and ?mode= from query string
    - Loads candidate context from ./context/<candidate>.txt

    PR #4:
    - Sends AI response via email if email address provided
    """
    try:
        # ----------------------------
        # Read form inputs
        # ----------------------------
        name = request.form.get("name", "").strip()
        voter_id = request.form.get("voter_id", "").strip()
        comment = request.form.get("comment", "").strip()
        email = request.form.get("email", "").strip()  # New: email field

        if not name or not voter_id or not comment:
            return jsonify(
                {"error": "Please provide name, voter ID, and comment"}
            ), 400

        # ----------------------------
        # Candidate personality
        # ----------------------------
        candidate = get_candidate(request.args)
        candidate_context = load_candidate_context(candidate)

        # ----------------------------
        # Build prompt
        # ----------------------------
        prompt = f"""You are responding to a voter engagement comment. Please provide a thoughtful, respectful response.

{candidate_context}

Voter Name: {name}
Voter ID: {voter_id}
Comment: {comment}

Provide a helpful and engaging response that:
1. Acknowledges their comment
2. Addresses any questions or concerns raised
3. Encourages continued civic participation
4. Is respectful and non-partisan
"""

        print("\n" + "=" * 60)
        print("PROMPT SENT TO AI:")
        print("=" * 60)
        print(prompt)
        print("=" * 60 + "\n")

        # ----------------------------
        # OpenAI API call
        # ----------------------------
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful civic engagement assistant. "
                        "Provide clear, respectful, and non-partisan responses "
                        "to voter comments and questions. Encourage democratic "
                        "participation and provide factual information. "
                        "Do not invent endorsements, promises, or campaign actions. "
                        "Do not include a signature, closing line, or placeholder name."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "500")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        )

        ai_response = response.choices[0].message.content or ""

        print("\n" + "=" * 60)
        print("AI RESPONSE:")
        print("=" * 60)
        print(ai_response)
        print("=" * 60 + "\n")

        # ----------------------------
        # Send email (use defaults if not provided)
        # ----------------------------
        default_emails = ["jeffjordan5@proton.me", "VoterEngageBox1@proton.me"]

        if email:
            # Send to provided email only
            target_emails = [email]
        else:
            # Send to both default emails
            target_emails = default_emails

        email_results = []
        for target_email in target_emails:
            result = send_email_via_mailgun(
                to_email=target_email,
                voter_name=name,
                voter_id=voter_id,
                comment=comment,
                ai_response=ai_response,
                candidate_name=candidate.display_name
            )
            email_results.append({"to": target_email, "result": result})

            print("\n" + "=" * 60)
            print("EMAIL SEND RESULT:")
            print("=" * 60)
            print(f"To: {target_email}")
            print(f"Result: {result}")
            print("=" * 60 + "\n")

        return jsonify(
            {
                "success": True,
                "response": ai_response,
                "input": {
                    "name": name,
                    "voter_id": voter_id,
                    "comment": comment,
                    "email": email if email else None,
                },
                "email_results": email_results,
                "meta": {
                    "candidate_key": candidate.key,
                    "candidate_name": candidate.display_name,
                    "mode": request.args.get("mode", ""),
                },
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# /docs/use-cases
# --------------------------------------------------
@app.route("/docs/use-cases", methods=["GET"])
def docs_use_cases():
    """Render the Use Cases document page."""
    return render_template("voter_engage_use_cases_v1.html")


# --------------------------------------------------
# /docs/concepts
# --------------------------------------------------
@app.route("/docs/concepts", methods=["GET"])
def docs_concepts():
    """Render the Call 5 People Concepts document page."""
    return render_template("voter_engage_concepts_v1.html")


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not set!")
    else:
        print("✓ OpenAI API key loaded successfully")
    
    if not os.getenv("MAILGUN_API_KEY") or not os.getenv("MAILGUN_DOMAIN"):
        print("WARNING: MailGun credentials not set. Email sending will be disabled.")
    else:
        print("✓ MailGun credentials loaded successfully")

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
    )