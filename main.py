import yt_dlp
import streamlit as st
import os


def download_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/app/videos/%(title)s.%(ext)s',  # Save in /app/videos
            'merge_output_format': 'mp4',                # Force merge to mp4
        }

        print(f"Downloading video from URL: {url}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)  # ✅ actual saved file path

        print(f"Video Path: {video_path}")

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
        video_path = download_video(url)
        st.write("")

        if video_path and os.path.exists(video_path):
            try:
                with open(video_path, "rb") as video_file:
                    video_bytes = video_file.read()

                    file_ext = os.path.splitext(video_path)[1].lower()

                    if file_ext == ".mp4":
                        st.video(video_bytes)  # ✅ Streamlit can render mp4
                    else:
                        st.success("Video downloaded successfully!")
                        st.download_button(
                            label="Download Video",
                            data=video_bytes,
                            file_name=os.path.basename(video_path),
                            mime="video/mp4" if file_ext == ".mp4" else "application/octet-stream"
                        )
            except Exception as e:
                st.error(f"Failed to display the video: {e}")
        else:
            st.error("Failed to download or locate the video.")
