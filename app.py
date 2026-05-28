import streamlit as st
import ollama
import json
import os
from datetime import datetime

# ---------------- PAGE ---------------- #

st.set_page_config(
    page_title="Mentor AI",
    page_icon="🧠",
    layout="centered"
)

# ---------------- STYLE ---------------- #

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: white;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    background-color: #6C63FF;
    color: white;
    border: none;
}

textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MEMORY ---------------- #

MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

with open(MEMORY_FILE, "r") as f:
    memory = json.load(f)

# ---------------- TITLE ---------------- #

st.title("🧠 Mentor AI")
st.caption("Your Personal Wise Mentor")

# ---------------- INPUTS ---------------- #

schedule = st.text_area(
    "📅 Your Schedule",
    height=180,
    placeholder="""7am wake up
9am-4pm college
6pm gym
8pm gaming
12am sleep"""
)

ideas = st.text_area(
    "💡 Your Goals / Ideas",
    height=180,
    placeholder="""learn cybersecurity
make projects
improve discipline"""
)

checkin = st.text_area(
    "📝 Daily Check-In",
    height=120,
    placeholder="What did you actually do today?"
)

# ---------------- SAVE IDEAS ---------------- #

if st.button("💾 Save Ideas"):

    entry = {
        "date": str(datetime.now()),
        "ideas": ideas
    }

    memory.append(entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

    st.success("Ideas Saved")

# ---------------- SHOW OLD IDEAS ---------------- #

old_ideas = ""

if len(memory) > 0:

    st.subheader("🕘 Previous Ideas")

    for item in reversed(memory[-5:]):

        st.info(item["ideas"])

        old_ideas += item["ideas"] + "\n"

# ---------------- AI RESPONSE ---------------- #

if st.button("🧠 Get Mentor Advice"):

    prompt = f"""
You are NOT a generic AI assistant.

You are a wise older mentor guiding a younger person realistically.

IMPORTANT:
- Reply ONLY point wise
- Be practical
- Be observant
- Detect wasted time
- Suggest meaningful activities
- Avoid generic motivation
- Refer to old ideas naturally
- Keep the user's schedule mostly unchanged

FORMAT:

# 1. Deep Observations
-

# 2. Hidden Time Opportunities
-

# 3. High Value Activities
-

# 4. Things You Mentioned Before
-

# 5. Warnings
-

# 6. Mentor Advice
-

USER SCHEDULE:
{schedule}

USER GOALS:
{ideas}

OLD MEMORIES:
{old_ideas}

DAILY CHECK-IN:
{checkin}
"""

    with st.spinner("Mentor AI is thinking deeply..."):

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        reply = response["message"]["content"]

        st.subheader("🧠 Mentor Response")

        st.write(reply)

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("Built with Streamlit + Ollama")
