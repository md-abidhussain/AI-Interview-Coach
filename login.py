import streamlit as st
import os
import bcrypt
import csv
import re

USER_CSV = "users.csv"

def validate_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def save_user(username, password):
    username = username.strip()
    if not validate_username(username):
        return "invalid"
    
    try:
        if os.path.exists(USER_CSV):
            with open(USER_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[0].strip() == username:
                        return "exists"
                        
        file_exists = os.path.exists(USER_CSV)
        with open(USER_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["username", "password"])
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            writer.writerow([username, hashed_pw])
        return "success"
    except Exception as e:
        print(f"Database write error: {e}")
        return "error"

def check_credentials(username, password):
    username = username.strip()
    if not username or not os.path.exists(USER_CSV):
        return False
    
    try:
        with open(USER_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and row[0].strip() == username:
                    stored_val = row[1]
                    try:
                        if stored_val.startswith("$2"):
                            return bcrypt.checkpw(password.encode('utf-8'), stored_val.encode('utf-8'))
                    except Exception:
                        pass
                    return stored_val == password
    except Exception as e:
        print(f"Database read error: {e}")
    return False

def show_login():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem; background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Interview Coach</h1>
            <p style="font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">Master your interview skills with real-time AI feedback and personalized questions.</p>
        </div>
    """, unsafe_allow_html=True)

    if 'login_failed' not in st.session_state:
        st.session_state.login_failed = False

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
                    status = save_user(new_user, new_pass)
                    if status == "success":
                        st.success("Account created successfully! You can now log in.")
                        st.session_state.login_failed = False
                    elif status == "exists":
                        st.warning("Username already exists. Please choose another one.")
                    elif status == "invalid":
                        st.warning("⚠️ Username must be 3-20 characters long and contain only letters, numbers, and underscores (no spaces or slashes).")
                    else:
                        st.error("❌ A database error occurred. Please try again.")
                else:
                    st.warning("Please fill in both fields.")

    st.markdown("<div style='margin-top: 1.5rem; text-align: center; color: #64748b;'>— OR —</div>", unsafe_allow_html=True)
    st.write("")
    
    skip_label = "Skip for Now (Continue as Guest)" if st.session_state.login_failed else "Continue as Guest"
    if st.button(skip_label, use_container_width=True, type="secondary"):
        st.session_state.login_failed = False
        return 'demo'

    return False