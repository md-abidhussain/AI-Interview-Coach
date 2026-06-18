import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

# Fallback models in priority order to handle rate limits and future deprecations
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest"
]

def generate_with_fallbacks(prompt):
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            pass
            
    if not api_key:
        raise ValueError("🔑 GEMINI_API_KEY is missing! Please configure GEMINI_API_KEY in your environment or Streamlit App Secrets.")
        
    genai.configure(api_key=api_key, transport='rest')
    
    last_err = None
    for model_name in FALLBACK_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            # Use request_options to set timeout so we don't hang if a model is unavailable
            response = model.generate_content(prompt, request_options={'timeout': 15.0})
            return response.text
        except Exception as e:
            last_err = e
            # Output traceback or error internally for debug logs
            print(f"Fallback warning: Failed with {model_name} -> {e}. Trying next model...")
            
    if last_err:
        raise last_err
    raise ValueError("Failed to generate content using all fallback models.")

# Function to get feedback and rating score from Gemini model
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
        
        # Extract score and feedback from model response
        if "Score:" in response_text:
            feedback, score = response_text.split("Score:")
            clean_score = score.strip().replace(",", "").replace(".", "")
            return feedback.strip(), clean_score
        else:
            return response_text.strip(), "N/A"
    except Exception as e:
        return f"❌ Error evaluating answer: {str(e)}", "N/A"

# Function to generate interview question based on the role
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
        return f"❌ Error generating question: {str(e)}"

