import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the API key with rest transport to avoid grpc hangs on Windows
genai.configure(api_key=API_KEY, transport='rest')

# Use the Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Test prompt
prompt = "Summarize the theory of relativity in 3 sentences."

# Generate response
response = model.generate_content(prompt)

print("Response from gemini-2.5-flash:")
print(response.text)
