
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the API key
genai.configure(api_key=API_KEY)

# Use the Gemini 2.5 Flash model
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

# Your prompt
prompt = "Summarize the theory of relativity in 3 sentences."

# Generate a response
response = model.generate_content(prompt)

# Print the result
print("Response from gemini-2.0-flash:")
print(response.text)
