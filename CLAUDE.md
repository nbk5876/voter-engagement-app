# Voter Engagement App - Project Context

## Architecture
![Service Stack](diagrams/Voter%20Engagement%20Prototype%20Service%20Stack.png)
![Form Design](diagrams/Voter%20Engagement%20Form%20Design.png)
![Dev Roadmap](diagrams/Voter%20Engagement%20Dev%20Roadmap.png)

- **Backend**: Python Flask app (`votereng.py`)
- **Frontend**: `templates/index.html` (single-page form)
- **AI**: OpenAI ChatGPT GPT-4o-mini for generating responses
- **Email**: MailGun for sending email responses to voters
- **Database**: PostgreSQL (local: `votereng_dev`, Render: `votereng_db`)
- **Hosting**: Render (https://voter-engagement-app.onrender.com/)
- **Repo**: GitHub (nbk5876/voter-engagement-app)

## Deployment
- Render auto-deploys from `main` branch on push
- **UptimeRobot** pings the Render service to keep it alive — cold starts are NOT an issue
- Python version pinned to 3.12 (`.python-version`) for psycopg2-binary compatibility
- Startup notification email sent on each deploy (includes commit message on Render)

## Database
- **Local**: PostgreSQL on Windows, database `votereng_dev`
- **Render**: Managed PostgreSQL, database `votereng_db`
- **Tables**: `voter_submissions` (id, name, voter_id, email, comment, ai_response, candidate_key, created_at)
- **ORM**: Flask-SQLAlchemy

## Candidate Personalities
Selectable via `?ca=` query parameter:
- `saw` — Kshama Sawant (socialist)
- `cha` — Melissa Chaudhry (anti-war constitutionalist)
- `tur` — Jack Turner (fictional, hard-right conservative)
- `mod` — Karen Morales (fictional, moderate Democrat) **← default**

Context files in `context/` folder.

## Key Files
- `votereng.py` — Main Flask app with `/respond` endpoint, AI API calls, MailGun email, database writes
- `personality.py` — Candidate selection logic and context loading
- `templates/index.html` — Frontend form and JavaScript fetch logic
- `context/*.txt` — Candidate personality context files

## Email Format
- Email body uses Unicode box-drawing character (━) as section separators (15 chars wide)
- Sections: YOUR INFORMATION, AI RESPONSE
- Sent via MailGun REST API

## Roadmap (v1.2 complete)
- **v1.0** ✓ — Basic voter question submission
- **v1.1** ✓ — GitHub deploy, candidate personalities, MailGun email
- **v1.2** ✓ — PostgreSQL database (local + Render), startup notifications
- **v1.3** — Use Cases, Full DB Design
- **v1.4** — Expand schema for ENH-001 through ENH-005

## Next Up
- **Google OAuth** (UC-CF-11) — Required for email field and Civic Group features
- See `docs/Enhancement-Requests.md` for future enhancements
