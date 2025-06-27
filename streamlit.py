import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import openai
import os

# --- Configuration ---
OPENAI_API_KEY = "your-openai-api-key"  # Replace with your actual key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- Streamlit UI ---
st.set_page_config(page_title="AI KYC Concierge", layout="centered")
st.title("🤖 Customer Experience AI for KYC")
st.write("Welcome to your AI onboarding concierge. Let's verify your identity and get started.")

# --- Upload Document ---
st.header("1. Upload Identification Document")
id_doc = st.file_uploader("Upload your passport, NRIC, or government-issued ID (PDF or image)", type=["pdf", "png", "jpg", "jpeg"])

if id_doc:
    st.success("Document uploaded successfully. Verifying... (mocked)")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Check_mark_9x9.svg/2048px-Check_mark_9x9.svg.png", width=50)
    st.write("✅ Face and document matched. Proceeding to next step.")

# --- Basic Info Form ---
st.header("2. Fill in Basic Information")
full_name = st.text_input("Full Name")
country = st.selectbox("Country of Residence", ["Singapore", "Malaysia", "Hong Kong", "Other"])
source_of_wealth = st.text_area("Briefly describe your Source of Wealth")

# --- Chatbot Component ---
st.header("3. Ask Me Anything About KYC")
st.write("Got a question about what documents to upload or how this works? Ask below.")

openai.api_key = "your-openai-key"  # replace with your actual key

# Chatbot memory and interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Your Question", key="chat")

if user_input:
    st.session_state.chat_history.append(f"User: {user_input}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful KYC onboarding assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    answer = response["choices"][0]["message"]["content"]
    st.session_state.chat_history.append(f"AI Concierge: {answer}")
    st.write("**AI Concierge:**", answer)

# --- Final Submit ---
st.header("4. Complete Onboarding")
if st.button("Submit for Verification"):
    if id_doc and full_name and source_of_wealth:
        st.success(f"✅ Thank you {full_name}, your information has been submitted for review.")
    else:
        st.error("Please complete all fields and upload a valid ID document before submitting.")
