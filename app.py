import pickle
import base64
import io
import fitz  # PyMuPDF
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai


load_dotenv()

def load_pickled_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_pickled_model()

def get_gemini_response(input_text, pdf_content, prompt):
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        img_byte_arr = io.BytesIO(pix.tobytes())
        img_byte_arr.seek(0)
        img_data = base64.b64encode(img_byte_arr.read()).decode()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": img_data
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
st.title("ATS Resume Analyzer")

st.markdown("""
    **Welcome to the ATS Resume Analyzer!**  
    This tool is designed to help you evaluate your resume against a job description and optimize it for Applicant Tracking Systems (ATS).
    Follow the instructions below to get started:
""")

with st.form(key="input_form"):
    st.markdown("### 1. Enter Job Description")
    input_text = st.text_area("Job Description", 
                              placeholder="Paste the job description here...",
                              height=200, 
                              key="input")
    
    st.markdown("### 2. Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

    st.markdown("### 3. Select an Action")
    col1, col2, col3 = st.columns(3)

    with col1:
        submit1 = st.form_submit_button("Evaluate Resume")
    with col2:
        submit2 = st.form_submit_button("Skill Improvement Suggestions")
    with col3:
        submit3 = st.form_submit_button("ATS Match Percentage")


input_prompt1 = """You are an experienced Technical HR Manager with deep knowledge in Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis. 
                      Your task is to evaluate the provided resume against the given job description. 
                      Analyze the resume for the following criteria:
                      1. **Keyword Match**: Check if the resume contains the key terms and phrases mentioned in the job description.
                      2. **Skill Alignment**: Assess if the skills and experiences listed in the resume align with the job requirements.
                      3. **Role Fit**: Determine the candidate's suitability for the role based on their professional background and expertise.
                      4. **Strengths and Weaknesses**: Highlight the strengths and weaknesses of the resume in relation to the job description.
                      Provide a detailed evaluation of how well the resume fits the job role and offer suggestions for improvement."""

input_prompt2 = """As a Technical HR Manager with expertise in Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis, review the provided resume and job description.
                      Your task is to provide:
                      1. **Skill Gaps**: Identify any skills or qualifications that are missing from the resume but are required by the job description.
                      2. **Improvement Suggestions**: Offer specific advice on how the candidate can improve their skills and qualifications to better align with the job requirements.
                      3. **Professional Development**: Recommend additional certifications, courses, or experiences that could enhance the candidate's profile for this role."""

input_prompt3 = """You are an ATS expert with comprehensive knowledge of Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis. 
                      Analyze the resume against the provided job description and provide the following:
                      1. **Match Percentage**: Calculate the percentage of match between the resume and the job description based on keyword presence and skill alignment.
                      2. **Missing Keywords**: List any important keywords or phrases from the job description that are absent from the resume.
                      3. **Final Evaluation**: Offer a summary of how the resume compares to the job description, including any major discrepancies or areas for improvement.
                      Ensure your analysis is detailed and provides actionable insights for enhancing the resume's compatibility with the job requirements."""

if submit1 or submit2 or submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if submit1:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
        elif submit2:
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
        elif submit3:
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
        
        st.subheader("**Analysis Result**")
        st.write(response)
    else:
        st.warning("Please upload a resume to proceed.")
