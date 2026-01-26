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

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
import os
import socket
import requests  # Added for MailGun API
from datetime import datetime, timezone
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

# Secret key for sessions (required for OAuth)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

# Google OAuth configuration
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="google_authorized",
)
app.register_blueprint(google_bp, url_prefix="/login")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# --------------------------------------------------
# Database Model
# --------------------------------------------------
class VoterSubmission(db.Model):
    """Stores voter submissions and AI responses."""
    __tablename__ = "voter_submissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    voter_id = db.Column(db.String(200), nullable=True)  # Email for logged-in, NULL for anonymous
    email = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=True)
    candidate_key = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# Create tables if they don't exist
with app.app_context():
    db.create_all()


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

━━━━━━━━━━━━━━━
YOUR INFORMATION
━━━━━━━━━━━━━━━

Name: {voter_name}
Voter ID: {voter_id}

Your Comment:
{comment}

━━━━━━━━━━━━━━━
AI RESPONSE
━━━━━━━━━━━━━━━

{ai_response}

━━━━━━━━━━━━━━━

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
# Google OAuth Callback
# --------------------------------------------------
@app.route("/google_authorized")
def google_authorized():
    """Handle Google OAuth callback and store user email in session."""
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        session["user_email"] = user_info.get("email")
        session["user_name"] = user_info.get("name")
        print(f"User logged in: {session['user_email']}")

    return redirect(url_for("index"))


# --------------------------------------------------
# /logout
# --------------------------------------------------
@app.route("/logout")
def logout():
    """Clear session and log user out."""
    session.clear()
    return redirect(url_for("index"))


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

    # Get user info from session if logged in
    user_email = session.get("user_email")
    user_name = session.get("user_name")

    return render_template(
        "index.html",
        show_debug=show_debug,
        candidate_key=candidate.key,
        candidate_name=candidate.display_name,
        user_email=user_email,
        user_name=user_name,
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
        # Read form inputs and session
        # ----------------------------
        comment = request.form.get("comment", "").strip()

        # Get user info from session (if logged in via Google)
        user_email = session.get("user_email")
        user_name = session.get("user_name")

        # If logged in, use Google profile; otherwise use form fields
        if user_email:
            name = user_name or user_email
            voter_id = user_email  # Use email as voter_id for logged-in users
        else:
            name = request.form.get("name", "").strip()
            voter_id = None  # Anonymous users have no voter_id

        if not comment:
            return jsonify(
                {"error": "Please provide a comment"}
            ), 400

        if not user_email and not name:
            return jsonify(
                {"error": "Please provide your name"}
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
        # Save to database
        # ----------------------------
        submission = VoterSubmission(
            name=name,
            voter_id=voter_id,  # user_email if logged in, None if anonymous
            email=user_email,  # Only set if logged in
            comment=comment,
            ai_response=ai_response,
            candidate_key=candidate.key,
        )
        db.session.add(submission)
        db.session.commit()
        print(f"Saved submission to database (id={submission.id})")

        # ----------------------------
        # Send email notifications
        # ----------------------------
        email_results = []
        admin_emails = ["jeffjordan5@proton.me", "VoterEngageBox1@proton.me"]

        # 1. ALWAYS send to admin emails (every submission)
        for admin_email in admin_emails:
            result = send_email_via_mailgun(
                to_email=admin_email,
                voter_name=name,
                voter_id=voter_id or "anonymous",
                comment=comment,
                ai_response=ai_response,
                candidate_name=candidate.display_name
            )
            email_results.append({"to": admin_email, "result": result, "type": "admin"})

            print("\n" + "=" * 60)
            print("ADMIN EMAIL SEND RESULT:")
            print("=" * 60)
            print(f"To: {admin_email}")
            print(f"Result: {result}")
            print("=" * 60 + "\n")

        # 2. ADDITIONALLY send to user if logged in
        if user_email:
            result = send_email_via_mailgun(
                to_email=user_email,
                voter_name=name,
                voter_id=voter_id,
                comment=comment,
                ai_response=ai_response,
                candidate_name=candidate.display_name
            )
            email_results.append({"to": user_email, "result": result, "type": "user"})

            print("\n" + "=" * 60)
            print("USER EMAIL SEND RESULT:")
            print("=" * 60)
            print(f"To: {user_email}")
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
                    "logged_in": user_email is not None,
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
# Startup Notification
# --------------------------------------------------
def send_startup_notification():
    """Send an email notification when the server starts."""
    mailgun_api_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN")
    mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")

    if not mailgun_api_key or not mailgun_domain:
        print("Startup notification skipped: MailGun credentials not configured.")
        return

    environment = "Render" if os.getenv("RENDER") else "Local PC"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "unknown"

    # On Render, fetch the commit message from GitHub
    commit_info = ""
    commit_sha = os.getenv("RENDER_GIT_COMMIT")
    if commit_sha:
        try:
            gh_resp = requests.get(
                f"https://api.github.com/repos/nbk5876/voter-engagement-app/commits/{commit_sha}",
                timeout=5,
            )
            if gh_resp.status_code == 200:
                message = gh_resp.json().get("commit", {}).get("message", "")
                commit_info = f"Commit: {commit_sha[:7]}\nMessage: {message}\n"
        except Exception:
            commit_info = f"Commit: {commit_sha[:7]}\n"

    subject = f"Voter Engagement Server Started — {environment}"
    body = (
        f"The Voter Engagement server has started.\n\n"
        f"Environment: {environment}\n"
        f"Host: {hostname}\n"
        f"IP Address: {ip_address}\n"
        f"Timestamp: {timestamp}\n"
        f"{commit_info}"
    )

    recipients = ["jeffjordan5@proton.me", "VoterEngageBox1@proton.me"]
    for to_email in recipients:
        try:
            response = requests.post(
                f"{mailgun_base_url}/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"Voter Engagement <noreply@{mailgun_domain}>",
                    "to": to_email,
                    "subject": subject,
                    "text": body,
                },
            )
            print(f"Startup notification to {to_email}: {response.status_code}")
        except Exception as e:
            print(f"Startup notification to {to_email} failed: {e}")


send_startup_notification()


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