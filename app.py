from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os, random
from datetime import timedelta

def load_questions():
    data_path = os.path.join(os.path.dirname(__file__), "data", "questions.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Shuffle questions to add variety
    random.shuffle(data["questions"])
    return data

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("QUIZ_APP_SECRET", "dev_secret_change_me")
app.permanent_session_lifetime = timedelta(hours=6)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Please enter your name to start.", "error")
            return render_template("home.html")
        session.clear()
        session["player_name"] = name
        session["current_index"] = 0
        # Load questions fresh per attempt to allow shuffling
        payload = load_questions()
        session["quiz_title"] = payload.get("title", "Mshengu Quiz")
        session["questions"] = payload["questions"]
        session["answers"] = []
        return redirect(url_for("quiz"))
    return render_template("home.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "questions" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice is None:
            flash("Please select an option before continuing.", "error")
        else:
            # store chosen option index as int
            session["answers"].append(int(choice))
            session["current_index"] += 1

    idx = session.get("current_index", 0)
    questions = session["questions"]

    if idx >= len(questions):
        return redirect(url_for("result"))

    q = questions[idx]
    progress = {
        "current": idx + 1,
        "total": len(questions),
        "percent": int(((idx) / len(questions)) * 100)
    }
    return render_template("quiz.html", question=q, index=idx, progress=progress)

@app.route("/result")
def result():
    if "questions" not in session:
        return redirect(url_for("home"))

    questions = session["questions"]
    answers = session.get("answers", [])
    score = 0
    review = []

    for i, q in enumerate(questions):
        selected = answers[i] if i < len(answers) else None
        correct = q["correct_index"]
        is_correct = (selected == correct)
        if is_correct:
            score += 1
        review.append({
            "question": q["text"],
            "options": q["options"],
            "selected": selected,
            "correct": correct,
            "explanation": q.get("explanation", "")
        })

    result_data = {
        "name": session.get("player_name", "Player"),
        "score": score,
        "total": len(questions),
        "percent": int((score / max(1, len(questions))) * 100),
        "review": review
    }
    return render_template("result.html", result=result_data)

@app.route("/restart")
def restart():
    # Keep the name to avoid retyping, but refresh the quiz content
    name = session.get("player_name", "")
    session.clear()
    if name:
        session["player_name"] = name
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)