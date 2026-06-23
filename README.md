# 🎓 AI Interview Coach

> AI-powered interview practice platform with role-specific questions, multi-modal answer input, real-time Gemini feedback, and secure user authentication.

🔗 **Live Demo:** [ai-interview-coach-06122005.streamlit.app](https://ai-interview-coach-06122005.streamlit.app/)

---

## 📌 Overview

AI Interview Coach helps job seekers practice interviews for any role — SDE, Data Analyst, Product Manager, and more. Users get AI-generated questions, answer via text, uploaded audio, or live microphone, and receive instant structured feedback with a score out of 10.

Built as a solo project during an AI internship. Idea, architecture, and core logic are original.

---

## ✨ Features

- 🔐 **Secure Authentication** — bcrypt-hashed passwords stored in SQLite; supports login, signup, and guest mode
- 💬 **Role-Specific Questions** — Gemini generates tailored interview questions based on the target job role
- ✍️ **Text Answer Mode** — Type your response and get instant AI evaluation
- 🎙️ **Audio Upload Mode** — Upload an MP3/WAV/M4A file; Whisper transcribes it, Gemini evaluates it
- 🎤 **Live Mic Mode** — Speak directly; real-time transcription via SpeechRecognition
- 🤖 **4-Model Fallback Chain** — Tries `gemini-2.5-flash → gemini-2.0-flash → gemini-1.5-flash → gemini-flash-latest` for high availability
- 📊 **AI Scoring** — Structured feedback on knowledge, clarity, and relevance with a score out of 10
- ⚠️ **Graceful Error Handling** — API failures return user-friendly messages, never raw crashes

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| AI / LLM | Google Gemini API (`google-generativeai`) |
| Speech-to-Text | OpenAI Whisper + SpeechRecognition |
| Audio Processing | pydub |
| Database | SQLite (`sqlite3`) |
| Auth | bcrypt |
| Config | python-dotenv |
| Deployment | Streamlit Cloud |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│              Streamlit Frontend          │
│   Login / Signup / Guest  ──▶  App UI   │
└────────────┬────────────────────────────┘
             │
     ┌───────▼────────┐
     │   login.py      │  bcrypt auth + SQLite users table
     └───────┬─────────┘
             │
     ┌───────▼────────┐
     │   app.py        │  Session state + answer routing
     └──┬────┬─────┬──┘
        │    │     │
   Text │  Audio  Mic
        │    │     │
        │  whisper_transcriber.py
        │  mic_input.py
        │    │     │
     ┌──▼────▼─────▼──┐
     │  gemini_module  │  4-model fallback chain + prompt engineering
     └────────────────┘
```

---

## 📂 Project Structure

```
├── app.py                  # Main Streamlit app + UI logic
├── login.py                # Auth: bcrypt + SQLite signup/login
├── gemini_module.py        # Gemini API integration + fallback chain
├── whisper_transcriber.py  # Audio file → text (Whisper)
├── mic_input.py            # Live mic → text (SpeechRecognition)
├── requirements.txt
├── .env                    # (not committed) API keys
└── .gitignore
```

---

## 🚀 Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/md-abidhussain/ai-interview-coach.git
cd ai-interview-coach
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## 🔐 Security Design

- Passwords hashed with `bcrypt.hashpw()` on signup — never stored in plain text
- `bcrypt.checkpw()` used for login verification — original password is never recoverable
- API key loaded from `.env` → Streamlit Secrets → raises clear error if missing
- `.env` and `users.db` excluded from version control via `.gitignore`

---

## 🤖 Gemini Fallback Logic

```python
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest"
]
```

Each model is tried with a 15-second timeout. If all fail, a user-friendly error message is returned — the app never crashes raw on API failure.

---

## 📸 Screenshots

| Login Page | Interview Screen | AI Feedback |
|---|---|---|
| ![Login Page](screenshots/login_interface.png) | ![Interview Screen](screenshots/asking_question_interface.png) | ![AI Feedback](screenshots/ai_feedback_interface.png) |

---

## 🔮 Future Improvements

- Session history — store past questions and scores per user in SQLite
- Password strength validation on signup
- Logout button with session expiry
- Dashboard showing improvement over time
- Support for more roles and difficulty levels

---

## 👨💻 Author

**Mohd Abid Hussain** — CSE @ Jamia Hamdard  
[LinkedIn](https://www.linkedin.com/in/md-abidhussain) · [GitHub](https://github.com/md-abidhussain)

---

*Built with Python, Streamlit, and Google Gemini API*
