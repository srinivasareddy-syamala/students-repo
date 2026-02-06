import streamlit as st
import sqlite3
import pandas as pd

# ------------------ Database Connection ------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ Create Table ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

# ------------------ Sidebar Menu ------------------
st.sidebar.title("📚 Student Management")
menu = st.sidebar.radio(
    "Select an option",
    ["Insert Student Details", "View Student Details"]
)

# ------------------ Insert Student Details ------------------
if menu == "Insert Student Details":
    st.title("➕ Insert Student Details")

    name = st.text_input("Student Name")
    roll_no = st.text_input("Roll Number")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")

    if st.button("Save Student"):
        if name and roll_no and course:
            cursor.execute(
                "INSERT INTO students (name, roll_no, age, course) VALUES (?, ?, ?, ?)",
                (name, roll_no, age, course)
            )
            conn.commit()
            st.success("✅ Student details saved successfully!")
        else:
            st.warning("⚠️ Please fill all required fields")

# ------------------ View Student Details ------------------
elif menu == "View Student Details":
    st.title("📄 Student Details")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(
            data,
            columns=["ID", "Name", "Roll No", "Age", "Course"]
        )
        st.dataframe(df)
    else:
        st.info("ℹ️ No student records found")
