🎓 AI Interview Coach

An interactive AI-based platform to help users practice interview questions and get real-time feedback on their communication and technical responses.

💡 Project Type: Voice + Text Based AI App  
🛠️ Built With: Streamlit, Gemini Flash API, Whisper, SpeechRecognition, Pandas  
☁️ Deployed On: [Streamlit Cloud](https://ai-interview-coach-06122005.streamlit.app)

🔑 Features

🎤 Voice input + transcription using Whisper
✍️ Text-based answer option
🧠 AI-generated questions based on job role
🗣️ AI feedback on both content + communication
🔐 User login/signup with session control
🎨 Modern dark mode UI with gradient styling
🧪 Robust Gemini model fallback chain (Gemini 2.5-flash -> 2.0-flash -> 1.5-flash)

🚀 How To Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/md-abidhussain/AI-Interview-Coach
   cd AI-Interview-Coach
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

⚙️ Streamlit Cloud Deployment Config
To deploy on Streamlit Cloud:
1. Log in to [share.streamlit.io](https://share.streamlit.io/) via GitHub.
2. In the App settings, go to **Secrets** and add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
