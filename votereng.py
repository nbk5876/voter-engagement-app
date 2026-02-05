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
from sqlalchemy import func
from flask_dance.contrib.google import make_google_blueprint, google
import os
import secrets
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
print(f"DEBUG: MAILGUN_DOMAIN = {os.getenv('MAILGUN_DOMAIN')}")

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


class User(db.Model):
    """Stores authenticated users from Google OAuth."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    invite_code = db.Column(db.String(20), unique=True, nullable=False)
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    invited_by = db.relationship("User", remote_side=[id], backref="invitees")


class Group(db.Model):
    """Stores civic groups created by users."""
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    created_by = db.relationship("User", backref="groups_created")
    members = db.relationship("GroupMember", backref="group", cascade="all, delete-orphan")


class GroupMember(db.Model):
    """Junction table for group membership."""
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(20), default="member")  # 'founder' or 'member'
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint("group_id", "user_id", name="uq_group_user"),)

    user = db.relationship("User", backref="group_memberships")


# Create tables if they don't exist
with app.app_context():
    db.create_all()


def generate_invite_code():
    """Generate a unique, URL-safe invite code (8 characters)."""
    for _ in range(10):
        code = secrets.token_urlsafe(6)  # 6 bytes -> 8 URL-safe chars
        if not User.query.filter_by(invite_code=code).first():
            return code
    raise RuntimeError("Failed to generate unique invite code after 10 attempts")


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
                "from": f"Call5 <noreply@{mailgun_domain}>",
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


def send_recruiter_message(from_user_name, from_user_email, to_recruiter_email, message_text):
    """Send a message from a member to their recruiter via MailGun."""
    try:
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")

        if not mailgun_api_key or not mailgun_domain:
            return {"success": False, "error": "MailGun credentials not configured"}

        email_body = f"""You have a new message from {from_user_name}, a member of your Call5 Democracy network.

━━━━━━━━━━━━━━━
MESSAGE
━━━━━━━━━━━━━━━

{message_text}

━━━━━━━━━━━━━━━

To reply, respond to this email — it will go directly to {from_user_name} at {from_user_email}.

This message was sent via Call5 Democracy.
"""

        response = requests.post(
            f"{mailgun_base_url}/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={
                "from": f"Call5 <noreply@{mailgun_domain}>",
                "to": to_recruiter_email,
                "subject": f"Message from {from_user_name} on Call5 Democracy",
                "text": email_body,
                "h:Reply-To": from_user_email,
            }
        )

        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("id")}
        else:
            return {"success": False, "error": f"MailGun error: {response.status_code}", "details": response.text}

    except Exception as e:
        return {"success": False, "error": str(e)}


def send_invitation_email(sender_name, sender_email, recipient_email, invite_link, personal_message=None):
    """Send an invitation email to join Call5 Democracy."""
    try:
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")

        if not mailgun_api_key or not mailgun_domain:
            return {"success": False, "error": "MailGun credentials not configured"}

        # Build personal message section if provided
        personal_section = ""
        if personal_message and personal_message.strip():
            personal_section = f"""
{personal_message.strip()}

"""

        email_body = f"""Hi,

{sender_name} invited you to join Call5 Democracy - a platform for year-round civic engagement and network organizing.
{personal_section}
Join using {sender_name}'s invite link:
{invite_link}

About Call5 Democracy:
- Connect with your recruiter and grow your civic network
- Ask questions to AI-powered candidate personalities
- Organize into groups for coordinated action
- Track campaign promises and hold leaders accountable

See you there!

