import yt_dlp
import openai
import whisper
import os
import streamlit as st


# Step 1: Download the audio from the YouTube video
def download_audio_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'video_audio.%(ext)s',  # Save as 'video_audio.mp3'
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Step 2: Transcribe the audio using Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    # You can use "small", "medium", or "large" for better accuracy
    result = model.transcribe(audio_file)
    return result['text']


# Step 3: Summarize the transcript using OpenAI GPT
def summarize_transcript(transcript):
    openai.api_key = (
        'sk-proj-Zf4KUFNnEFnCkz8Eg_t_Cjd1ToxsRI9YuoF2EKRiYvfVciJTVu7JtwTgZZhzsVJG'
        '4mbnweLYu6T3BlbkFJFH0mRXUog-HAWdWRn155A1IhYLm3Y-I4Bv01ZRIbog2ZcW3MFsOMxaze'
        'T-xI15zKnS9GJ8OxcA'
    )  # Replace with your OpenAI API key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" for better performance
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes video content."},
            {"role": "user", "content": f"Summarize the following transcript:\n{transcript}"}
        ],
        max_tokens=300
    )
    summary = response['choices'][0]['message']['content']
    return summary


# Streamlit UI
st.title("Video Content Summarizer")
st.write("Enter a YouTube video URL to get a summary of its content.")

# User input for video URL
video_url = st.text_input("YouTube Video URL:")

if video_url:
    with st.spinner('Downloading and processing the video...'):
        try:
            # Download the audio from the YouTube video
            download_audio_from_youtube(video_url)

            # Transcribe the audio
            transcript = transcribe_audio("video_audio.mp3")

            # Summarize the transcript
            summary = summarize_transcript(transcript)

            st.success("Summary Generated Successfully!")
            st.subheader("Video Summary:")
            st.write(summary)

            # Clean up the audio file after processing
            os.remove("video_audio.mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
