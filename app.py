import streamlit as st
import re
from pymongo import MongoClient

# ------------------------------------------------------------
# MUST BE FIRST
# ------------------------------------------------------------
st.set_page_config(page_title="Student Feedback Form", layout="centered")

# ------------------------------------------------------------
# REMOVE SEARCH BAR
# ------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppSearch"] { display: none !important; }
h1 { text-align:center !important; }
.subtitle { text-align:center; color:#888; font-size:18px; margin-top:-10px; }
.form-container {
    padding:25px; border-radius:15px;
    background-color:rgba(255,255,255,0.05);
    box-shadow:0 4px 20px rgba(0,0,0,0.15);
}
.stTextInput > div > div > input,
.stTextArea > div > textarea {
    background-color:transparent !important;
    color:inherit !important;
    border:1.5px solid #555 !important;
    border-radius:10px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# MONGODB CONNECTION
# ------------------------------------------------------------
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["feedbackFormDB"]      # database
feedback_col = db["feedbacks"]     # collection

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown("<h1>📝 Student Feedback Form</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your feedback helps us improve! 🌱</p>", unsafe_allow_html=True)

# ------------------------------------------------------------
# FORM
# ------------------------------------------------------------
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("feedback_form", clear_on_submit=True):

        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number")
        email = st.text_input("Email Address")

        rating = st.slider("Rate Your Experience (1 = Poor, 5 = Excellent)", 1, 5, 3)

        comments = st.text_area("Additional Comments (Optional)")

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:

            # -------------------------------------
            # 1. EMAIL VALIDATION
            # -------------------------------------
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("❌ Please enter a valid email address.")
            
            # -------------------------------------
            # 2. CHECK FOR DUPLICATE ROLL NUMBER
            # -------------------------------------
            elif feedback_col.find_one({"roll": roll}):
                st.error("❌ This Roll Number already submitted feedback. Only one submission allowed.")

            # -------------------------------------
            # 3. CHECK FOR DUPLICATE EMAIL
            # -------------------------------------
            elif feedback_col.find_one({"email": email}):
                st.error("❌ This Email ID already submitted feedback. Only one submission allowed.")

            else:
                # -------------------------------------
                # 4. SAVE FEEDBACK
                # -------------------------------------
                feedback_col.insert_one({
                    "name": name,
                    "roll": roll,
                    "email": email,
                    "rating": rating,
                    "comments": comments
                })
                st.success("✅ Thank you! Your feedback has been submitted.")

    st.markdown('</div>', unsafe_allow_html=True)
