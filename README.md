# Mshengu Quiz App (Flask) 
attention : Mentec Foundation -- William Mutau--

============== By SIZWE ERNEST MABUZA=============
               9103185935080

A clean, single-file Flask backend with Jinja templates for a multiple-choice quiz. Stores user progress in session and supports question shuffling.

## Features
- Name entry + session-based progress
- One-question-at-a-time flow with progress bar
- Review page with correct/incorrect highlights and explanations
- Questions loaded from `data/questions.json` (easy to edit)
- Minimal dependencies (Flask only)

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py          # Windows PowerShell: $env:FLASK_APP="app.py"
export FLASK_RUN_PORT=5000
flask run
```

Then open http://localhost:5000 in your browser.

## Customize Questions
Edit `data/questions.json`:
```json
{
  "title": "Your Quiz Title",
  "questions": [
    {
      "text": "Question text?",
      "options": ["A", "B", "C", "D"],
      "correct_index": 2,
      "explanation": "Optional explanation",
      "hint": "Optional hint"
    }
  ]
}
```

## Environment
- `QUIZ_APP_SECRET`: optional Flask secret key for sessions.
- `PORT`: override default port when running `python app.py` directly.

## Notes
- This app stores answers in the session cookie; if you need persistence, add a database and user accounts.
- To deploy, you can use Railway/Render/Fly.io/Heroku-like platforms; remember to set `QUIZ_APP_SECRET`.