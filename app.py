import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="AI Communication Generator", page_icon="✉️")

# ---------- UI HEADER ---------- #
st.markdown("<h1 style='text-align:center;color:#4CAF50;'>✉️ AI Email & Letter Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart • Fast • Professional</p>", unsafe_allow_html=True)
st.divider()

# ---------- INPUTS ---------- #
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Your Name")
    recipient_name = st.text_input("📨 Recipient Name (optional)")

with col2:
    format_type = st.radio("📄 Format", ["Email", "Formal Letter"])
    language = st.selectbox("🌐 Language", ["English", "Hindi", "Telugu"])

email_type = st.selectbox("📌 Type", [
    "Leave Request",
    "Apology",
    "Job Request",
    "Complaint",
    "General"
])

tone = st.selectbox("🎯 Tone", ["Professional", "Friendly", "Formal", "Very Polite"])

length = st.selectbox("📏 Length", [
    "Very Short (2 lines)",
    "Short",
    "Medium",
    "Long"
])

greeting_style = st.selectbox("🙏 Greeting Style", ["Respected", "Dear", "Hello"])
closing_style = st.selectbox("✍️ Closing Style", ["Yours sincerely", "Regards", "Thank you"])

# ---------- SUGGESTIONS ---------- #
suggestions = {
    "Leave Request": ["Fever", "Family function", "Personal work"],
    "Apology": ["Late submission", "Missed meeting"],
    "Job Request": ["Applying for internship", "Request for job opening"],
    "Complaint": ["Poor service", "Product issue"],
    "General": ["Meeting request", "Follow-up"]
}

reason = st.selectbox("💡 Select Reason", suggestions[email_type])
custom_reason = st.text_input("✏️ Or type your own reason")
final_reason = custom_reason if custom_reason else reason

# ---------- EXTRA FIELDS ---------- #
from_date = st.date_input("📅 From Date (optional)")
to_date = st.date_input("📅 To Date (optional)")
days = st.number_input("📆 Number of Days (optional)", min_value=0)

company = st.text_input("🏢 Company Name (optional)")
role = st.text_input("💼 Job Role (optional)")

place = st.text_input("📍 Place (optional)")

st.divider()

# ---------- GENERATE FUNCTION ---------- #
def generate_email():
    prompt = f"""
    Write a complete {format_type} in {language}.

    Sender Name: {name}
    Recipient Name: {recipient_name}
    Email Type: {email_type}
    Tone: {tone}
    Length: {length}
    Greeting Style: {greeting_style}
    Closing Style: {closing_style}
    Reason: {final_reason}

    Additional Details:
    From Date: {from_date}
    To Date: {to_date}
    Days: {days}
    Company: {company}
    Role: {role}
    Place: {place}

    Instructions:
    - If Very Short → 2-3 lines
    - If Short → brief
    - If Medium → normal
    - If Long → detailed
    - Use recipient name if provided
    - Include subject (for email)
    - Proper greeting and closing
    - Natural and human-like writing
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert communication writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# ---------- SESSION ---------- #
if "output" not in st.session_state:
    st.session_state.output = ""

# ---------- BUTTON ---------- #
if st.button("🚀 Generate"):
    if not name or not final_reason:
        st.warning("⚠️ Please fill required fields")
    else:
        try:
            st.session_state.output = generate_email()
        except Exception as e:
            st.error(f"Error: {e}")

# ---------- OUTPUT ---------- #
if st.session_state.output:
    st.subheader("📄 Output")

    st.text_area("Generated Content", st.session_state.output, height=300)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button("📥 Download", st.session_state.output, file_name="output.txt")

    with col2:
        if st.button("🔄 Regenerate"):
            st.session_state.output = generate_email()

st.divider()
st.markdown("<p style='text-align:center;'>✨ Smart AI Communication Tool</p>", unsafe_allow_html=True)