import streamlit as st
import cv2
import numpy as np
from PIL import Image
import openai

# 设置 OpenAI API 密钥
openai.api_key = st.secrets['key']

st.title("Capture QR Code Using Webcam and Analyze with AI")

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
