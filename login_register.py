import streamlit as st
from database import add_user, login_user, hash_password

# 定义加载 CSS 的函数
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 调用加载 CSS 文件
load_css("style.css")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_password = hash_password(password)
        result = login_user(username, hashed_password)
        if result:
            st.success(f"Logged in as {username}")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state['page'] = "main"
        else:
            st.warning("Incorrect Username/Password")

    if st.button("Go to Register"):
        st.session_state['page'] = "register"

def register():
    st.subheader("Register")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if new_password == confirm_password:
        if st.button("Register"):
            hashed_new_password = hash_password(new_password)
            add_user(new_username, hashed_new_password)
            st.success("You have successfully created an account!")
            st.info("You can now log in.")
    else:
        st.warning("Passwords do not match")

    if st.button("Go to Login"):
        st.session_state['page'] = "login"

def modify_account():
    st.subheader("Modify Account")
    st.info("Account modification functionality to be implemented.")

def delete_account():
    st.subheader("Delete Account")
    st.info("Account deletion functionality to be implemented.")
