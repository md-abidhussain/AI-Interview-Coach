import streamlit as st
from login import show_login
from gemini_module import get_feedback, generate_question
from whisper_transcriber import transcribe_audio_file
from mic_input import record_and_transcribe

# ========== Custom CSS ========== #
def load_custom_css():
    st.markdown("""
        <style>
            html, body, [data-testid="stApp"] {
                height: 100%;            
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #1f1c2c, #928dab);
                font-family: 'Segoe UI', sans-serif;
                color: #f3f4f6;
            }
            .block-container {
                padding: 2rem;
            }
            h1.centered-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: #ffffff;
            }
            .subtext {
                text-align: center;
                font-size: 18px;
                margin-bottom: 2rem;
                color: #e2e8f0;
            }
            .question-box, .feedback-box, .answer-box {
                background-color: rgba(255,255,255,0.05);
                color: white;
                padding: 1rem;
                border-left: 6px solid #7c3aed;
                border-radius: 10px;
                margin-top: 1rem;
                font-size: 15px;
                line-height: 1.6;
                white-space: pre-wrap;
            }
            .score-badge {
                background: linear-gradient(to right, #9333ea, #7c3aed);
                padding: 8px 15px;
                border-radius: 30px;
                color: white;
                font-weight: bold;
                display: inline-block;
                font-size: 15px;
                margin-top: 0.7rem;
            }
            .login-section {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                width: 100vw;
                text-align: center;
                padding: 0;
                margin: 0;
            }
            .login-card {
                background: rgba(30, 27, 46, 0.95);
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                max-width: 480px;
                width: 60%;
            }
            .login-title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 0px;
                color: #f0f9ff;
            }
            footer {
                text-align: center;
                color: #cbd5e1;
                font-size: 14px;
                margin-top: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)

# ========== App Config ========== #
st.set_page_config(page_title="AI Interview Coach", layout="wide", page_icon="🎓")
load_custom_css()

# ========== Login ========== #
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='centered-title'>🔐 Welcome to AI Interview Coach</h1>", unsafe_allow_html=True)
    logged_in = show_login()  # Let user log in first
    if logged_in:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.stop()  # Stop if not logged in

# ========== Main App ========== #
if st.session_state.logged_in:
    st.markdown("<h1 class='centered-title'>🎓 Welcome to AI Interview Coach</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Practice your answers. Get AI feedback. Improve your interview skills.</div>", unsafe_allow_html=True)

    role = st.text_input("👨‍💻 Enter the job role you're preparing for: (Data Analyst, SDE)")

    if role:
        if 'interview_question' not in st.session_state:
            with st.spinner("💬 Generating interview question..."):
                st.session_state.interview_question = generate_question(role)

        st.markdown("### 💬 Gemini's Interview Question")
        st.markdown(f"<div class='question-box'>{st.session_state.interview_question}</div>", unsafe_allow_html=True)

        option = st.radio("🎯 Choose how you'll answer:", ["✍️ Text Input", "🎙️ Upload Audio", "🎤 Speak Live (Mic)"])

        if option == "✍️ Text Input":
            user_input = st.text_area("📝 Type your answer:")
            if st.button("📤 Submit Text Answer"):
                if user_input:
                    with st.spinner("Gemini is analyzing your answer..."):
                        feedback, score = get_feedback(answer=user_input, role=role, mode="text")
                    st.markdown("### 🗣️ Transcribed Answer")
                    st.markdown(f"<div class='answer-box'>{user_input}</div>", unsafe_allow_html=True)
                    st.markdown("### 💡 Gemini's Feedback")
                    st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                    st.markdown("### 📊 Your AI Score")
                    st.markdown(f"<div class='score-badge'>⭐ {score}/10</div>", unsafe_allow_html=True)
                else:
                    st.warning("Please enter your answer first!")

        elif option == "🎙️ Upload Audio":
            audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])
            if audio_file and st.button("📤 Submit Audio"):
                with st.spinner("Transcribing your voice..."):
                    try:
                        transcribed = transcribe_audio_file(audio_file)
                        st.success("📝 Transcription complete!")
                        st.markdown("### 🗣️ Transcribed Answer")
                        st.markdown(f"<div class='answer-box'>{transcribed}</div>", unsafe_allow_html=True)
                        with st.spinner("Evaluating answer..."):
                            feedback, score = get_feedback(answer=transcribed, role=role, mode="voice")
                        st.markdown("### 💡 Gemini's Feedback")
                        st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                        st.markdown("### 📊 Your AI Score")
                        st.markdown(f"<div class='score-badge'>⭐ {score}/10</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        elif option == "🎤 Speak Live (Mic)":
            if st.button("🎙️ Start Recording"):
                with st.spinner("Listening..."):
                    result = record_and_transcribe()
                st.markdown("### 🗣️ Transcribed Answer")
                st.markdown(f"<div class='answer-box'>{result}</div>", unsafe_allow_html=True)
                if result and "Error" not in result and "⚠️" not in result:
                    with st.spinner("Evaluating your response..."):
                        feedback, score = get_feedback(answer=result, role=role, mode="voice")
                    st.markdown("### 💡 Gemini's Feedback")
                    st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                    st.markdown("### 📊 Your AI Score")
                    st.markdown(f"<div class='score-badge'>⭐ {score}/10</div>", unsafe_allow_html=True)

    st.markdown("""
        <footer>
        ⚡ Created by <strong>Mohd Abid Hussain</strong> 🎓 CSE @ Jamia Hamdard
        </footer>
    """, unsafe_allow_html=True)
