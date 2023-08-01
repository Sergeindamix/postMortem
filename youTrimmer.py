import os
import streamlit as st
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

def download_video(youtube_url, output_file):
    yt = YouTube(youtube_url)
    video = yt.streams.get_highest_resolution()
    video.download(output_path=os.path.dirname(output_file), filename=os.path.basename(output_file))

def trim_video(input_file, output_file, start, end):
    clip = VideoFileClip(input_file).subclip(start, end)
    clip.write_videofile(output_file)

st.title("YouTube Video Trimmer")

YOUTUBE_URL = st.text_input("Enter the YouTube video URL", "https://www.youtube.com/watch?v=jkDzEIPgI90")
start = st.number_input("Start (seconds)", value=0)
end = st.number_input("End (seconds)", value=30)

# Check if the video is downloaded and trimmed
input_file = "/content/sample_data/input_vid.mp4"
output_file = "/content/sample_data/trimmed_vid.mp4"

if st.button("Trim Video"):
    try:
        download_video(YOUTUBE_URL, input_file)
        trim_video(input_file, output_file, start, end)
        st.success("Video trimmed successfully.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Preview the trimmed video
if os.path.exists(output_file):
    st.markdown("### Trimmed Video Preview")
    st.video(output_file)
