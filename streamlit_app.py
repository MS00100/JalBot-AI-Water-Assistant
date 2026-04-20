import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid
import re

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="JalBot",
    page_icon="💧",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------
st.title("💧 JalBot: Smart Water Data Assistant")
st.markdown("Ask anything like **'rainfall in indore'**, **'groundwater in delhi'**")

# -------------------------------
# RESET BUTTON
# -------------------------------
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------------
# CHAT MEMORY
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# DISPLAY CHAT
# -------------------------------
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "chart":
            st.plotly_chart(msg["content"], key=f"chart_{i}", use_container_width=True)

# -------------------------------
# NLP FUNCTIONS
# -------------------------------
def extract_location(prompt):
    prompt = prompt.lower()

    match = re.search(r"in ([a-zA-Z ]+)", prompt)
    if match:
        return match.group(1).strip()

    words = prompt.split()
    return words[-1]


def extract_intent(prompt):
    prompt = prompt.lower()

    if "rain" in prompt:
        return "rainfall"
    elif "ground" in prompt or "level" in prompt:
        return "groundwater"
    elif "trend" in prompt:
        return "trend"
    else:
        return "unknown"


# -------------------------------
# FAKE DATA GENERATOR (SMART)
# -------------------------------
def generate_fake_data(location):
    np.random.seed(abs(hash(location)) % (10**6))

    years = [2018, 2019, 2020, 2021, 2022]
    rainfall = np.random.randint(600, 1200, 5)
    groundwater = np.random.randint(10, 30, 5)

    return years, rainfall, groundwater


# -------------------------------
# RESPONSE ENGINE
# -------------------------------
def generate_response(prompt):
    intent = extract_intent(prompt)
    location = extract_location(prompt)

    if "hello" in prompt or "hi" in prompt:
        return {"type": "text", "content": "Hello! I am JalBot 🤖"}

    years, rainfall, groundwater = generate_fake_data(location)

    if intent == "rainfall":
        df = pd.DataFrame({"Year": years, "Rainfall": rainfall})
        fig = px.line(df, x="Year", y="Rainfall",
                      title=f"🌧️ Rainfall Trend in {location.title()}")
        return {"type": "chart", "content": fig}

    elif intent == "groundwater":
        df = pd.DataFrame({"Year": years, "Groundwater": groundwater})
        fig = px.line(df, x="Year", y="Groundwater",
                      title=f"💧 Groundwater Trend in {location.title()}")
        return {"type": "chart", "content": fig}

    elif intent == "trend":
        df = pd.DataFrame({"Year": years, "Value": groundwater})
        fig = px.line(df, x="Year", y="Value",
                      title=f"📈 Trend in {location.title()}")
        return {"type": "chart", "content": fig}

    else:
        return {"type": "text", "content": f"I detected location **{location.title()}**, please ask about rainfall or groundwater."}


# -------------------------------
# INPUT
# -------------------------------
prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "type": "text"
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    response = generate_response(prompt)

    with st.chat_message("assistant"):
        if response["type"] == "text":
            st.markdown(response["content"])
        else:
            st.plotly_chart(response["content"], key=str(uuid.uuid4()), use_container_width=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response["content"],
        "type": response["type"]
    })

# -------------------------------
# SIDEBAR (PREMIUM UI)
# -------------------------------
with st.sidebar:
    st.header("⚙️ JalBot Control Panel")

    st.markdown("### 💡 Main Features")
    st.markdown("""
    - 💬 Natural Language Queries  
    - 🌍 Works for ANY Location  
    - 📊 Rainfall & Groundwater Trends  
    - 🧠 Smart NLP Understanding  
    - ⚡ Fast Response  
    """)

    st.markdown("---")

    st.markdown("### 🧪 Try These Queries")
    st.code("rainfall in bhopal")
    st.code("groundwater in indore")
    st.code("trend in delhi")
    st.code("rainfall in mumbai")

    st.markdown("---")

    st.markdown("### 🎯 Select Quick Location")
    location_select = st.selectbox(
        "Choose a city",
        ["Bhopal", "Indore", "Delhi", "Mumbai"]
    )

    if st.button("Show Rainfall"):
        st.session_state.messages.append({
            "role": "user",
            "content": f"rainfall in {location_select}",
            "type": "text"
        })
        st.rerun()

    st.markdown("---")

    st.markdown("### 👨‍💻 Project Info")
    st.write("JalBot - AI Water Assistant")
    st.write("Developed by Team JalBot")

    st.markdown("---")

    st.success("🚀 AI-like chatbot (No API required)")