━━━━━━━━━━━━━━━
This invitation was sent by {sender_name} ({sender_email})
A copy has been sent to their email address.
"""

        response = requests.post(
            f"{mailgun_base_url}/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={
                "from": f"Call5 <noreply@{mailgun_domain}>",
                "to": recipient_email,
                "cc": sender_email,
                "subject": f"{sender_name} invited you to join Call5 Democracy",
                "text": email_body,
                "h:Reply-To": sender_email,
            }
        )

        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("id")}
        else:
            return {"success": False, "error": f"MailGun error: {response.status_code}", "details": response.text}

    except Exception as e:
        return {"success": False, "error": str(e)}


def send_group_broadcast(group, founder, subject, message_body):
    """Send a broadcast message from a group founder to all group members."""
    mailgun_api_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN")
    mailgun_base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")

    if not mailgun_api_key or not mailgun_domain:
        return {"sent": 0, "failed": 0, "error": "MailGun credentials not configured"}

    # Get members (exclude founder)
    members = [m for m in group.members if m.user_id != founder.id]
    if not members:
        return {"sent": 0, "failed": 0, "error": "No members to send to"}

    render_url = os.getenv("RENDER_EXTERNAL_URL", "https://voter-engagement-app.onrender.com")
    group_url = f"{render_url}/groups/{group.id}"

    sent = 0
    failed = 0
    for m in members:
        email_body = f"""Hi {m.user.name},

{founder.name} sent this message to all members of {group.name}:

━━━━━━━━━━━━━━━

{message_body}

━━━━━━━━━━━━━━━

Sent via Call5 Democracy
View your group: {group_url}
Reply to this email to contact {founder.name} directly.
"""
        try:
            response = requests.post(
                f"{mailgun_base_url}/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"Call5 <noreply@{mailgun_domain}>",
                    "to": m.user.email,
                    "cc": founder.email,
                    "subject": subject,
                    "text": email_body,
                    "h:Reply-To": founder.email,
                }
            )
            if response.status_code == 200:
                sent += 1
            else:
                failed += 1
                print(f"Broadcast to {m.user.email} failed: {response.status_code} {response.text}")
        except Exception as e:
            failed += 1
            print(f"Broadcast to {m.user.email} error: {e}")

    return {"sent": sent, "failed": failed}


# --------------------------------------------------
# Google OAuth Callback
# --------------------------------------------------
@app.route("/google_authorized")
def google_authorized():
    """Handle Google OAuth callback: persist user to DB and store session data."""
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        print(f"Google userinfo request failed: {resp.status_code}")
        return redirect(url_for("index"))

    user_info = resp.json()
    google_id = user_info.get("id")       # Google's unique user ID
    email = user_info.get("email")
    name = user_info.get("name", email)    # Fallback to email if name missing

    if not google_id:
        print("Google userinfo missing 'id' field")
        return redirect(url_for("index"))

    # Look up or create user in database
    user = User.query.filter_by(google_id=google_id).first()

    if user:
        # Existing user: update name/email if changed
        if user.email != email or user.name != name:
            user.email = email
            user.name = name
            db.session.commit()
            print(f"Updated user info: {email}")
        print(f"Existing user logged in: {email} (id={user.id})")
    else:
        # New user: create record with invite code
        invite_code = generate_invite_code()

        # Resolve referral if ?ref= was captured on landing page
        invited_by_user_id = None
        ref_code = session.pop("ref_code", None)
        if ref_code:
            referrer = User.query.filter_by(invite_code=ref_code).first()
            if referrer:
                invited_by_user_id = referrer.id
                print(f"Referral tracked: {email} invited by user {referrer.id} ({referrer.email})")
            else:
                print(f"Referral code '{ref_code}' not found, ignoring")

        user = User(
            google_id=google_id,
            email=email,
            name=name,
            invite_code=invite_code,
            invited_by_user_id=invited_by_user_id,
        )
        db.session.add(user)
        db.session.commit()
        print(f"New user created: {email} (id={user.id}, invite_code={invite_code})")

    # Store in session for use across the app
    session["user_id"] = user.id
    session["user_email"] = email
    session["user_name"] = name

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

    # Capture referral code from ?ref= parameter (survives OAuth redirect)
    ref_code = request.args.get("ref")
    if ref_code:
        session["ref_code"] = ref_code

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
# /dashboard
# --------------------------------------------------
@app.route("/dashboard")
def dashboard():
    """Authenticated-only dashboard showing invite link, recruit stats, and actions."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    invite_link = request.host_url.rstrip("/") + "/?ref=" + user.invite_code
    recruiter_name = user.invited_by.name if user.invited_by else None
    recruit_count = len(user.invitees)

    return render_template("dashboard.html",
        user_name=user.name, user_email=user.email,
        invite_link=invite_link, invite_code=user.invite_code,
        recruiter_name=recruiter_name, recruit_count=recruit_count,
        is_admin=user.is_admin)


