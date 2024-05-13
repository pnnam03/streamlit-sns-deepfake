import streamlit as st
import requests
import os
from pathlib import Path

def main():
    st.title("Media Uploader")

    # Input area for text
    text_input = st.text_input("Enter some text")

    # File uploader for image
    st.subheader("Image Upload")
    image_uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_uploaded is not None:
        st.image(image_uploaded)
    # File uploader for video
    st.subheader("Video Upload")
    video_uploaded = st.file_uploader("Upload a video", type=["mp4"])
    if video_uploaded is not None:
        st.video(video_uploaded)
    # Submit button
    if st.button("Submit"):
        # Prepare data
        data = {}
        save_folder = os.path.dirname(__file__)

        if text_input:
            data['text'] = text_input

        if image_uploaded is not None:
            # Save image to /images folder
            image_save_path = Path(save_folder+"/images", image_uploaded.name)
            with open(image_save_path, mode='wb') as w:
                w.write(image_uploaded.getvalue())
            
            # Get an image from /images folder then send to server
            response = send_media('images', image_save_path)
            if response.status_code == 201:
                st.success("Image submitted successfully!")
            else:
                st.error("Failed to submit image to the API")

        if video_uploaded is not None:
            # Save video to /videos folder
            video_save_path = Path(save_folder+"/videos", video_uploaded.name)
            with open(video_save_path, mode='wb') as w:
                w.write(video_uploaded.getvalue())
            
            # Get a video from /videos folder then send to server
            response = send_media('videos', video_save_path)
            if response.status_code == 201:
                st.success("Video submitted successfully!")
            else:
                st.error("Failed to submit video to the API")

# Handle sending action
def send_media(image_or_video, file_path):
    try:
        mime_type = 'image/png' if image_or_video == 'images' else 'video/mp4'
        files = {image_or_video: (Path(file_path).name, open(file_path, 'rb'), mime_type)}

        # Define URL
        response = requests.post("http://localhost:8888/api/v1/media/"+image_or_video, files=files)
        return response
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    main()
