import streamlit as st
from datetime import datetime

# -------------- Helpers --------------
FAQ = {
    "what is kyc": "KYC stands for Know Your Customer. It's how we verify identity to protect you and the financial institution.",
    "what documents": "Typically: government ID (passport/NRIC), proof of address (utility bill/bank stmt <3 months), and source-of-wealth evidence if applicable.",
    "nric": "NRIC is accepted. Please make sure the image is clear and all four corners are visible.",
    "passport": "Passports are accepted. Upload the photo page with MRZ visible.",
    "proof of address": "Acceptable proofs: utility bill, bank statement, telco bill issued in the last 3 months, showing your full name and address.",
    "source of wealth": "Examples: employment income (payslips), business income (financials), investments (broker statements), inheritance (legal docs), or property sale (sale & proceeds).",
    "how long": "Typical KYC review time is 1–2 business days after submission. If clarification is needed, we’ll contact you.",
    "data privacy": "Your documents are encrypted at rest and in transit. They’re used only for compliance verification.",
    "why rejected": "Common reasons: blurry/obscured images, expired documents, mismatched names/addresses, or missing SoW evidence."
}

def get_bot_reply(text: str) -> str:
    """Very simple rule-based reply; falls back to a friendly default."""
    q = (text or "").lower().strip()
    # quick keyword routing
    for key, answer in FAQ.items():
        if key in q:
            return answer
    if "hello" in q or "hi" in q:
        return "Hi! I can help with documents, proofs, timelines, and privacy. Ask me anything about KYC."
    if "country" in q or "singapore" in q:
        return "For Singapore, NRIC/FIN or passport works. Proof of address must be within the last 3 months."
    if "help" in q:
        return "Sure—tell me what you’re trying to submit and I’ll list what’s needed."
    # default
    return (
        "Thanks! I’m a simple demo concierge. Ask about: required documents, proof of address, "
        "source of wealth, timelines, data privacy, or common rejection reasons."
    )

def chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

# -------------- App UI --------------
st.set_page_config(page_title="AI KYC Concierge (Demo)", layout="centered")
st.title("🤖 Customer Experience KYC Concierge — Demo (No API)")

st.info("This demo is fully local and **does not call any external APIs**. Responses are hard-coded.")

# --- 1) Upload ID ---
st.header("1) Upload Identification")
id_doc = st.file_uploader(
    "Upload your passport/NRIC/ID (PDF or image)", type=["pdf", "png", "jpg", "jpeg"]
)
if id_doc:
    st.success("Document uploaded. Running mock checks…")
    st.caption("• Blur check: Pass • Expiry check: Pass • MRZ present: Pass (mock)")
    st.write("✅ Face and document matched. Proceed to Step 2.")

# --- 2) Basic Info ---
st.header("2) Basic Information")
col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name")
with col2:
    country = st.selectbox("Country of Residence", ["Singapore", "Malaysia", "Hong Kong", "Other"])
source_of_wealth = st.text_area("Briefly describe your Source of Wealth")

# --- 3) Concierge Chat (hard-coded logic) ---
st.header("3) Ask Me Anything About KYC")
if "chat" not in st.session_state:
    st.session_state.chat = []

# Show history
for role, msg in st.session_state.chat:
    chat_message(role, msg)

# Chat input (Streamlit’s chat UI)
user_q = st.chat_input("Type your question...")
if user_q:
    st.session_state.chat.append(("user", user_q))
    chat_message("user", user_q)

    bot_a = get_bot_reply(user_q)
    st.session_state.chat.append(("assistant", bot_a))
    chat_message("assistant", bot_a)

# --- 4) Submit ---
st.header("4) Submit for Verification")
if st.button("Submit"):
    if not id_doc:
        st.error("Please upload a valid ID document.")
    elif not full_name or not source_of_wealth:
        st.error("Please complete your name and source of wealth.")
    else:
        ref = f"KYC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        st.success(f"✅ Thanks, {full_name}! Your application has been submitted. Reference: **{ref}**")
        st.caption("This is a demo. No data leaves your browser/session.")

