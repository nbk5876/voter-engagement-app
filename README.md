# Voter Engagement App

A Python web application that facilitates civic engagement by enabling voters to submit questions to candidates and receive AI-generated responses based on candidate-specific context. The app also supports the "Call 5 People" civic networking model for sustained engagement beyond election cycles.

**Live Site:** [https://nbk5876.github.io/voter-engagement-app/](https://nbk5876.github.io/voter-engagement-app/)
**App on Render:** [https://votereng.onrender.com](https://votereng.onrender.com)

## Features

- Voter question/comment submission form
- AI-powered responses using OpenAI API
- Multiple candidate personality support (via query parameters)
- Mobile-friendly responsive design
- DEV/TST mode for debugging
- Documentation pages for Use Cases and Concepts

## Project Structure

```
voter-engagement-app/
├── votereng.py              # Main Flask application
├── personality.py           # Candidate personality configuration
├── simple_server.py         # Simple server for testing
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── index.html               # GitHub Pages landing page
├── context/                 # Candidate context files
│   ├── sawant.txt
│   ├── chaudhry.txt
│   └── turner.txt
├── templates/
│   ├── index.html                      # Main voter form
│   ├── voter_engage_use_cases_v1.html  # Use cases documentation
│   └── voter_engage_concepts_v1.html   # Concepts documentation
├── docs/
│   ├── Call 5 People - High Level Concept.pdf
│   ├── Use Cases - Living Document.pdf
│   ├── UC-CF-12-Candidate-Relationship.md
│   └── Enhancement-Requests.md
└── diagrams/
    └── Voter Engagement Prototype Components v 1.x.png
```

## Routes

| Route | Description |
|-------|-------------|
| `/` | Main voter question form |
| `/respond` | POST endpoint for AI response generation |
| `/docs/use-cases` | Use Cases documentation page |
| `/docs/concepts` | Call 5 People Concepts page |

## Query Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `ca` | `saw`, `cha`, `tur` | Select candidate personality |
| `mode` | `dev`, `tst` | Enable debug information display |

**Examples:**
- `/?ca=saw` - Kshama Sawant personality
- `/?ca=cha` - Chaudhry personality
- `/?ca=tur` - Jack Turner (Fictional) personality
- `/?mode=dev` - Show debug information

## Setup Instructions

### 1. Install Python Dependencies

Requires Python 3.8+

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

1. Get your API key from https://platform.openai.com/api-keys
2. Create a `.env` file:

```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run the Application

```bash
python votereng.py
```

The server starts at `http://localhost:5000`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use for responses |
| `OPENAI_MAX_TOKENS` | `500` | Maximum response tokens |
| `OPENAI_TEMPERATURE` | `0.7` | Response creativity (0-1) |
| `PORT` | `5000` | Server port |

## How It Works

1. A voter fills out the form with their name, voter ID, and question/comment
2. Form data is submitted to the Flask backend via POST
3. Flask loads the appropriate candidate context from `./context/`
4. OpenAI generates a response based on the candidate's positions and tone
5. The response is displayed on the page

## Call 5 People Model

The app supports a civic networking model where:
- Voters organize into small, trust-based Civic Groups
- Each member can invite up to 5 people
- Members can only join one group but can lead another
- Groups persist post-election for ongoing accountability

See `/docs/concepts` for full documentation.

## Documentation

- [Use Cases](/docs/use-cases) - Core use cases for the app
- [Concepts](/docs/concepts) - Call 5 People high-level concept
- [Enhancement Requests](docs/Enhancement-Requests.md) - Tracked enhancements
- [UC-CF-12](docs/UC-CF-12-Candidate-Relationship.md) - Candidate relationship use case

## Deployment

The app is configured for deployment on Render with `gunicorn`:

```bash
gunicorn votereng:app
```

## Security Notes

- Never commit `.env` file to version control
- Use HTTPS in production
- Implement rate limiting for production use
- Add input validation and sanitization
- Consider user authentication for sensitive features

## License

This is a development/prototyping environment for civic engagement tools.

## Support

- **Flask:** https://flask.palletsprojects.com/
- **OpenAI API:** https://platform.openai.com/docs
- **GitHub Issues:** https://github.com/nbk5876/voter-engagement-app/issues