# --------------------------------------------------
# /admin
# --------------------------------------------------
@app.route("/admin")
def admin():
    """Admin-only report page showing all users and anonymous submissions."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    # Section 1: All registered users
    all_users = User.query.order_by(User.created_at.desc()).all()
    users_data = []
    for u in all_users:
        users_data.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "invite_code": u.invite_code,
            "recruited_by": u.invited_by.name if u.invited_by else None,
            "recruit_count": len(u.invitees),
            "is_admin": u.is_admin,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else "",
        })

    # Section 2: Anonymous submissions (voter_id IS NULL), grouped
    anon_query = (
        db.session.query(
            VoterSubmission.name,
            VoterSubmission.email,
            VoterSubmission.voter_id,
            func.count().label("submission_count"),
            func.max(VoterSubmission.created_at).label("last_submission"),
        )
        .filter(VoterSubmission.voter_id.is_(None))
        .group_by(VoterSubmission.name, VoterSubmission.email, VoterSubmission.voter_id)
        .order_by(func.max(VoterSubmission.created_at).desc())
        .all()
    )
    anon_data = []
    for row in anon_query:
        anon_data.append({
            "name": row.name,
            "email": row.email,
            "voter_id": row.voter_id,
            "submission_count": row.submission_count,
            "last_submission": row.last_submission.strftime("%Y-%m-%d %H:%M") if row.last_submission else "",
        })

    return render_template("admin.html",
        user_name=user.name, user_email=user.email, is_admin=user.is_admin,
        users=users_data, user_count=len(users_data),
        anon_submissions=anon_data, anon_count=len(anon_data))


# --------------------------------------------------
# /admin/network
# --------------------------------------------------
@app.route("/admin/network")
def admin_network():
    """Admin-only network tree showing recruitment hierarchy."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    # Load all users and group by parent (invited_by_user_id)
    all_users = User.query.all()
    users_by_parent = {}
    for u in all_users:
        parent_id = u.invited_by_user_id
        if parent_id not in users_by_parent:
            users_by_parent[parent_id] = []
        users_by_parent[parent_id].append(u)

    # Sort each group by created_at
    for parent_id in users_by_parent:
        users_by_parent[parent_id].sort(key=lambda u: u.created_at or datetime.min)

    def build_tree(parent_id, level):
        """Recursively build flattened tree with level info."""
        nodes = []
        for u in users_by_parent.get(parent_id, []):
            nodes.append({
                "id": u.id,
                "name": u.name,
                "recruit_count": len(u.invitees),
                "level": level,
            })
            nodes.extend(build_tree(u.id, level + 1))
        return nodes

    # Root nodes have invited_by_user_id = None
    tree_nodes = build_tree(None, 0)

    return render_template("admin_network.html",
        user_name=user.name, user_email=user.email,
        tree_nodes=tree_nodes, user_count=len(tree_nodes))


