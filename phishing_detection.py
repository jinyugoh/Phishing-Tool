import streamlit as st
from PIL import Image
import pytesseract
import openai
import speech_recognition as sr
from pydub import AudioSegment
import cv2
import numpy as np

# 设置 OpenAI API 密钥
openai.api_key = st.secrets['key']

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    # 使用 pydub 将音频文件转换为 WAV 格式
    audio_segment = AudioSegment.from_file(audio_file)

    # 将音频文件导出为临时 WAV 文件
    audio_segment.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            st.warning("Could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from the recognition service.")
            return None

def decode_qr_code(image):
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    qr_data, points, _ = detector(image_cv)

    if qr_data:
        return [qr_data]
    else:
        return []

def capture_qr_code():
    st.header("Capture QR Code Using Webcam")
    st.write("Click the button to take a picture.")

    # 使用 streamlit 提供的摄像头输入组件
    picture = st.camera_input("Take a picture")

    if picture:
        # 将图像转换为 PIL 格式
        img = Image.open(picture)

        # 将 PIL 图像转换为 numpy 数组，并转换为 OpenCV 格式
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # 使用 OpenCV 的 QRCodeDetector 进行二维码检测和解码
        qrCodeDetector = cv2.QRCodeDetector()
        decoded_text, points, _ = qrCodeDetector.detectAndDecode(img_cv)

        if points is not None:
            # 在图像中绘制二维码的边界
            points = points[0].astype(int)
            for i in range(len(points)):
                cv2.line(img_cv, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

            # 显示带有二维码标记的图像
            st.image(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB), channels="RGB")

            # 如果二维码成功解码，调用 OpenAI API 来分析解码后的内容
            st.write("Analyzing QR Code with AI...")

            # 调用 OpenAI GPT 模型进行分析
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Analyze this QR code content: {decoded_text}. What is its purpose?"}
                ],
                max_tokens=100,
                temperature=0.5
            )

            # 显示 AI 的分析结果
            ai_analysis = response['choices'][0]['message']['content'].strip()
            st.write(f"AI Analysis: {ai_analysis}")

        else:
            st.write("No QR Code detected.")

def phishing_detection_page():
    st.title("Phishing Detection Page")

    if st.button("Back to Main Page"):
        st.session_state['page'] = 'main' 

    st.header("Email Text Phishing Detection")
    email_text = st.text_area("Paste your email content here:")
    if st.button("Analyze Email"):
        if email_text:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this email and detect if it's a phishing attempt: {email_text}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
        else:
            st.warning("Please paste some email content.")

    st.header("Email Screenshot Phishing Detection")
    uploaded_image = st.file_uploader("Upload an email screenshot", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Email Screenshot')
        text_from_image = pytesseract.image_to_string(image)
        st.write("Extracted text from image:")
        st.write(text_from_image)

        if st.button("Analyze Extracted Text"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this extracted email text and detect if it's a phishing attempt: {text_from_image}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)

    st.header("SMS Smishing Detection")
    sms_text = st.text_area("Paste your SMS content here:")
    if st.button("Analyze SMS"):
        if sms_text:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this SMS and detect if it's a smishing attempt: {sms_text}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
        else:
            st.warning("Please paste some SMS content.")

    # st.header("Voice Phishing (Vishing) Detection")
    # uploaded_audio = st.file_uploader("Upload a voice message (WAV, MP3, etc.)", type=["wav", "mp3", "m4a"])
    # if uploaded_audio is not None:
    #     vishing_transcript = audio_to_text(uploaded_audio)
    #     if vishing_transcript:
    #         st.write("Extracted text from voice message:")
    #         st.write(vishing_transcript)

    #         if st.button("Analyze Vishing"):
    #             response = openai.ChatCompletion.create(
    #                 model="gpt-3.5-turbo",
    #                 messages=[{"role": "user", "content": f"Analyze this voice message transcript and detect if it's a vishing attempt: {vishing_transcript}"}],
    #                 max_tokens=150,
    #                 temperature=0.5
    #             )
    #             result = response['choices'][0]['message']['content'].strip()
    #             st.write("AI Analysis Result:")
    #             st.write(result)

    st.header("Malvertising Detection")
    malvertising_url = st.text_input("Paste the URL of the advertisement:")
    if st.button("Analyze Malvertising"):
        if malvertising_url:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this advertisement URL and detect if it's malicious: {malvertising_url}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
        else:
            st.warning("Please paste the advertisement URL.")

    st.header("Website/Login Page Spoofing Detection")
    spoofed_url = st.text_input("Paste the URL of the suspected spoofed website:")
    if st.button("Analyze Spoofed Website"):
        if spoofed_url:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this website URL and detect if it’s a spoofed page: {spoofed_url}"}],
                max_tokens=150,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content'].strip()
            st.write("AI Analysis Result:")
            st.write(result)
        else:
            st.warning("Please paste the website URL.")

    st.header("QR Code Detection")
    capture_qr_code()

# 主应用
def main():
    st.title("Phishing Detection Application")
    st.sidebar.title("Navigation")
    st.sidebar.button("Phishing Detection", on_click=phishing_detection_page)

if __name__ == "__main__":
    main()
