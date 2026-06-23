import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import random

FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest"
]

FALLBACK_QUESTIONS = {
    "sde": [
        "Can you explain the difference between a process and a thread, and when you would use multi-threading?",
        "How do you design a scalable system like a URL shortener? Describe the database choice and caching strategy.",
        "Describe a challenging technical problem you solved in a past project. How did you identify the bottleneck and solve it?",
        "What is the difference between SQL and NoSQL databases, and how do you decide which one to use for a project?",
        "Explain how memory management works in Python or another language of your choice. What is garbage collection?"
    ],
    "data analyst": [
        "How do you handle missing or corrupt data in a dataset during the data cleaning process?",
        "Explain the difference between JOIN and UNION in SQL, and give a scenario where you would use each.",
        "Describe a time when you used data analysis to solve a real-world business problem. What metrics did you focus on?",
        "What is A/B testing, and how would you design an experiment to test a new feature on a website?",
        "Can you explain the difference between correlation and causation with a real-world example?"
    ],
    "product manager": [
        "How would you measure the success of a new feature like Instagram Stories?",
        "Tell me about a time you had to make a product decision without having all the data you needed.",
        "How do you prioritize features on a product roadmap when stakeholders have conflicting demands?",
        "Choose a product you use daily. How would you improve it, and why?",
        "How would you design an interview prep platform for university students?"
    ]
}

GENERAL_FALLBACK_QUESTIONS = [
    "Tell me about yourself and why you are interested in this role.",
    "Describe a time you had a conflict with a team member. How did you resolve it, and what did you learn?",
    "What is your greatest technical strength, and what is an area you are actively trying to improve?",
    "Describe a situation where you had to learn a new technology or domain very quickly to deliver a project.",
    "Where do you see yourself in five years, and how does this role fit into your career path?"
]

def get_local_fallback_question(role):
    if not role:
        return random.choice(GENERAL_FALLBACK_QUESTIONS)
    role_lower = role.lower()
    if any(k in role_lower for k in ["sde", "software", "developer", "engineer", "programmer", "coding", "technical"]):
        return random.choice(FALLBACK_QUESTIONS["sde"])
    elif any(k in role_lower for k in ["data", "analyst", "analytics", "bi", "sql"]):
        return random.choice(FALLBACK_QUESTIONS["data analyst"])
    elif any(k in role_lower for k in ["product", "pm", "manager"]):
        return random.choice(FALLBACK_QUESTIONS["product manager"])
    return random.choice(GENERAL_FALLBACK_QUESTIONS)

def get_local_fallback_feedback(answer, role):
    word_count = len(answer.split())
    if word_count < 10:
        score = 4
        feedback = f"Your response is quite brief. Try to structure your thoughts using the STAR method (Situation, Task, Action, Result) and provide specific technical details relevant to a {role} role."
    elif word_count < 30:
        score = 6
        feedback = f"Good initial response! You touched on the key aspects of the question, but could improve by adding concrete details of tools/technologies used and quantitative impact metrics for a {role} role."
    else:
        score = 8
        feedback = f"Excellent response! You provided a detailed explanation showing great technical depth and domain understanding. Make sure to keep your delivery clear and well-structured."
    return feedback, str(score)

def generate_with_fallbacks(prompt):
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
    if not api_key:
        raise ValueError("🔑 GEMINI_API_KEY is missing! Please configure GEMINI_API_KEY in your environment or Streamlit App Secrets.")
        
    genai.configure(api_key=api_key, transport='rest')
    
    last_err = None
    for model_name in FALLBACK_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, request_options={'timeout': 15.0})
            return response.text
        except Exception as e:
            last_err = e
            print(f"Fallback warning: Failed with {model_name} -> {e}. Trying next model...")
            
    if last_err:
        raise last_err
    raise ValueError("Failed to generate content using all fallback models.")

def get_feedback(answer, role, mode="text"):
    if mode == "text":
        prompt = f"""
        You are an expert interview evaluator. The candidate is applying for the role: {role}.
        Their answer is below.

        TASK:
        1. Provide detailed feedback on knowledge, clarity, and relevance.
        2. Rate their knowledge from 1 to 10 (just the number).

        Format:
        Feedback: <your feedback>
        Score: <1-10>

        Answer:
        {answer}
        """
    else:
        prompt = f"""
        The candidate is applying for: {role}.
        Evaluate their spoken response (transcribed below) for:
        - Knowledge
        - Communication
        - Confidence

        TASK:
        1. Give feedback on their performance.
        2. Give an overall score out of 10 (just the number).

        Format:
        Feedback: <your feedback>
        Score: <1-10>

        Answer:
        {answer}
        """

    try:
        response_text = generate_with_fallbacks(prompt)
        
        if "Score:" in response_text:
            feedback, score = response_text.split("Score:")
            clean_score = score.strip().replace(",", "").replace(".", "")
            return feedback.strip(), clean_score
        else:
            return response_text.strip(), "N/A"
    except Exception as e:
        print(f"Gemini API Feedback Error: {e}. Falling back to local offline evaluator.")
        feedback, score = get_local_fallback_feedback(answer, role)
        return f"{feedback} (Note: Offline feedback generated due to temporary connectivity issues)", score

def generate_question(role):
    prompt = f"""
    You are a professional interviewer. The candidate is applying for the role: {role}.
    Give one descriptive, open-ended interview question to start the interview.
    Only return the question, nothing else.
    """
    try:
        response_text = generate_with_fallbacks(prompt)
        return response_text.strip()
    except Exception as e:
        print(f"Gemini API Question Error: {e}. Falling back to offline predefined question catalog.")
        return get_local_fallback_question(role)
