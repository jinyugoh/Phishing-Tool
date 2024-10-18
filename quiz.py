import streamlit as st
import openai
from database import create_usertable, add_user, login_user, update_highscore, get_highscore
from database import get_leaderboard, get_highscore, update_highscore


# 设置 OpenAI API 密钥
openai.api_key = st.secrets['key']
# 创建数据库表
create_usertable()

def generate_questions():
    """使用 OpenAI API 生成随机问题."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Generate 10 yes/no questions about phishing with their correct answers in lowercase."}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # 解析生成的文本
        questions_text = response['choices'][0]['message']['content'].strip()
        questions = questions_text.split("\n\n")

        formatted_questions = []
        for entry in questions:
            lines = entry.strip().split("\n")
            if len(lines) >= 2:
                question = lines[0].strip()
                answer = lines[1].strip().lower()  # 将正确答案转为小写
                formatted_questions.append({"question": question, "answer": answer})

        if len(formatted_questions) != 10:
            st.error("Error: Generated questions do not equal 10. Please try again.")
            return []

        return formatted_questions

    except Exception as e:
        st.error("Error generating questions: " + str(e))
        return []

def quiz_page():
    """问答游戏页面."""
    st.title("Phishing Quiz Game")

    # 输入用户名
    if 'username' not in st.session_state:
        st.session_state['username'] = st.text_input("Enter your username:")

    if st.session_state['username']:
        if 'questions' not in st.session_state:
            st.session_state['questions'] = generate_questions()
            st.session_state['score'] = 0
            st.session_state['current_question'] = 0
            st.session_state['quiz_finished'] = False
            st.session_state['user_answers'] = [None] * 10  # 初始化用户答案列表

        if st.session_state['quiz_finished']:
            st.subheader("Quiz Finished!")
            st.write(f"Your score: {st.session_state['score']}/{len(st.session_state['questions'])}")

            # 更新数据库中的高分
            update_highscore(st.session_state['username'], st.session_state['score'])

            # 显示用户的最高分
            st.write(f"Your highest score: {get_highscore(st.session_state['username'])}")

            # 显示排行榜按钮
            if st.button("View Leaderboard"):
                st.subheader("Leaderboard")
                leaderboard = get_leaderboard()  # 从数据库获取排行榜
                st.write("Scores:")
                for idx, (username, score) in enumerate(leaderboard, 1):
                    st.write(f"{idx}. {username}: {score}")

            # 显示每个问题的答案
            for idx, question in enumerate(st.session_state['questions']):
                st.write(f"Q{idx + 1}: {question['question']}")
                st.write(f"Your answer: {st.session_state['user_answers'][idx]}")
                st.write(f"Correct answer: {question['answer'].capitalize()}")
                st.write("---")

            if st.button("Back to Main Page"):
                st.session_state['page'] = 'main'
                st.session_state.pop('questions', None)
                st.session_state.pop('score', None)
                st.session_state.pop('current_question', None)
                st.session_state.pop('quiz_finished', None)
                st.session_state.pop('user_answers', None)
        else:
            current_question_index = st.session_state['current_question']

            if current_question_index < len(st.session_state['questions']):
                current_question = st.session_state['questions'][current_question_index]
                st.subheader(current_question['question'])

                # 显示用户的答案
                user_answer = st.radio("Choose your answer:", ("Yes", "No"), key=f'user_answer_{current_question_index}')

                col1, col2 = st.columns(2)

                # 左侧按钮，查看上一题
                with col1:
                    if st.button("⬅️ Previous"):
                        if current_question_index > 0:
                            st.session_state['current_question'] -= 1

                # 右侧按钮，查看下一题
                with col2:
                    if st.button("Next ➡️"):
                        if current_question_index < len(st.session_state['questions']) - 1:
                            st.session_state['current_question'] += 1

                # 保存用户答案（每次选择都会保存当前问题的答案）
                st.session_state['user_answers'][current_question_index] = user_answer.lower()

                # 提交按钮
                if st.button("Submit"):
                    # 检查是否所有问题都已作答
                    if None in st.session_state['user_answers']:
                        st.warning("You haven't answered all the questions. Please complete the quiz before submitting.")
                    else:
                        # 所有问题都已作答，计算分数并结束问答
                        for idx, question in enumerate(st.session_state['questions']):
                            if st.session_state['user_answers'][idx] == question['answer']:
                                st.session_state['score'] += 1
                        st.session_state['quiz_finished'] = True



# 测试 quiz_page 函数
if __name__ == "__main__":
    quiz_page()
