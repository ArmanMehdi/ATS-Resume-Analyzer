from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv('Google_API_KEY'))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                'mime_type': "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('No file uploaded')

st.set_page_config(page_title='ATS RESUME EXPERT')
st.header('ATS tracking system')
input_text = st.text_area('Job Description', key='input')
uploaded_file = st.file_uploader('Upload your resume (PDF)', type=['pdf'])
if uploaded_file is not None:
    st.write('PDF uploaded successfully')

submit1 = st.button('Tell me about Resume')
submit2 = st.button('How can I improve my skills')
submit3 = st.button('Percentage match')

input_prompt1 = '''You are an experienced HR with tech experience in the field of Data Science, Full Stack, Web Development, Data Engineering, DevOps, and Data Analytics. Your task is to review the provided resume against the job description for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with the job description. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.'''
input_prompt2 = '''You are an expert career advisor with deep knowledge of Data Science, Full Stack, Web Development, DevOps, and AI. Analyze the candidate’s resume and suggest actionable steps on how they can improve their skills in alignment with current job market trends. Highlight any gaps and recommend learning paths, certifications, or skill development areas.'''
input_prompt3 = '''You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job Data Science, AI, Full Stack, DevOps, and ATS functionality. Your task is to evaluate the resume against the provided job description. Give me the percentage of how much the resume matches the job description. First, the output should come as a percentage, followed by any missing keywords, and finally your thoughts.'''

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader('The response is:')
        st.write(response)
    else:
        st.write('Please upload the resume')
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader('Skill Improvement Suggestions:')
        st.write(response)
    else:
        st.write('Please upload the resume')
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader('The response is:')
        st.write(response)
    else:
        st.write('Please upload the resume')
