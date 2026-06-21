🎓 AI Interview Coach

An interactive AI-based platform to help users practice interview questions and get real-time feedback on their communication and technical responses.

💡 Project Type: Voice + Text Based AI App  
🛠️ Built With: Streamlit, Gemini Flash API, Whisper, SpeechRecognition, PostgreSQL  
☁️ Deployed On: [Streamlit Cloud](https://ai-interview-coach-06122005.streamlit.app/)

🔑 Features

🎤 Voice input + transcription using Whisper
✍️ Text-based answer option
🧠 AI-generated questions based on job role
🗣️ AI feedback on both content + communication
🔐 User login/signup with secure PostgreSQL storage & bcrypt password hashing
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
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

⚙️ Secret Configurations & Deployment

### 1. PostgreSQL Database Configuration
This project uses **PostgreSQL** exclusively for user account registration and login authentication.
* **Local Run:** Set the `DATABASE_URL` key in your `.env` file.
* **Streamlit Cloud:** Add `DATABASE_URL` to your **App Secrets** (see below).

*Note: The app will automatically connect and initialize the `users` table on startup once `DATABASE_URL` is provided.*

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
   DATABASE_URL = "postgresql://username:password@hostname:5432/dbname"
   ```
6. Click **Save**. The app will automatically restart and be active!
