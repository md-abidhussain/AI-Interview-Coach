🎓 AI Interview Coach
AI-powered interview practice tool with role-specific questions, voice/text answers, Gemini AI feedback, and secure user authentication.

### Topics:
`python`, `streamlit`, `gemini-api`, `whisper`, `sqlite`, `bcrypt`, `nlp`, `interview-prep`, `ai`, `speech-recognition`

💡 Project Type: Voice + Text Based AI App  
🛠️ Built With: Streamlit, Gemini Flash API, Whisper, SpeechRecognition, SQLite  
☁️ Deployed On: [Streamlit Cloud](https://ai-interview-coach-06122005.streamlit.app/)

🔑 Features

🎤 Voice input + transcription using Whisper
✍️ Text-based answer option
🧠 AI-generated questions based on job role
🗣️ AI feedback on both content + communication
🔐 User login/signup with secure SQLite storage & bcrypt password hashing
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

3. Create a `.env` file in the root directory and add your database and API credentials:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   DATABASE_URL=users.db
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

⚙️ Secret Configurations & Deployment

### 1. SQLite Database Configuration
This project uses **SQLite** for user account registration and login authentication.
* **Local Run:** Set the `DATABASE_URL` key in your `.env` file (e.g., `DATABASE_URL=users.db`). If not set, it defaults to `users.db` automatically.
* **Streamlit Cloud:** Add `DATABASE_URL` to your **App Secrets** (see below).

*Note: The app will automatically connect and initialize the `users` table on startup.*

### 2. GitHub Secrets (Git Secrets)
To securely store credentials in GitHub (e.g. for CI/CD runners):
1. Go to your GitHub repository at [md-abidhussain/AI-Interview-Coach](https://github.com/md-abidhussain/AI-Interview-Coach).
2. Click on the **Settings** tab.
3. In the left sidebar, click **Secrets and variables** -> **Actions**.
4. Click the **New repository secret** button.
5. Create secrets for:
   - `GEMINI_API_KEY`
   - `DATABASE_URL`

### 3. Streamlit Cloud Secrets (Production Deployment)
Streamlit Cloud uses its own secret manager to run the app. To add your database credentials and API key for the live website:
1. Log into your dashboard at [share.streamlit.io](https://share.streamlit.io/).
2. Locate the **AI Interview Coach** app in the list.
3. Click the three dots `...` next to the app name and choose **Settings**.
4. Select **Secrets** on the left menu.
5. Enter your configuration keys in TOML format:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   DATABASE_URL = "users.db"
   ```
6. Click **Save**. The app will automatically restart and be active!
