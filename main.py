import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import io
import base64

Google_API_KEY ='AIzaSyD20lbYsJVsDHt5CdZYp4n8r6CIqCZ7uVo'
genai.configure(api_key=Google_API_KEY)

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Use fitz to extract the first page image from the PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        
        img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))
        
        pdf_parts = [
            {
                'mime_type': "image/jpeg",
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()
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

input_prompt1 = '''You are an experienced HR with tech experience in the field of Data Science, Full Stack, Web Development, Data Engineering, DevOps, and Data Analytics...'''

input_prompt2 = '''You are an expert career advisor with deep knowledge of Data Science, Full Stack, Web Development, DevOps, and AI...'''

input_prompt3 = '''You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of...'''

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