# --------------------------------------------------
# /share
# --------------------------------------------------
@app.route("/share")
def share():
    """Share page with platform-specific pre-written messages and invite link."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    invite_link = request.host_url.rstrip("/") + "/?ref=" + user.invite_code

    # Get confirmation/error from query params (after redirect from send-email)
    confirmation = request.args.get("confirmation")
    error = request.args.get("error")

    return render_template("share.html",
        user_name=user.name, user_email=user.email,
        invite_link=invite_link,
        confirmation=confirmation, error=error)


# --------------------------------------------------
# /share/send-email
# --------------------------------------------------
@app.route("/share/send-email", methods=["POST"])
def share_send_email():
    """Send an invitation email to a recipient."""
    import re

    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    recipient_email = request.form.get("recipient_email", "").strip().lower()
    personal_message = request.form.get("personal_message", "").strip()

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not recipient_email:
        return redirect(url_for("share", error="Please enter a recipient email address."))
    if not re.match(email_pattern, recipient_email):
        return redirect(url_for("share", error="Please enter a valid email address."))

    # Prevent sending to self
    if recipient_email == user.email.lower():
        return redirect(url_for("share", error="You cannot send an invitation to yourself."))

    # Limit personal message length
    if len(personal_message) > 1000:
        return redirect(url_for("share", error="Personal message is too long (max 1000 characters)."))

    # Build invite link
    invite_link = request.host_url.rstrip("/") + "/?ref=" + user.invite_code

    # Send email
    result = send_invitation_email(
        sender_name=user.name,
        sender_email=user.email,
        recipient_email=recipient_email,
        invite_link=invite_link,
        personal_message=personal_message if personal_message else None,
    )

    if result.get("success"):
        return redirect(url_for("share",
            confirmation=f"Invitation sent to {recipient_email}! A copy has been sent to {user.email}."))
    else:
        print(f"Invitation email failed: {result.get('error')}")
        return redirect(url_for("share", error="Sorry, the invitation could not be sent. Please try again later."))


# --------------------------------------------------
# /message-recruiter
# --------------------------------------------------
@app.route("/message-recruiter", methods=["GET", "POST"])
def message_recruiter():
    """Send a message to the user's recruiter via email."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    if not user.invited_by:
        return redirect(url_for("dashboard"))

    recruiter = user.invited_by
    confirmation = None
    error = None
    message_text = ""

    if request.method == "POST":
        message_text = request.form.get("message", "").strip()
        if not message_text:
            error = "Please enter a message."
        else:
            result = send_recruiter_message(
                from_user_name=user.name,
                from_user_email=user.email,
                to_recruiter_email=recruiter.email,
                message_text=message_text,
            )
            if result.get("success"):
                confirmation = f"Your message has been sent to {recruiter.name}."
                message_text = ""
            else:
                error = "Sorry, your message could not be sent. Please try again later."
                print(f"Recruiter message failed: {result.get('error')}")

    return render_template("message_recruiter.html",
        user_name=user.name, user_email=user.email,
        recruiter_name=recruiter.name,
        confirmation=confirmation, error=error,
        message_text=message_text)


# --------------------------------------------------
# /groups/create
# --------------------------------------------------
@app.route("/groups/create", methods=["GET", "POST"])
def groups_create():
    """Create a new civic group (requires recruit_count > 0)."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    recruit_count = len(user.invitees)
    if recruit_count == 0:
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip() or None

        if not name:
            error = "Please enter a group name."
        elif len(name) > 100:
            error = "Group name must be 100 characters or less."
        else:
            # Create group
            group = Group(
                name=name,
                description=description,
                created_by_user_id=user.id,
            )
            db.session.add(group)
            db.session.flush()  # Get the group ID

            # Add founder as member
            member = GroupMember(
                group_id=group.id,
                user_id=user.id,
                role="founder",
            )
            db.session.add(member)
            db.session.commit()

            return redirect(url_for("group_manage", group_id=group.id))

    return render_template("group_create.html",
        user_name=user.name, user_email=user.email,
        error=error)


# --------------------------------------------------
# /groups
# --------------------------------------------------
@app.route("/groups")
def groups_list():
    """List all groups the user is a member of."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    recruit_count = len(user.invitees)

    # Get all groups the user is a member of
    memberships = GroupMember.query.filter_by(user_id=user.id).all()
    groups_data = []
    for m in memberships:
        groups_data.append({
            "id": m.group.id,
            "name": m.group.name,
            "role": m.role,
            "member_count": len(m.group.members),
            "created_by": m.group.created_by.name,
            "joined_at": m.joined_at.strftime("%Y-%m-%d") if m.joined_at else "",
        })

    return render_template("groups_list.html",
        user_name=user.name, user_email=user.email,
        groups=groups_data, recruit_count=recruit_count)


