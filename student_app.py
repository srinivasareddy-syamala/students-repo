import streamlit as st
import sqlite3
import pandas as pd

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="centered"
)

# ------------------ Database Connection ------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ Create Table ONLY IF NOT EXISTS ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL UNIQUE,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

# ------------------ Sidebar Menu ------------------
st.sidebar.title("🎓 Student Management")
menu = st.sidebar.radio(
    "Choose Option",
    ["Insert Student Details", "View Student Details"]
)

# ================== INSERT STUDENT ==================
if menu == "Insert Student Details":
    st.title("➕ Insert Student Details")

    name = st.text_input("Student Name")
    roll_no = st.text_input("Roll Number")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    course = st.text_input("Course")

    if st.button("Save Student"):
        if not name or not roll_no or not course:
            st.warning("⚠️ Please fill all required fields")
        else:
            try:
                cursor.execute(
                    "INSERT INTO students (name, roll_no, age, course) VALUES (?, ?, ?, ?)",
                    (name, roll_no, age, course)
                )
                conn.commit()
                st.success("✅ Student details saved successfully!")
            except sqlite3.IntegrityError:
                st.error("❌ Duplicate Roll Number! Roll number must be unique.")

# ================== VIEW STUDENTS ==================
elif menu == "View Student Details":
    st.title("📄 Student Details")

    df = pd.read_sql_query("SELECT * FROM students", conn)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("ℹ️ No student records found")
