import streamlit as st
import google.generativeai as genai
import cv2
import speech_recognition as sr
import pyttsx3
from fer import FER
import tempfile
import os

# Configure Google Generative AI
API_KEY = "AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to capture speech and convert to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand.")
            return None

# Function to analyze facial emotions using FER
def analyze_emotion(frame):
    try:
        # Save the frame as a temporary image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            temp_image_path = temp_image.name
            cv2.imwrite(temp_image_path, frame)

        # Analyze emotion using FER
        emotion_detector = FER()
        emotion = emotion_detector.detect_emotion(frame)
        if emotion:
            dominant_emotion = max(emotion[0]['emotions'], key=emotion[0]['emotions'].get)
        else:
            dominant_emotion = "No emotion detected"

        # Clean up the temporary image
        os.remove(temp_image_path)

        return dominant_emotion
    except Exception as e:
        st.write(f"Error analyzing emotion: {e}")
        return None

# Function to correct grammar using Google Generative AI
def correct_grammar(text):
    try:
        response = model.generate_content(f"Correct this English sentence: {text}")
        corrected_text = response.text
        return corrected_text
    except Exception as e:
        st.write(f"Error correcting grammar: {e}")
        return None

# Function to provide feedback via text-to-speech
def speak_feedback(feedback):
    engine.say(feedback)
    engine.runAndWait()

# Streamlit App Layout
st.title("English Teaching Assistant")
st.write("This app helps you practice English by analyzing your speech, correcting grammar, and understanding your emotions.")

# Webcam Integration
st.write("### Webcam Feed")
webcam_enabled = st.checkbox("Enable Webcam")
if webcam_enabled:
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    while webcam_enabled:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture frame.")
            break

        # Display the webcam feed
        frame_placeholder.image(frame, channels="BGR")

        # Analyze emotion
        emotion = analyze_emotion(frame)
        if emotion:
            st.write(f"Detected Emotion: {emotion}")

        # Break the loop if the user disables the webcam
        if not st.checkbox("Keep Webcam On", value=True):
            webcam_enabled = False

    cap.release()

# Speech Recognition and Grammar Correction
st.write("### Speech Practice")
if st.button("Start Speaking"):
    user_text = speech_to_text()
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
