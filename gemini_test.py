from google import genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print("Calling gemini-2.5-flash with google-genai...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Summarize the theory of relativity in 3 sentences."
)

print("Response:")
print(response.text)
