# Call5 Democracy - Project Context

## Vision
Call5 Democracy is a **hub-and-spoke civic engagement platform** that orchestrates notifications across existing social networks (Nextdoor, Bluesky, Mastodon, email) rather than creating another platform. The hub (Call5) hosts substantive discussions while spokes deliver notifications to members via their preferred channels.

## Architecture
![Service Stack](diagrams/Voter%20Engagement%20Prototype%20Service%20Stack.png)
![Form Design](diagrams/Voter%20Engagement%20Form%20Design.png)
![Dev Roadmap](diagrams/Voter%20Engagement%20Dev%20Roadmap.png)

- **Backend**: Python Flask app (`votereng.py`)
- **Frontend**: `templates/index.html` (single-page form)
- **AI**: OpenAI ChatGPT GPT-4o-mini for generating responses
- **Auth**: Google OAuth via Flask-Dance (progressive authentication)
- **Email**: MailGun for sending email responses to voters
- **Notifications**: Hub-and-spoke routing (Nextdoor, Bluesky, Mastodon, email)
- **Database**: PostgreSQL (local: `votereng_dev`, Render: `votereng_db`)
- **Hosting**: Render (https://voter-engagement-app.onrender.com/)
- **Repo**: GitHub (nbk5876/voter-engagement-app)

## Deployment
- Render auto-deploys from `main` branch on push
- **UptimeRobot** pings the Render service to keep it alive — cold starts are NOT an issue
- Python version pinned to 3.12 (`.python-version`) for psycopg2-binary compatibility
- Startup notification email sent on each deploy (includes commit message on Render)

## Authentication
- **Google OAuth** via Flask-Dance (UC-CF-11)
- Progressive authentication: anonymous users can submit, logged-in users get email responses
- Session stores `user_email` and `user_name` from Google profile
- `voter_id` in database: Google email if logged in, NULL if anonymous
- Admin emails always sent; user email only if authenticated

## Database
- **Local**: PostgreSQL on Windows, database `votereng_dev`
- **Render**: Managed PostgreSQL, database `votereng_db`
- **Tables**: `voter_submissions` (id, name, voter_id, email, comment, ai_response, candidate_key, created_at)
- **ORM**: Flask-SQLAlchemy
- `voter_id` column is nullable (supports anonymous submissions)

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

## Use Cases (v0.3)
See `docs/Call5_v0.3_Use_Cases_Integrated.md` for complete documentation.

### Voter Questions
- **UC-VQ-1**: Submit Question (anonymous or authenticated)
- **UC-VQ-2**: AI Candidate Response (triggers hub-and-spoke notifications if member)

### Civic Group Formation (UC-CF-1 through UC-CF-12)
- Create/join groups, invite members, track invitation networks
- **Single membership rule**: Member of ONE group, can lead ANOTHER (ENH-005)
- Platform preference management per member
- UC-CF-11 (Google OAuth) ✓ implemented

### Hub-and-Spoke Notifications (UC-HS-1 through UC-HS-6)
- UC-HS-1: Group Leader posts announcement → routes to all member platforms
- UC-HS-2: AI responses shared with civic groups
- UC-HS-3: Call-5 recruitment via existing social networks
- UC-HS-4: Cross-platform discussion threads (conversation stays in hub)
- UC-HS-5: Post-election network persistence
- UC-HS-6: Platform migration flexibility

### Admin (UC-ADM-1 through UC-ADM-5)
- System health monitoring, candidate management, campaign promises

## Roadmap (prototype versioning reset at v0.3)
- **v1.0** ✓ — Connect voters to AI for policy questions in candidate-scoped context
- **v1.1** ✓ — Deploy GitHub framework, candidate personalities, Claude Code, MailGun email
- **v1.2** ✓ — PostgreSQL database (local + Render), Google OAuth authentication
- **v0.3** — Call 5 Hub and Spoke: Use Cases, Full DB Design
- **v0.4** — Expand schema for ENH-001 through ENH-005

## Future Enhancements (v0.4+)
- **ENH-001**: Group Leaders as news/event channels
- **ENH-002**: Campaign promise repository
- **ENH-003**: AI-powered promise news scanning
- **ENH-004**: Post-election network persistence
- **ENH-005**: Single membership, multiple leadership model

## Next Up
- Full DB design based on Use Cases document (new entities: Users, Platform Preferences, Invitations, Announcements, Notifications)
- Civic Group features (UC-CF-1 through UC-CF-10)
- Platform API research (Bluesky AT Protocol, Mastodon ActivityPub, Nextdoor)
- See `docs/Enhancement-Requests.md` for additional enhancements
