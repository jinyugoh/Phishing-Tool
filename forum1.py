import streamlit as st
import sqlite3

def create_forum_table():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS forum_posts(post_id INTEGER PRIMARY KEY, author TEXT, content TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS comments(comment_id INTEGER PRIMARY KEY, post_id INTEGER, author TEXT, content TEXT)')
    conn.commit()
    conn.close()

def add_post(author, content):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('INSERT INTO forum_posts (author, content) VALUES (?, ?)', (author, content))
    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('SELECT * FROM forum_posts')
    posts = c.fetchall()
    conn.close()
    return posts

def delete_post(post_id):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('DELETE FROM forum_posts WHERE post_id = ?', (post_id,))
    c.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()

def add_comment(post_id, author, content):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)', (post_id, author, content))
    conn.commit()
    conn.close()

def recall_comment(comment_id):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('DELETE FROM comments WHERE comment_id = ?', (comment_id,))
    conn.commit()
    conn.close()

def get_comments(post_id):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,))
    comments = c.fetchall()
    conn.close()
    return comments





def forum_page():
    create_forum_table()

    st.title("Forum")

    # Form to create a new forum post
    with st.form("New Post"):
        post_content = st.text_area("Create a new post", "")
        submitted = st.form_submit_button("Submit Post")
        if submitted and post_content:
            add_post(st.session_state['username'], post_content)
            st.success("Post created successfully!")

    st.subheader("Posts")
    posts = get_posts()
    for post_id, author, content in posts:
        st.markdown(f"**{author}** says:")
        st.markdown(content)

        # Allow delete action for post
        if 'username' in st.session_state and author == st.session_state['username']:
            if st.button(f"Delete Post {post_id}", key=f'delete_{post_id}'):
                delete_post(post_id)
                st.success("Post deleted successfully.")
                continue  # Skip this post since it's deleted




        if 'username' in st.session_state:
            with st.form(f"Comment on Post {post_id}"):
                comment_content = st.text_input("Leave a comment")
                comment_submitted = st.form_submit_button("Submit Comment")
                if comment_submitted and comment_content:
                    add_comment(post_id, st.session_state['username'], comment_content)
                    st.success("Comment added successfully!")

        st.subheader("Comments")
        comments = get_comments(post_id)
        if comments:
            for _, _, comment_author, comment_content in comments:
                st.markdown(f"**{comment_author}** commented:")
                st.markdown(comment_content)

        
        else:
            st.write("No comments yet.")

    if st.button("Back to Main Menu"):
        st.session_state['page'] = 'main'


