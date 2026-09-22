try:
    import os
    from flask import Flask, render_template, request, jsonify
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from dotenv import load_dotenv
    from openai import OpenAI
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Activate your virtual environment and run: "
        "pip install -r requirements.txt"
    ) from exc

load_dotenv()
app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Edit this knowledge base with your latest personal information.
PROFILE = {
    "name": "Sanjay Prasad .C",
    "role": "ECE CPS Student | ML & AI Enthusiast",
    "college": "SRM Institute of Science and Technology (SRM IST)",
    "course": "ECE CPS",
    "school": "Sri Sankara Vidyalaya",
    "tenth": "76.2% (2019)",
    "twelfth": "77.8% (2021)",
    "college_joined": "2024",
    "about": (
        "I am an ECE CPS student interested in electronics, computing, "
        "machine learning, web development and practical technology projects."
    ),
    "skills": [
        "HTML",
        "Python",
        "MS Excel",
        "MS PowerPoint",
        "MS Word",
        "Basics of Artificial Intelligence",
        "Data Structures",
    ],
    "internship": (
        "ML Internship — worked on machine learning workflow, data inspection, "
        "data cleaning, exploratory data analysis, feature engineering, "
        "classification, regression, clustering and portfolio/chatbot development."
    ),
    "projects": [
        {
            "name": "Smart Accident Detection and Emergency Alert System",
            "description": (
                "An embedded safety project that detects possible accidents and "
                "triggers an emergency alert using sensors, a microcontroller, "
                "communication hardware and an alert mechanism."
            ),
        },
        {
            "name": "Smart Irrigation",
            "description": "IoT-based water control for smarter irrigation.",
        },
        {
            "name": "Face Detection",
            "description": "Machine-learning/computer-vision project using OpenCV.",
        },
    ],
    "certifications": [
        "Digital logic design : A complete Guide",
        "Learn pyhton programming- Beginner to master",
    ],
    "achievements": [
        "participated in NGO",
    ],
    "github": "https://github.com/sanjayprasad",
    "linkedin": "https://www.linkedin.com/in/sanjayprasad1605",
    "email": "sanjayprasad160407@gmail.com",
}

# Retrieval-based chatbot knowledge.
KNOWLEDGE = [
    (f"My name is {PROFILE['name']}. My role is {PROFILE['role']}.", 
     ["profile", "name", "who are you", "student", "about"]),
    (f"{PROFILE['about']}", 
     ["about", "yourself", "introduce", "profile"]),
    (f"I study {PROFILE['course']} at {PROFILE['college']}. I joined college in {PROFILE['college_joined']}.",
     ["education", "college", "course", "degree", "study"]),
    (f"My school is {PROFILE['school']}. I scored {PROFILE['tenth']} in Class 10 and {PROFILE['twelfth']} in Class 12.",
     ["school", "10th", "12th", "marks", "percentage"]),
    (f"My technical skills include: {', '.join(PROFILE['skills'])}.",
     ["skills", "technical", "programming", "tools", "abilities"]),
    (PROFILE["internship"],
     ["internship", "intern", "experience", "training"]),
]

for project in PROFILE["projects"]:
    KNOWLEDGE.append(
        (f"{project['name']}: {project['description']}",
         ["project", project["name"].lower(), "machine learning", "ml", "iot", "accident"])
    )

KNOWLEDGE.append(
    (f"My certifications include: {', '.join(PROFILE['certifications'])}.",
     ["certification", "certificate", "course"])
)
KNOWLEDGE.append(
    (f"My achievements include: {', '.join(PROFILE['achievements'])}.",
     ["achievement", "award", "accomplishment"])
)
KNOWLEDGE.append(
    (f"My GitHub is {PROFILE['github']} and my LinkedIn is {PROFILE['linkedin']}.",
     ["github", "linkedin", "social", "links", "contact"])
)
KNOWLEDGE.append(
    (f"I can be contacted at {PROFILE['email']}.",
     ["email", "contact", "reach", "mail"])
)

texts = [item[0] + " " + " ".join(item[1]) for item in KNOWLEDGE]
vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(texts)


def chatbot_reply(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Please type a question about my profile, skills, education, internship, projects, certifications or experience."

    q_vector = vectorizer.transform([q])
    scores = cosine_similarity(q_vector, matrix)[0]
    best_index = int(scores.argmax())
    confidence = float(scores[best_index])

    # Casual conversation and low-confidence fallback.
    normalized = q.lower()
    greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "good night"}
    if normalized in greetings or normalized.startswith(("hi ", "hello ", "hey ")):
        return f"Hello! I'm Sanjay's portfolio assistant. Ask me about his skills, education, internship, projects or experience."

    if confidence < 0.12:
        return (
            "I can answer questions about Sanjay's profile, education, technical skills, "
            "internship, ML projects, certifications, achievements, experience and contact links."
        )

    if client:
        try:
            context = "\n".join(item[0] for item in KNOWLEDGE)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                instructions="Answer only using the portfolio information provided. If unknown, say you do not know.",
                input=f"Portfolio information:\n{context}\n\nQuestion: {q}"
            )
            return response.output_text
        except Exception as exc:
            app.logger.exception("OpenAI request failed: %s", exc)
    return KNOWLEDGE[best_index][0]


@app.route("/")
def home():
    return render_template("index.html", profile=PROFILE)


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("message", "")
    return jsonify({"reply": chatbot_reply(question)})


if __name__ == "__main__":
    app.run(debug=True)
