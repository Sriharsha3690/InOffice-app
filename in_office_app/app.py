import streamlit as st

st.set_page_config(page_title="InOffice", layout="wide")

st.title("🏢 InOffice - Attendance Dashboard")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Mark Attendance", "Manage Employees", "Reports"])

if menu == "Dashboard":
    st.subheader("📊 Dashboard Overview")
    st.write("This is where the summary will appear.")

elif menu == "Mark Attendance":
    st.subheader("📝 Mark Attendance")
    st.write("Attendance marking interface here.")

elif menu == "Manage Employees":
    st.subheader("👥 Manage Employees")
    st.write("Add/Edit/Delete Employees")

elif menu == "Reports":
    st.subheader("📈 Reports")
    st.write("Export monthly reports here.")
