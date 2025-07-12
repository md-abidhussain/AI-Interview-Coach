import google.generativeai as genai

# ✅ Set up your Gemini API key
genai.configure(api_key="AIzaSyBnXv6d13Uc6mjtHWgEu_hiuCG4nYFalJ0")  # 👈 Replace this

# ✅ Load Gemini Flash model once
gemini_model = genai.GenerativeModel("models/gemini-2.0-flash")

# --------------------------------------
# 🔹 1. Feedback + Score Function
# --------------------------------------
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

    response = gemini_model.generate_content(prompt).text

    # Clean split and formatting
    if "Score:" in response:
        feedback, score = response.split("Score:")
        clean_score = score.strip().replace(",", "").replace(".", "")
        return feedback.strip(), clean_score
    else:
        return response.strip(), "N/A"

# --------------------------------------
# 🔹 2. Generate Interview Question
# --------------------------------------
def generate_question(role):
    prompt = f"""
    You are a professional interviewer. The candidate is applying for the role: {role}.
    Give one descriptive, open-ended interview question to start the interview.
    Only return the question, nothing else.
    """
    response = gemini_model.generate_content(prompt).text
    return response.strip()
