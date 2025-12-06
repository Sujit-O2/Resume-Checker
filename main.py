import io
import os
import dotenv
import PyPDF2
import requests
import streamlit as st

dotenv.load_dotenv()

def sujit(uploadedFile, job_role="java"):
    if uploadedFile is None:
        st.error("Please upload a PDF file first.")
        st.stop()

    if uploadedFile.type != "application/pdf":
        st.error("Only PDF files are supported.")
        st.stop()

    pdfData= io.BytesIO(uploadedFile.read())

    text = ""
    pdf_reader = PyPDF2.PdfReader(pdfData)
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    if not text.strip():
        st.error("No content extracted from PDF.")
        st.stop()
    return {
        "model": "x-ai/grok-4.1-fast:free",
        "messages": [
            {
                "role": "user",
                "content": f"{text}\n\nJob Role: {job_role}\n"+"Analyze this resume, check if skills match the job role"
                   + "list missing requirements, and give your opinion."
                }
        ]
    }


API_KEY = os.environ["API_KEY"]

st.set_page_config("Sujit Resume", page_icon="🤨", layout="centered")
st.title("Sujit")
st.markdown("Upload Your Resume")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

uploadedFile = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_role = st.text_input("Enter the job role")

if st.button("Analyze"):
    st.write("Analyzing...")

    data = sujit(uploadedFile, job_role)
    resp = requests.post(url=url, json=data, headers=headers)

    st.write(resp.json()["choices"][0]["message"]["content"])
