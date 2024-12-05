import speech_recognition as sr
import streamlit as st

class VoiceService:
    """Handles voice recognition functionality"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def record_and_transcribe(self) -> str:
        """Record audio and convert to text"""
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak into your microphone.")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                st.success(f"🎯 Transcribed: {text}")
                return text
            except sr.UnknownValueError:
                st.warning("❌ Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"❌ Could not request results: {e}")
            except sr.WaitTimeoutError:
                st.warning("⌛ Listening timed out. Please try again.")
        return ""