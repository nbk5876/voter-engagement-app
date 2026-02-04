# Call5 Democracy

A civic engagement platform that sustains voter participation beyond traditional election cycles through an exponential "Call-5" network model. Users can ask questions to AI-powered candidate personalities and recruit others to join their network.

**Version:** v0.3.1
**Live Site:** https://voter-engagement-app.onrender.com

## Features

- **Google OAuth authentication** — Secure sign-in with Google accounts
- **AI-powered candidate Q&A** — Ask questions to candidate personalities with responses delivered via email
- **Network recruitment system** — Unique invite codes for each user
- **Referral tracking** — Track who recruited whom through the network
- **User dashboard** — View recruiter relationships and recruit counts
- **Multi-platform sharing** — Pre-written invite messages for Nextdoor, Twitter, Bluesky, Mastodon, and Email
- **Recruiter messaging** — Members can message their recruiter directly
- **Admin tools** — User reports and network tree visualization

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python Flask, SQLAlchemy |
| Database | PostgreSQL |
| Authentication | Google OAuth (Flask-Dance) |
| AI | OpenAI GPT-4o-mini |
| Email | MailGun API |
| Hosting | Render (auto-deploy from GitHub main branch) |

## Database Schema

**users** — Authenticated members with recruitment relationships
- `id`, `google_id`, `email`, `name`, `invite_code`
- `invited_by_user_id` — Foreign key to recruiter
- `is_admin`, `created_at`

**voter_submissions** — Questions and AI responses
- `id`, `name`, `voter_id`, `email`, `comment`
- `ai_response`, `candidate_key`, `created_at`

## Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page with voter question form |
| `/dashboard` | Authenticated user dashboard |
| `/share` | Multi-platform invite sharing |
| `/message-recruiter` | Send message to recruiter |
| `/admin` | Admin user report (admin only) |
| `/admin/network` | Network tree visualization (admin only) |
| `/respond` | POST endpoint for AI response generation |
| `/docs/use-cases` | Use cases documentation |
| `/docs/concepts` | Call 5 People concepts |

## Local Development

### 1. Clone and Install

```bash
git clone https://github.com/nbk5876/voter-engagement-app.git
cd voter-engagement-app
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/votereng_dev

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# MailGun
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain

# Flask
FLASK_SECRET_KEY=your-secret-key
PORT=5000
```

### 3. Set Up Database

Create a local PostgreSQL database:

```bash
createdb votereng_dev
```

Tables are created automatically on first run.

### 4. Run

```bash
python votereng.py
```

Server starts at http://localhost:5000

## Candidate Personalities

Select via `?ca=` query parameter:

| Code | Candidate | Description |
|------|-----------|-------------|
| `mod` | Karen Morales | Moderate Democrat (default) |
| `saw` | Kshama Sawant | Socialist |
| `cha` | Melissa Chaudhry | Anti-war constitutionalist |
| `tur` | Jack Turner | Hard-right conservative (fictional) |

## Deployment

The app auto-deploys to Render when changes are pushed to `main`. UptimeRobot keeps the service alive to avoid cold starts.

## License

This is a development/prototyping environment for civic engagement tools.

## Support

- **GitHub Issues:** https://github.com/nbk5876/voter-engagement-app/issues
