
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the API key
genai.configure(api_key=API_KEY)

# Use the Gemini Flash Latest model
model = genai.GenerativeModel(model_name="models/gemini-flash-latest")

# Your prompt
prompt = "Summarize the theory of relativity in 3 sentences."

# Generate a response
response = model.generate_content(prompt)

print("Response from gemini-flash-latest:")
print(response.text)
