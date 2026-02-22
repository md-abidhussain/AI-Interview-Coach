import streamlit as st
from login import show_login
from gemini_module import get_feedback, generate_question
from whisper_transcriber import transcribe_audio_file
from mic_input import record_and_transcribe

def apply_login_styles():
    st.markdown("""
    <style>
        /* Sleek dark gradient for login page */
        [data-testid="stApp"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 100vh;
        }
        
        .block-container {
            max-width: 500px;
            margin: auto;
            padding: 3rem 2.5rem;
            background: rgba(30, 41, 59, 0.7);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* Forms */
        div[data-testid="stForm"] {
            border: none;
            background: transparent;
            padding: 0;
        }
        
        div[data-testid="stTextInput"] > label {
            color: #cbd5e1 !important; 
            font-weight: 500;
        }
        
        div[data-testid="stTextInput"] input {
            background-color: rgba(15, 23, 42, 0.6) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 8px;
            width: 100% !important;
            height: 44px !important;
            padding: 0 1rem !important;
            font-size: 15px !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            outline: none !important;
        }
        div[data-testid="stTextInput"] input::placeholder {
            color: #64748b !important;
        }

        /* Buttons matching the blue-purple gradient */
        div[data-testid="stFormSubmitButton"] > button {
            border: none;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white !important;
            border-radius: 8px;
            padding: 10px 0;
            font-weight: 600;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 14px 0 rgba(139, 92, 246, 0.39);
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
        }
        div[data-testid="stFormSubmitButton"] > button:active {
            transform: translateY(0);
        }

        /* Tabs styling */
        button[data-baseweb="tab"] {
            color: #94a3b8;
            font-weight: 600;
            background: transparent !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #f8fafc;
            border-bottom: 2px solid #8b5cf6 !important;
        }
        
        div[data-testid="stForm"] div[data-testid="stNotification"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<style>.stTabs [data-baseweb='tab'] {font-size: 1rem !important;}</style>", unsafe_allow_html=True)


def load_custom_css():
    st.markdown("""
        <style>
            html, body, [data-testid="stApp"] {
                height: 100%;            
                margin: 0;
                padding: 0;
                background: #0f172a; /* Solid dark slate for main app */
                font-family: 'Inter', 'Segoe UI', sans-serif;
                color: #f8fafc;
            }

            /* Container inside the app */
            .main .block-container {
                max-width: 800px;
                padding-top: 3rem;
                padding-bottom: 5rem;
                background: transparent;
                box-shadow: none;
                border: none;
                backdrop-filter: none;
            }

            .centered-title {
                text-align: center;
                font-size: 38px;
                font-weight: 800;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
                background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtext {
                text-align: center;
                font-size: 17px;
                margin-bottom: 2.5rem;
                color: #cbd5e1;
            }

            /* Styling the feedback and response boxes to be highly visible */
            .question-box, .feedback-box, .answer-box {
                background-color: #1e293b;
                color: #f8fafc;
                padding: 1.25rem 1.5rem;
                border: 1px solid rgba(248, 250, 252, 0.1);
                border-left: 4px solid #3b82f6;
                border-radius: 12px;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
                font-size: 15px;
                line-height: 1.7;
                white-space: pre-wrap;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .question-box { border-left-color: #8b5cf6; }
            .feedback-box { border-left-color: #10b981; }

            .score-badge {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                padding: 8px 16px;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                display: inline-block;
                font-size: 16px;
                box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
            }
                
            footer {
                text-align: center;
                color: #64748b;
                font-size: 14px;
                margin-top: 4rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255,255,255,0.05);
            }

            /* Radio options styling */
            div[data-testid="stRadio"] > label {
                font-size: 1.1rem;
                font-weight: 600;
                color: #f1f5f9;
                margin-bottom: 0.5rem;
            }
            div[data-testid="stRadio"] > div {
                background-color: rgba(255, 255, 255, 0.03); 
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1rem;
                border-radius: 12px;
            }

            /* Main App Text Input / Text Area Formatting */
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {
                background-color: rgba(30, 41, 59, 1) !important;
                color: #f8fafc !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                border-radius: 10px !important;
                padding: 0.75rem 1rem !important;
                font-size: 15px !important;
                transition: all 0.2s ease-in-out !important;
            }

            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {
                color: #64748b !important;
            }

            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stTextArea"] textarea:focus {
                background-color: rgba(30, 41, 59, 1) !important;
                border: 1px solid #3b82f6 !important;
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
            }

            /* Override Streamlit Markdown constraints */
            label, .stMarkdown, p, span, h1, h2, h3, h4 {
                color: #f1f5f9;
            }

            /* Primary Action Button (Main App) */
            div[data-testid="stButton"] > button {
                border: none;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                color: white !important;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                transition: all 0.2s ease;
                box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3);
            }
            div[data-testid="stButton"] > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
            }
            
            /* File uploader text */
            .stFileUploader > div > div > small {
                color: #cbd5e1 !important;
            }

        </style>
        """, unsafe_allow_html=True)


st.set_page_config(page_title="AI Interview Coach", layout="wide", page_icon="🎓")
load_custom_css()

if 'mode' not in st.session_state:
    st.session_state.mode = 'login'

if st.session_state.mode == 'login':
    apply_login_styles()
    
    login_result = show_login()

    if login_result is True or login_result == 'demo':
        st.session_state.mode = 'app'
        st.rerun()


elif st.session_state.mode == 'app':
      
    st.markdown("<h1 class='centered-title'>AI Interview Coach</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Practice your answers. Get AI feedback. Improve your interview skills.</div>", unsafe_allow_html=True)

    role = st.text_input("Enter the job role you're preparing for: (Data Analyst, SDE)")

    if role:
        if 'interview_question' not in st.session_state:
            with st.spinner("Generating interview question..."):
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

