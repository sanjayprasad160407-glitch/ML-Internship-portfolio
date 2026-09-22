# Python ML Portfolio + AI Chatbot

A responsive portfolio website built with **Python + Flask**, with a Python-powered retrieval chatbot using **TF-IDF + cosine similarity** from scikit-learn.

## Features

- About Me
- Education
- Technical Skills
- Internship Experience
- ML / technical projects
- Certifications
- Achievements
- Contact information
- GitHub / LinkedIn
- Floating portfolio chatbot
- Quick chatbot prompts
- Responsive UI

## 1. Create a virtual environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install packages

Make sure your virtual environment is activated, then run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `pip` cannot download packages, check your internet connection, proxy/firewall settings, or try again from a normal terminal with internet access.

## 3. Run

```bash
python app.py
```

Open the local address shown in the terminal, usually:

http://127.0.0.1:5000

## 4. Customize your portfolio

Open `app.py` and update the `PROFILE` dictionary:

- name
- role
- skills
- internship
- projects
- certifications
- achievements
- email
- GitHub
- LinkedIn

The chatbot automatically uses that same information.

## How the chatbot works

1. The portfolio sends the user's question from JavaScript to Python using `/chat`.
2. Python converts the question into TF-IDF features.
3. Cosine similarity finds the closest profile knowledge item.
4. The matching portfolio answer is returned as JSON.
5. JavaScript displays the answer in the chatbot window.

This approach is intentionally simple and local, so no paid AI API key is required.

## Deploying

This Flask project can be deployed to a Python-compatible hosting service such as Render, Railway, or PythonAnywhere. For production, run Flask behind a production WSGI server such as Gunicorn where supported.

## Enable OpenAI chatbot

1. Copy `.env.example` to `.env`.
2. Open `.env` and replace `sk-your-key-here` with your API key.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start the app: `python app.py`.
5. Open `http://127.0.0.1:5000` and refresh the page.

Never upload `.env` to GitHub or place the key in HTML/JavaScript.
