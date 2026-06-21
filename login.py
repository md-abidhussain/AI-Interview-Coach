import streamlit as st
import os
import bcrypt
import re
import psycopg2

def validate_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        try:
            db_url = st.secrets["DATABASE_URL"]
        except KeyError:
            pass
    return db_url

def init_db(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Database init error: {e}")
        conn.rollback()

def save_user(username, password):
    username = username.strip()
    if not validate_username(username):
        return "invalid"
    
    db_url = get_db_connection()
    if not db_url:
        return "Database error: DATABASE_URL is not set"
        
    conn = None
    try:
        conn = psycopg2.connect(db_url)
        init_db(conn)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return "exists"
            
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        cursor.close()
        conn.close()
        return "success"
    except Exception as e:
        print(f"PostgreSQL write error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return f"Database error: {str(e)}"

def check_credentials(username, password):
    username = username.strip()
    if not username:
        return False
    
    db_url = get_db_connection()
    if not db_url:
        raise ValueError("DATABASE_URL is missing! Please configure it in your secrets.")
        
    conn = None
    try:
        conn = psycopg2.connect(db_url)
        init_db(conn)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            return False
            
        stored_val = row[0]
        try:
            if stored_val.startswith("$2"):
                return bcrypt.checkpw(password.encode('utf-8'), stored_val.encode('utf-8'))
        except Exception:
            pass
        return stored_val == password
    except Exception as e:
        print(f"PostgreSQL read error: {e}")
        if conn:
            conn.close()
        raise e

def show_login():
    db_url = get_db_connection()
    if not db_url:
        st.error("🔑 DATABASE_URL is missing! Please configure your PostgreSQL database URL in your local .env or Streamlit App Secrets.")
        st.stop()

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
                try:
                    if check_credentials(username, password):
                        st.session_state.login_failed = False
                        st.success(f"Welcome back, {username}!")
                        return True
                    else:
                        st.session_state.login_failed = True
                        st.error("Invalid credentials. Please try again or create an account.")
                except Exception as e:
                    st.error(f"❌ Database error: {e}")

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
                    elif status.startswith("Database error:"):
                        st.error(f"❌ {status}")
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