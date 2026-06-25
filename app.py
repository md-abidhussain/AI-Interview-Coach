import streamlit as st
from login import show_login
from gemini_module import get_feedback, generate_question
from whisper_transcriber import transcribe_audio_file
from mic_input import record_and_transcribe

def apply_login_styles():
    st.markdown("""
    <style>
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

        div[data-testid="stForm"] {
            border: none;
            background: transparent;
            padding: 0;
        }
        
        div[data-testid="stTextInput"] > label {
            color: #cbd5e1 !important; 
            font-weight: 500;
        }
        
        div[data-baseweb="input"], div[data-baseweb="textarea"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border-color: #ff4b4b !important;
            box-shadow: 0 0 0 1px #ff4b4b !important;
        }
        div[data-baseweb="base-input"] {
            background-color: transparent !important;
            border: none !important;
        }
        div[data-baseweb="base-input"] button {
            background-color: transparent !important;
            border: none !important;
        }
        div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
            background: transparent !important;
            color: #f8fafc !important;
            border: none !important;
            box-shadow: none !important;
            width: 100% !important;
            font-size: 15px !important;
        }
        div[data-baseweb="input"] input {
            height: 44px !important;
            padding: 0 1rem !important;
        }

        div[data-testid="stFormSubmitButton"] > button {
            border: none;
            background: linear-gradient(135deg, #3b82f6 0%, #ff4b4b 100%);
            color: white !important;
            border-radius: 8px;
            padding: 10px 0;
            font-weight: 600;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 14px 0 rgba(255, 75, 75, 0.39);
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
        }
        div[data-testid="stFormSubmitButton"] > button:active {
            transform: translateY(0);
        }

        button[data-baseweb="tab"] {
            color: #94a3b8;
            font-weight: 600;
            background: transparent !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #f8fafc;
            border-bottom: 2px solid #ff4b4b !important;
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
                background: #0f172a;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                color: #f8fafc;
            }

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
                background: -webkit-linear-gradient(45deg, #3b82f6, #ff4b4b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtext {
                text-align: center;
                font-size: 17px;
                margin-bottom: 2.5rem;
                color: #cbd5e1;
            }

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
            .question-box { border-left-color: #ff4b4b; }
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

            div[data-baseweb="input"], div[data-baseweb="textarea"] {
                background-color: #1e293b !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                border-radius: 10px !important;
                transition: all 0.2s ease-in-out !important;
                width: 100% !important;
            }
            div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 1px #ff4b4b !important;
            }
            div[data-baseweb="base-input"] {
                background-color: transparent !important;
                border: none !important;
            }
            div[data-baseweb="base-input"] button {
                background-color: transparent !important;
                border: none !important;
            }
            div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
                background: transparent !important;
                color: #f8fafc !important;
                border: none !important;
                box-shadow: none !important;
                font-size: 15px !important;
                width: 100% !important;
            }
            div[data-baseweb="input"] input {
                padding: 0.75rem 1rem !important;
                height: 44px !important;
            }
            div[data-baseweb="textarea"] textarea {
                padding: 0.75rem 1rem !important;
            }

            label, .stMarkdown, p, span, h1, h2, h3, h4 {
                color: #f1f5f9;
            }

            div[data-testid="stButton"] > button {
                border: none;
                background: linear-gradient(135deg, #3b82f6 0%, #ff4b4b 100%);
                color: white !important;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                transition: all 0.2s ease;
                box-shadow: 0 4px 14px rgba(255, 75, 75, 0.3);
            }
            div[data-testid="stButton"] > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
            }
            
            .stFileUploader > div > div > small {
                color: #cbd5e1 !important;
            }

        </style>
        """, unsafe_allow_html=True)

st.set_page_config(page_title="AI Interview Coach", layout="wide")
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
    with st.sidebar:
        st.markdown("<h3 style='color: #cbd5e1;'>Session Management</h3>", unsafe_allow_html=True)
        if st.button("Log Out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
      
    st.markdown("<h1 class='centered-title'>AI Interview Coach</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Practice your answers. Get AI feedback. Improve your interview skills.</div>", unsafe_allow_html=True)

    role = st.text_input("Enter the job role you're preparing for: (Data Analyst, SDE)")

    if role:
        if 'interview_question' not in st.session_state or st.session_state.get('current_role') != role:
            st.session_state.current_role = role
            with st.spinner("Generating interview question..."):
                try:
                    st.session_state.interview_question = generate_question(role)
                except Exception as e:
                    st.session_state.interview_question = f"Error: {e}"
        
        st.markdown("### Gemini's Interview Question")
        if st.session_state.interview_question.startswith("Error:"):
            st.error(st.session_state.interview_question)
            if st.button("Try Again"):
                if 'interview_question' in st.session_state:
                    del st.session_state.interview_question
                st.rerun()
        else:
            st.markdown(f"<div class='question-box'>{st.session_state.interview_question}</div>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Next Question"):
                    if 'interview_question' in st.session_state:
                        del st.session_state.interview_question
                    st.rerun()

        option = st.radio("Choose how you'll answer:", ["Text Input", "Upload Audio", "Speak Live (Mic)"])

        if option == "Text Input":
            user_input = st.text_area("Type your answer:")
            if st.button("Submit Text Answer"):
                if user_input:
                    with st.spinner("Gemini is analyzing your answer..."):
                        try:
                            feedback, score = get_feedback(answer=user_input, role=role, mode="text")
                            st.markdown("### Transcribed Answer")
                            st.markdown(f"<div class='answer-box'>{user_input}</div>", unsafe_allow_html=True)
                            st.markdown("### Gemini's Feedback")
                            st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                            st.markdown("### Your AI Score")
                            st.markdown(f"<div class='score-badge'>Score: {score}/10</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please enter your answer first!")

        elif option == "Upload Audio":
            audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])
            if audio_file and st.button("Submit Audio"):
                with st.spinner("Transcribing your voice..."):
                    try:
                        transcribed = transcribe_audio_file(audio_file)
                        st.success("Transcription complete!")
                        st.markdown("### Transcribed Answer")
                        st.markdown(f"<div class='answer-box'>{transcribed}</div>", unsafe_allow_html=True)
                        with st.spinner("Evaluating answer..."):
                            feedback, score = get_feedback(answer=transcribed, role=role, mode="voice")
                        st.markdown("### Gemini's Feedback")
                        st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                        st.markdown("### Your AI Score")
                        st.markdown(f"<div class='score-badge'>Score: {score}/10</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif option == "Speak Live (Mic)":
            if st.button("Start Recording"):
                with st.spinner("Listening..."):
                    result = record_and_transcribe()
                st.markdown("### Transcribed Answer")
                st.markdown(f"<div class='answer-box'>{result}</div>", unsafe_allow_html=True)
                if result and not result.startswith("Error:") and not result.startswith("Live microphone"):
                    with st.spinner("Evaluating your response..."):
                        try:
                            feedback, score = get_feedback(answer=result, role=role, mode="voice")
                            st.markdown("### Gemini's Feedback")
                            st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
                            st.markdown("### Your AI Score")
                            st.markdown(f"<div class='score-badge'>Score: {score}/10</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.error(result)

        st.markdown("""
        <footer>
        Created by <strong>Mohd Abid Hussain</strong> | CSE @ Jamia Hamdard
        </footer>
        """, unsafe_allow_html=True)
