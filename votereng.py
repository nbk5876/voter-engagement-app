"""
Name: votereng.py
Simple Flask application for voter engagement response using OpenAI API

PR #2:
- Candidate personality selection via query parameter (?ca=)
- DEV/TST mode support via (?mode=DEV|TST)
"""

from flask import Flask, render_template, request, jsonify
import os
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
    """
    try:
        # ----------------------------
        # Read form inputs
        # ----------------------------
        name = request.form.get("name", "").strip()
        voter_id = request.form.get("voter_id", "").strip()
        comment = request.form.get("comment", "").strip()

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

        return jsonify(
            {
                "success": True,
                "response": ai_response,
                "input": {
                    "name": name,
                    "voter_id": voter_id,
                    "comment": comment,
                },
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
# Main
# --------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not set!")
    else:
        print("✓ OpenAI API key loaded successfully")

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
    )
