import streamlit as st
import uuid
from datetime import datetime
from googletrans import Translator
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import Levenshtein

# Initialize Google Translate and set up languages
translator = Translator()
languages = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Kannada": "kn",
    "Telugu": "te",
    "Bengali": "bn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Odia": "or"
}

# Directory to store published blogs
published_blog_directory = "published_blogs"

# Ensure the published blogs directory exists
if not os.path.exists(published_blog_directory):
    os.makedirs(published_blog_directory)

# Placeholder to store blog data, analytics, and translation accuracy
if "blog_data" not in st.session_state:
    st.session_state.blog_data = {}
if "edit_history" not in st.session_state:
    st.session_state.edit_history = []  # Store edit history with timestamps
if "blog_views" not in st.session_state:
    st.session_state.blog_views = {}  # Store blog views
if "blog_likes" not in st.session_state:
    st.session_state.blog_likes = {}  # Store blog likes
if "blog_shares" not in st.session_state:
    st.session_state.blog_shares = {}  # Store blog shares
if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False  # Flag to control showing analytics
if "home_page" not in st.session_state:
    st.session_state.home_page = True  # Flag to control if user is on the homepage
if "blog_categories" not in st.session_state:
    st.session_state.blog_categories = []  # Store blog categories
if "blog_tags" not in st.session_state:
    st.session_state.blog_tags = []  # Store blog tags

# Function to translate text into regional languages
def translate_text(text, languages):
    translations = {}
    for language, code in languages.items():
        try:
            translated = translator.translate(text, dest=code)
            translations[language] = translated.text
        except Exception as e:
            translations[language] = f"Error: {e}"
    return translations

# Function to calculate translation accuracy based on Levenshtein distance
def calculate_accuracy(original_text, translated_text):
    # Calculate the Levenshtein distance between the original and translated text
    levenshtein_distance = Levenshtein.distance(original_text, translated_text)
    max_len = max(len(original_text), len(translated_text))
    
    # The accuracy will be inversely proportional to the Levenshtein distance
    accuracy = (1 - levenshtein_distance / max_len) * 100  # Percentage accuracy
    return accuracy

