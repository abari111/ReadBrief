import streamlit as st
from transformers import pipeline
from gtts import gTTS
import tempfile
import os

# Set up the summarization model (using a Hugging Face model)
summarizer = pipeline("summarization")

# Function to extract chapters
def extract_chapters(text, delimiter="Chapitre"):
    chapters = text.split(delimiter)
    # Adding 'Chapter' back to each chapter for clear titles
    return {f"chapitre {idx}": f"{delimiter}{chapter.strip()}" for chapter, idx in zip(chapters, range(len(chapters))) if chapter.strip()}

# Function to summarize text
def summarize_text(text):
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

# Streamlit app layout
st.title("Chapter Summarizer and Audio Generator")

# Upload section
uploaded_file = st.file_uploader("Upload your text file", type="txt")
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    
    # Extract chapters
    chapters = extract_chapters(text)
    st.sidebar.header("Chapters")
    selected_chapter = st.sidebar.radio("Select a Chapter", options=chapters.keys())

    # Display the selected chapter content
    st.subheader("Selected Chapter Content")
    st.write(selected_chapter)
    
    # Summarize the chapter content
    if st.button("Summarize Chapter"):
        summary = summarize_text(chapters[selected_chapter])
        
        # Display text summary
        st.subheader("Text Summary")
        st.write(summary)

        # Generate audio summary
        st.subheader("Audio Summary")
        tts = gTTS(summary)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            tts.save(temp_audio_file.name)
            st.audio(temp_audio_file.name, format="audio/mp3")

    # Download button for the uploaded file
    st.sidebar.download_button(
        label="Download Uploaded File",
        data=text,
        file_name="uploaded_file.txt",
        mime="text/plain"
    )
