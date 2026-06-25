from google import genai
import streamlit as st
from dotenv import load_dotenv
import os

def get_genai_client():
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing! Please configure GEMINI_API_KEY in your environment or Streamlit App Secrets.")
    return genai.Client(api_key=api_key)

def generate_api_response(prompt):
    client = get_genai_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini generation failed: {e}")

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
        response_text = generate_api_response(prompt)
        
        if "Score:" in response_text:
            feedback, score = response_text.split("Score:")
            clean_score = score.strip().replace(",", "").replace(".", "")
            return feedback.strip(), clean_score
        else:
            return response_text.strip(), "N/A"
    except Exception as e:
        raise RuntimeError(f"Gemini API Feedback Error: {e}")

def generate_question(role):
    prompt = f"""
    You are a professional interviewer. The candidate is applying for the role: {role}.
    Give one descriptive, open-ended interview question to start the interview.
    Only return the question, nothing else.
    """
    try:
        response_text = generate_api_response(prompt)
        return response_text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API Question Error: {e}")
