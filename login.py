import streamlit as st
import pandas as pd
import os

USER_CSV = "users.csv"

# Create CSV if not exists
if not os.path.exists(USER_CSV):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_CSV, index=False)

# Save new user
def save_user(username, password):
    df = pd.read_csv(USER_CSV)
    if username in df["username"].values:
        return False
    new_user = pd.DataFrame({"username": [username], "password": [password]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_CSV, index=False)
    return True

# Check login
def check_credentials(username, password):
    df = pd.read_csv(USER_CSV)
    return ((df["username"] == username) & (df["password"] == password)).any()
    

def show_login():
    # Landing Page Hero Section
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem; background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Interview Coach</h1>
            <p style="font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">Master your interview skills with real-time AI feedback and personalized questions.</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize a session state for showing the skip button on failure
    if 'login_failed' not in st.session_state:
        st.session_state.login_failed = False

    # Tabs for Login / Sign Up
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            st.markdown("<h3 style='color: #f1f5f9; margin-bottom: 1rem;'>Welcome Back</h3>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.write("") 
            
            submitted = st.form_submit_button("Log In", use_container_width=True)
            if submitted:
                if check_credentials(username, password):
                    st.session_state.login_failed = False
                    st.success(f"Welcome back, {username}!")
                    return True
                else:
                    st.session_state.login_failed = True
                    st.error("Invalid credentials. Please try again or create an account.")

    with tab2:
        with st.form("signup_form"):
            st.markdown("<h3 style='color: #f1f5f9; margin-bottom: 1rem;'>Create an Account</h3>", unsafe_allow_html=True)
            new_user = st.text_input("Choose a Username", placeholder="e.g. tech_ninja")
            new_pass = st.text_input("Create a secure Password", type="password", placeholder="Minimum 8 characters")
            st.write("") 
            submitted_signup = st.form_submit_button("Create Account", use_container_width=True)
            if submitted_signup:
                if len(new_user) > 0 and len(new_pass) > 0:
                    if save_user(new_user, new_pass):
                        st.success("Account created successfully! You can now log in.")
                        st.session_state.login_failed = False
                    else:
                        st.warning("Username already exists. Please choose another one.")
                else:
                    st.warning("Please fill in both fields.")

    st.markdown("<div style='margin-top: 1.5rem; text-align: center; color: #64748b;'>— OR —</div>", unsafe_allow_html=True)
    st.write("")
    
    # "Skip" button behavior
    skip_label = "Skip for Now (Continue as Guest)" if st.session_state.login_failed else "Continue as Guest"
    if st.button(skip_label, use_container_width=True, type="secondary"):
        st.session_state.login_failed = False
        return 'demo'

    return False