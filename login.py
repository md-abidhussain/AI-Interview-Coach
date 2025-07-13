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

# Styled login form
def show_login():
    st.markdown("Login or Register to Continue")
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("👤 Username", key="login_user")
        password = st.text_input("🔒 Password", type="password", key="login_pass")
        if st.button("Login"):
            if check_credentials(username, password):
             st.success(f"✅ Welcome, {username}!")
             return True
            else:
                st.error("❌ Invalid credentials")
            return False

    with tab2:
        new_user = st.text_input("👤 Create Username", key="signup_user")
        new_pass = st.text_input("🔒 Create Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if save_user(new_user, new_pass):
                st.success("✅ Account created. Please login.")
            else:
                st.warning("⚠️ Username already exists.")

    return False