# Function to track blog edits with timestamps
def track_edit_history(blog_id, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.edit_history.append({"blog_id": blog_id, "action": action, "timestamp": timestamp})

# Function to increment views, likes, and shares for a blog
def increment_blog_stat(blog_id, stat_type):
    if stat_type == "view":
        if blog_id not in st.session_state.blog_views:
            st.session_state.blog_views[blog_id] = 0
        st.session_state.blog_views[blog_id] += 1
    elif stat_type == "like":
        if blog_id not in st.session_state.blog_likes:
            st.session_state.blog_likes[blog_id] = 0
        st.session_state.blog_likes[blog_id] += 1
    elif stat_type == "share":
        if blog_id not in st.session_state.blog_shares:
            st.session_state.blog_shares[blog_id] = 0
        st.session_state.blog_shares[blog_id] += 1

# Function to save the blog to a file (simulating permanent storage)
def save_blog_to_file(blog_id, blog_data):
    file_path = os.path.join(published_blog_directory, f"{blog_id}.json")
    with open(file_path, "w") as f:
        json.dump(blog_data, f)
    st.success(f"Blog '{blog_data['title']}' published successfully!", icon="📢")

# Streamlit app UI improvements
st.set_page_config(page_title="Regional Language Blog Translator", page_icon="🌐", layout="wide")

# Title and Description
st.title("🌍 *Regional Language Blog Translator*")
st.markdown(""" 
    Welcome to the *Regional Language Blog Translator* app! Upload text or a file, and see it translated into 
    multiple Indian languages. Manage your blog content, SEO, and analytics easily.
""")
st.markdown("---")

# Sidebar for user dashboard with better styling
st.sidebar.header("📊 *Dashboard*")
uploaded_blogs = list(st.session_state.blog_data.keys())

# Dashboard refresh button
if st.sidebar.button("Refresh Dashboard"):
    st.session_state.show_analytics = True  # Set flag to show analytics after refresh
    st.session_state.home_page = False  # Ensure the user goes to the dashboard
    st.query_params = {}  # Reset query parameters

# Home Button: Returns to the homepage
if st.sidebar.button("Home"):
    st.session_state.show_analytics = False  # Reset analytics visibility
    st.session_state.home_page = True  # Set the user to be on the homepage
    st.query_params = {}  # Reset query parameters

# Create tabs for different sections
tabs = ["Homepage", "Manage Blog", "Analytics", "Blog Section"]
selected_tab = st.sidebar.radio("Select Tab", tabs)

# Home Page Content
if selected_tab == "Homepage" and st.session_state.home_page:
    st.subheader("Welcome to the Homepage!")
    st.markdown("Here, you can translate text or upload files for regional language blog translations.")

    # Language selection dropdown (This will be hidden if a blog is being managed)
    selected_language = st.selectbox("Select Language for Translation", list(languages.keys()), index=0)

    # Dynamic Content Section
    st.subheader("Enter the Content for Translation")
    input_option = st.radio("Select Input Type", ("Text", "Text File", "Video/Audio File"), key="input_type")

    # Text Input
    if input_option == "Text":
        text_input = st.text_area("Enter text to translate:", height=150)
        if text_input:
            st.info("Translating into regional languages...", icon="🔄")

            # Translate the text
            translations = translate_text(text_input, languages)

            # Display translated text only for selected language
            if selected_language:
                translated_text = translations[selected_language]
                # Display translated blog content
                st.subheader(f"Translated Blog in {selected_language}")
                st.write(translated_text)

                # Add a Publish button
                if st.button(f"Publish {selected_language} Blog", key="publish_blog"):
                    blog_id = str(uuid.uuid4())
                    # Store blog with content, categories, and tags
                    st.session_state.blog_data[blog_id] = {
                        "content": translated_text,
                        "categories": [],
                        "tags": [],
                        "title": f"Blog in {selected_language}"
                    }
                    track_edit_history(blog_id, "Published")
                    increment_blog_stat(blog_id, "view")
                    save_blog_to_file(blog_id, st.session_state.blog_data[blog_id])  # Save to file
                    st.success(f"Blog published successfully!", icon="📢")
                    st.write(f"Published Blog ID: {blog_id}")
                    st.text_area(f"Edit {selected_language} Blog Draft:", translated_text, height=150)

# Blog Section
elif selected_tab == "Blog Section":
    st.subheader("📚 *Blog Section*")
    # Show a list of published blogs
    for blog_id, blog in st.session_state.blog_data.items():
        blog_name = blog["title"]
        st.markdown(f"### {blog_name}")
        st.write(blog["content"])

        # Show like button and update like counter
        if st.button(f"Like {blog_name}", key=f"like_{blog_id}"):

            increment_blog_stat(blog_id, "like")
            st.success(f"Liked the blog '{blog_name}'!")

        st.markdown("---")

# Manage Blog Section
elif selected_tab == "Manage Blog":
    uploaded_blogs = list(st.session_state.blog_data.keys())
    if uploaded_blogs:
        st.sidebar.subheader("Recent Blogs")
        for blog in uploaded_blogs[-5:]:  # Show the last 5 blogs
            st.sidebar.write(f"➡️ {blog}")

        blog_to_manage = st.sidebar.selectbox("Select Blog to Manage", uploaded_blogs)
        blog_action = st.sidebar.radio("Choose Action", ("Edit", "Delete", "View Blog"))

        # Edit Blog
        if blog_action == "Edit":
            blog_content = st.session_state.blog_data[blog_to_manage]["content"]
            edited_content = st.text_area(f"Edit Blog: {blog_to_manage}", blog_content, height=250)
            if st.button("Update Blog", key="update_blog"):
                st.session_state.blog_data[blog_to_manage]["content"] = edited_content
                track_edit_history(blog_to_manage, "Edited")
                st.success("Blog updated successfully!", icon="✅")

        # Delete Blog
        elif blog_action == "Delete":
            if st.button(f"Delete {blog_to_manage}", key="delete_blog"):
                del st.session_state.blog_data[blog_to_manage]
                track_edit_history(blog_to_manage, "Deleted")
                st.success(f"Blog '{blog_to_manage}' deleted successfully.", icon="❌")

        # View Blog Content
        elif blog_action == "View Blog":
            st.write(st.session_state.blog_data[blog_to_manage]["content"])

# Analytics
elif selected_tab == "Analytics":
    st.subheader("📊 *Analytics*")
    st.markdown("Visualize your blog's performance.")

    # Display views, likes, and shares for blogs
    for blog_id in st.session_state.blog_data.keys():
        views = st.session_state.blog_views.get(blog_id, 0)
        likes = st.session_state.blog_likes.get(blog_id, 0)
        shares = st.session_state.blog_shares.get(blog_id, 0)

        # Plot the data
        fig, ax = plt.subplots()
        ax.bar(["Views", "Likes", "Shares"], [views, likes, shares], color=["blue", "green", "orange"])
        ax.set_title(f"Blog Performance for {blog_id}")
        ax.set_xlabel("Metrics")
        ax.set_ylabel("Count")

        st.pyplot(fig)
