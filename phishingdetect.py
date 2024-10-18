import streamlit as st
import openai
from PIL import Image
import pytesseract

openai.api_key = st.secrets['key']
# 钓鱼检测页面
def phishing_detection_page():
    st.title("Phishing Detection Page")

    # 功能 1: 邮件文本分析
    st.header("Email Text Phishing Detection")
    email_text = st.text_area("Paste your email content here:")

    if st.button("Analyze Email"):
        if email_text:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this email for phishing: {email_text}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
        else:
            st.warning("Please paste some email content.")

    # 功能 2: 图片上传与文本提取
    st.header("Email Screenshot Phishing Detection")
    uploaded_image = st.file_uploader("Upload an email screenshot", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Email Screenshot')
        text_from_image = pytesseract.image_to_string(image)
        st.write("Extracted text from image:")
        st.write(text_from_image)

        if st.button("Analyze Extracted Text"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this extracted email text for phishing: {text_from_image}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