# --------------------------------------------------
# /groups/<id>
# --------------------------------------------------
@app.route("/groups/<int:group_id>")
def group_manage(group_id):
    """Manage a group: view members, invite recruits."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    group = db.session.get(Group, group_id)
    if not group:
        return redirect(url_for("groups_list"))

    # Check user is a member of this group
    membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        return redirect(url_for("groups_list"))

    # Get members list
    members_data = []
    for m in group.members:
        members_data.append({
            "id": m.user.id,
            "name": m.user.name,
            "email": m.user.email,
            "role": m.role,
            "joined_at": m.joined_at.strftime("%Y-%m-%d") if m.joined_at else "",
        })

    # Get recruits who are NOT yet in this group (for invite dropdown)
    existing_member_ids = {m.user_id for m in group.members}
    invitable_recruits = [r for r in user.invitees if r.id not in existing_member_ids]

    confirmation = request.args.get("invited")
    broadcast_confirmation = request.args.get("broadcast_sent")
    error = request.args.get("error")

    is_founder = group.created_by_user_id == user.id
    member_count = sum(1 for m in group.members if m.user_id != group.created_by_user_id)

    return render_template("group_manage.html",
        user_name=user.name, user_email=user.email,
        group=group, members=members_data,
        invitable_recruits=invitable_recruits,
        confirmation=confirmation,
        broadcast_confirmation=broadcast_confirmation,
        error=error,
        is_founder=is_founder,
        member_count=member_count)


# --------------------------------------------------
# /groups/<id>/invite
# --------------------------------------------------
@app.route("/groups/<int:group_id>/invite", methods=["POST"])
def group_invite(group_id):
    """Add a recruit to a group."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    group = db.session.get(Group, group_id)
    if not group:
        return redirect(url_for("groups_list"))

    # Check user is a member of this group
    membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
    if not membership:
        return redirect(url_for("groups_list"))

    recruit_id = request.form.get("recruit_id", type=int)
    if not recruit_id:
        return redirect(url_for("group_manage", group_id=group_id))

    # Validate the recruit belongs to this user
    recruit = db.session.get(User, recruit_id)
    if not recruit or recruit.invited_by_user_id != user.id:
        return redirect(url_for("group_manage", group_id=group_id))

    # Check recruit not already in group
    existing = GroupMember.query.filter_by(group_id=group_id, user_id=recruit_id).first()
    if existing:
        return redirect(url_for("group_manage", group_id=group_id))

    # Add recruit as member
    member = GroupMember(
        group_id=group_id,
        user_id=recruit_id,
        role="member",
    )
    db.session.add(member)
    db.session.commit()

    return redirect(url_for("group_manage", group_id=group_id, invited=recruit.name))


# --------------------------------------------------
# /groups/<id>/broadcast
# --------------------------------------------------
@app.route("/groups/<int:group_id>/broadcast", methods=["POST"])
def group_broadcast(group_id):
    """Send a broadcast message from the group founder to all members."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("index"))

    group = db.session.get(Group, group_id)
    if not group:
        return redirect(url_for("groups_list"))

    # Only founder can broadcast
    if group.created_by_user_id != user.id:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Only group founders can send broadcast messages."))

    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # Validation
    if not subject:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Subject line is required."))
    if not message:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Message is required."))
    if len(subject) > 200:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Subject must be under 200 characters."))
    if len(message) > 5000:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Message must be under 5000 characters."))

    # Send broadcast
    result = send_group_broadcast(group, user, subject, message)

    if result.get("error"):
        return redirect(url_for("group_manage", group_id=group_id,
            error=result["error"]))

    sent = result["sent"]
    failed = result["failed"]

    if failed == 0:
        return redirect(url_for("group_manage", group_id=group_id,
            broadcast_sent=f"Message sent to {sent} group member{'s' if sent != 1 else ''}! A copy has been sent to your email."))
    elif sent > 0:
        return redirect(url_for("group_manage", group_id=group_id,
            broadcast_sent=f"Message sent to {sent} of {sent + failed} members. Some emails failed."))
    else:
        return redirect(url_for("group_manage", group_id=group_id,
            error="Failed to send message. Please try again."))


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
                    "from": f"Call5 <noreply@{mailgun_domain}>",
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
        print("[OK] OpenAI API key loaded successfully")
    
    if not os.getenv("MAILGUN_API_KEY") or not os.getenv("MAILGUN_DOMAIN"):
        print("WARNING: MailGun credentials not set. Email sending will be disabled.")
    else:
        print("[OK] MailGun credentials loaded successfully")

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
    )