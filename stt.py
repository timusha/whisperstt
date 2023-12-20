import streamlit as st
from openai import OpenAI
import io

def transcribe_audio(audio_file, api_key):
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)

    try:
        # Sending the file directly for transcription
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        
        # Check the response type and extract the transcript
        if isinstance(transcript_response, dict):
            return transcript_response.get("text", "No transcript found.")
        elif isinstance(transcript_response, str):
            return transcript_response
        else:
            return "Unexpected response format."
    except Exception as e:
        return f"Error during transcription: {e}"

# Streamlit interface
st.title('ChatGPT арқылы қазақша аудионы мәтінге айналдыру')

# API Key input
api_key = st.text_input("OpenAI API Key", type="password")

# Define supported file types
supported_types = ["flac", "m4a", "mp3", "mp4", "mpeg", "mpga", "oga", "ogg", "wav", "webm"]
uploaded_file = st.file_uploader("Аудио жүкте немесе микрофон арқылы сөйле", type=supported_types)

if uploaded_file is not None and api_key:
    st.audio(uploaded_file, format='audio/wav')
    if st.button('Мәтінге айналдыр'):
        with st.spinner('Айналдырып жатырмын...'):
            transcription = transcribe_audio(uploaded_file, api_key)
            st.text_area("Танскрипция:", transcription, height=150)
else:
    st.warning("Please upload an audio file and enter your OpenAI API key.")
