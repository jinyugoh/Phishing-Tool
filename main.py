import streamlit as st
import openai
from login_register import login, register, modify_account, delete_account
from phishing_detection import phishing_detection_page
from quiz import quiz_page
from forum1 import forum_page
from database import create_usertable  # 导入创建数据库的函数

# 定义加载 CSS 的函数
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 调用加载 CSS 文件
load_css("style.css")

# 初始化数据库
create_usertable()  # 创建用户表

# Set OpenAI API Key (replace with your actual API key)
openai.api_key = st.secrets['key']

# 页面路由
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if st.session_state['page'] == 'login':
    login()
elif st.session_state['page'] == 'register':
    register()
elif st.session_state['page'] == 'main':
    if 'username' in st.session_state:
        st.title("🔐 Welcome to the Cyber Security App")
        st.markdown("### Protect yourself against phishing and other cyber threats.")

        # 创建三列布局
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button('🔒 Phishing Detection', key='phishing_button', help="Detect phishing attempts"):
                st.session_state['page'] = 'phishing_detection'

        with col2:
            if st.button('📝 Take the Quiz', key='quiz_button', help="Test your knowledge"):
                st.session_state['page'] = 'quiz'

        with col3:
            if st.button('💬 Go to Forum', key='forum_button', help="Discuss and share"):
                st.session_state['page'] = 'forum'

        if st.button('Log Out', key='logout_button'):
            st.session_state['logged_in'] = False
            st.session_state['page'] = 'login'

        # Chatbox Functionality
        chat_expander = st.expander("💬 Live Chat", expanded=False)
        with chat_expander:
            st.markdown("### AI Support")

            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []

            # Display chat history
            for chat in st.session_state.chat_history:
                st.markdown(f"*You*: {chat['user']}")
                st.markdown(f"*AI*: {chat['assistant']}")

            # Input area for user to type message
            query = st.text_input("Enter your query:", key="user_input")

            if st.button("Send", key="send_button"):
                if query:
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{
                                "role": "system",
                                "content": "You are a helpful assistant."
                            }, {
                                "role": "user",
                                "content": query
                            }])
                        answer = response['choices'][0]['message']['content'].strip()
                        st.session_state.chat_history.append({
                            "user": query,
                            "assistant": answer
                        })
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

elif st.session_state['page'] == 'phishing_detection':
    phishing_detection_page()
elif st.session_state['page'] == 'forum':
    forum_page()
elif st.session_state['page'] == 'quiz':
    quiz_page()
