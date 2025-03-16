import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile
import os

# Configure Google Generative AI
API_KEY = "AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Function to correct grammar using Google Generative AI
def correct_grammar(text):
    try:
        response = model.generate_content(f"Correct this English sentence: {text}")
        corrected_text = response.text
        return corrected_text
    except Exception as e:
        st.write(f"Error correcting grammar: {e}")
        return None

# Function to provide feedback via text-to-speech using gTTS
def speak_feedback(feedback):
    tts = gTTS(text=feedback, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format="audio/mp3")
        os.remove(temp_audio.name)

# Streamlit App Layout
st.title("English Teaching Assistant")
st.write("This app helps you practice English by analyzing your speech and correcting grammar.")

# Speech Practice
st.write("### Speech Practice")
user_text = st.text_input("Type a sentence to practice:")
if user_text:
    corrected_text = correct_grammar(user_text)
    if corrected_text:
        st.write(f"Corrected Sentence: {corrected_text}")
        feedback = f"You said: {user_text}. The correct sentence is: {corrected_text}."
        speak_feedback(feedback)

# Conversational Practice
st.write("### Conversational Practice")
user_input = st.text_input("Ask me anything or practice a conversation:")
if user_input:
    response = model.generate_content(user_input)
    st.write(f"AI Response: {response.text}")
    speak_feedback(response.text)
