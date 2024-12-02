from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    # convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

#StreamLit App

st.set_page_config(page_title=" ATS Resume Scanner")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded Sucessfully")

submit1 = st.button("Tell Me About the Resume")
# submit2 = st.button("How Can I Improvise my Skills")
submit2 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager in the field of PCB Design, Schematic Layout, full stack developer, data science, your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.  Also write what spoken languages he knows. 
"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of PCB Design, Schematic Layout, full stack developer, data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts. Also tell if we should consider him for the role or not. Write whether his current skills makes him a worthy candidate for this position.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")