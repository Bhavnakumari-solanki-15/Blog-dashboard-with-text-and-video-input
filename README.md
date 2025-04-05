# 🌐 Multilingual Blog Translator for Indian Languages

Welcome to the **Multilingual Blog Translator** platform! This application empowers users to seamlessly convert blog content into various Indian regional languages, manage blog posts, track analytics, and permanently store translated blogs in a structured format.

---

## ✨ Features

- **Regional Language Translation**  
  Translate blogs into Indian languages like Hindi, Marathi, Tamil, Telugu, Bengali, Kannada, Gujarati, Malayalam, Odia, and Punjabi.

- **Blog Management**  
  Create, update, delete, and view blogs across different languages.

- **Analytics Dashboard**  
  Monitor engagement metrics like views, likes, and shares using interactive visualizations.

- **Translation Accuracy**  
  Uses Levenshtein distance to measure the similarity between the original and translated text for evaluating translation quality.

- **Persistent Storage**  
  All published blogs are saved in a `published_blogs/` directory as JSON files for easy access and portability.

- **Interactive Streamlit UI**  
  Intuitive web interface built using Streamlit for real-time translation and blog interaction.

---

## 🛠 Technology Stack

- **Streamlit** – UI development
- **Google Translate API** – Language translation
- **Levenshtein** – Translation similarity comparison
- **Matplotlib** – Visualization of blog performance
- **Pandas** – Data handling and processing
- **JSON** – Structured data storage

---

## 🚀 Getting Started

### 📥 Clone the Repository

```bash
git clone https://github.com/yourusername/regional-language-blog-translator.git
cd regional-language-blog-translator

## Installation Instructions:

### Create a virtual environment and activate it (optional but recommended).


python -m venv venv

## Usage:

### Homepage:
- Choose the language to which you want to translate your blog.
- Enter text or upload a file to translate.
- Once translated, you can publish the content as a blog and see the translation in real-time.

### Blog Section:
- View all the published blogs with their titles and content.
- Like, share, and track blog performance through the interface.

### Manage Blog:
- Select a blog to manage: edit its content, delete it, or view it.

### Analytics:
- View the performance of each blog based on metrics like views, likes, and shares.
- Visualize these metrics with interactive graphs.

## File Structure:
- **app.py**: Main Streamlit application.
- **requirements.txt**: List of dependencies.
- **published_blogs/**: Directory to store published blog data in JSON format.
- **README.md**: Project documentation.
- **LICENSE**: License file (if applicable).
