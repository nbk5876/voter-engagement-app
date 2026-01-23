# Voter Engagement App - Project Context

## Architecture
![Service Stack](diagrams/Voter%20Engagement%20Prototype%20Service%20Stack.png)

- **Backend**: Python Flask app (`votereng.py`)
- **Frontend**: `templates/index.html` (single-page form)
- **AI**: OpenAI ChatGPT GPT-4o-mini for generating responses
- **Email**: MailGun for sending email responses to voters
- **Hosting**: Render (https://voter-engagement-app.onrender.com/)
- **Repo**: GitHub (nbk5876/voter-engagement-app)

## Deployment
- Render auto-deploys from `main` branch on push
- **UptimeRobot** pings the Render service to keep it alive — cold starts are NOT an issue

## Key Files
- `votereng.py` — Main Flask app with `/respond` endpoint, AI API calls, and MailGun email sending
- `templates/index.html` — Frontend form and JavaScript fetch logic

## Email Format
- Email body uses Unicode box-drawing character (━) as section separators (15 chars wide)
- Sections: YOUR INFORMATION, AI RESPONSE
- Sent via MailGun REST API
