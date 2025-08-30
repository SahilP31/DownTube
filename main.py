import yt_dlp
import streamlit as st
import os


def download_video(url):
    try:
        # Set yt-dlp options for video download
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Output file name template
        }

        # Download video with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', None)
            video_ext = info.get('ext', None)

        # Construct the full path of the downloaded video
        video_file_name = f"{video_title}.{video_ext}"
        video_path = os.path.join(os.getcwd(), video_file_name)

        return video_path
    except Exception as e:
        print(f"Error: {e}")
        return None


# Streamlit UI Configuration
st.set_page_config(page_title='DownTube', page_icon='▶️')
st.markdown('<h1 style="text-align: center;"> DownTube </h1>', unsafe_allow_html=True)
st.markdown('<h5 style="text-align: center; margin-top:-10px;"> Youtube Video Downloader </h5>', unsafe_allow_html=True)
st.write("")

# Input field for YouTube URL
url = st.text_input("Enter a youtube video url: ")
if url:
    with st.spinner("Downloading video.."):
        # Download the video and get its path
        video_path = download_video(url)
        st.write("")
        if video_path and os.path.exists(video_path):
            # Display the video in the UI
            video_file = open(video_path, "rb")
            video_bytes = video_file.read()
            st.video(video_bytes)

            # Close the file after reading
            video_file.close()
        else:
            st.error("Failed to download or locate the video.")