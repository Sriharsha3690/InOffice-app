# Update app.py to support basic user accounts with limited access and mark holidays

app_with_admin_user = """
import streamlit as st
import sqlite3
from datetime import datetime

# Hardcoded accounts
ACCOUNTS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
}

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Login function
def login():
    st.title("InOffice Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            account = ACCOUNTS.get(username)
            if account and account["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = account["role"]
                st.success("Login successful.")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")

# Logout function
def logout():
    for key in ["logged_in", "username", "role"]:
        st.session_state[key] = False if key == "logged_in" else ""
    st.success("Logged out.")
    st.experimental_rerun()

# Admin dashboard
def admin_dashboard():
    st.title("InOffice Dashboard - Admin")
    st.write(f"Welcome, {st.session_state.username} 👋")
    st.markdown("### Mark Holidays")
    date = st.date_input("Select Date")
    reason = st.text_input("Reason (e.g. Sunday, Festival)")
    if st.button("Add Holiday"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO holidays (date, reason) VALUES (?, ?)", (str(date), reason))
            conn.commit()
            st.success(f"Holiday on {date} added.")
        except sqlite3.IntegrityError:
            st.warning("Holiday already exists for this date.")
        conn.close()

# User dashboard
def user_dashboard():
    st.title("InOffice Dashboard - User")
    st.write(f"Welcome, {st.session_state.username} 👋")
    st.markdown("### Mark Attendance")
    today = datetime.now().date()
    if st.button("Mark Present for Today"):
        st.success(f"Attendance marked for {today} ✔️")

# App router
def run_app():
    init_db()
    if not st.session_state.logged_in:
        login()
    else:
        if st.session_state.role == "admin":
            admin_dashboard()
        else:
            user_dashboard()
        st.markdown("---")
        if st.button("Logout"):
            logout()

run_app()
"""

# Write the updated app.py
project_path = "/mnt/data/in_office_app"
with open(os.path.join(project_path, "app.py"), "w") as f:
    f.write(app_with_admin_user.strip())

# Regenerate ZIP with new app.py
zip_path = "/mnt/data/in_office_app.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    for root, dirs, files in os.walk(project_path):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, "/mnt/data")
            zipf.write(full_path, arcname=arcname)

zip_path
