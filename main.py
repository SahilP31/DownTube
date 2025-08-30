import yt_dlp
import streamlit as st
import os


def download_video(url):
    try:
        # Set yt-dlp options for video download
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/app/videos/%(title)s.%(ext)s',  # Save videos to the mounted volume
            'merge_output_format': 'mp4',  # Ensure merging is supported (e.g., mp4)
        }

        print(f"Downloading video from URL: {url}")  # Log the URL

        # Download video with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', None)
            video_ext = info.get('ext', None)

        # Construct the full path of the downloaded video
        video_file_name = f"{video_title}.{video_ext}"
        video_path = os.path.join("/app/videos", video_file_name)  # Use /app/videos

        print(f"Video Path: {video_path}")  # Log the video path

        # Check if the file exists
        if os.path.exists(video_path):
            print("Video file exists.")
            return video_path
        else:
            print("Video file does not exist.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Streamlit UI Configuration
st.set_page_config(page_title='DownTube', page_icon='▶️')
st.markdown('<h1 style="text-align: center;"> DownTube </h1>', unsafe_allow_html=True)
st.markdown('<h5 style="text-align: center; margin-top:-10px;"> Youtube Video Downloader </h5>', unsafe_allow_html=True)
st.write("")

# Input field for YouTube URL
url = st.text_input("Enter a YouTube video URL:")
if url:
    with st.spinner("Downloading video..."):
        # Download the video and get its path
        video_path = download_video(url)
        st.write("")
        if video_path and os.path.exists(video_path):  # Check if the file exists
            # Display the video in the UI
            try:
                video_file = open(video_path, "rb")
                video_bytes = video_file.read()
                st.video(video_bytes)
                video_file.close()
            except Exception as e:
                st.error(f"Failed to display the video: {e}")
        else:
            st.error("Failed to download or locate the video.")
