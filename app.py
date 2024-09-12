import streamlit as st
import requests
import json
from PIL import Image
import time
import re
from TTS.api import TTS
from moviepy.editor import VideoFileClip, AudioFileClip
from unittest.mock import patch
import os


# Display the header
st.markdown("## VibeSnip")
st.markdown("### Automating short video generation.")

# Input for the genre
genre = st.text_input("Enter your idea")

if genre:
    # Set the URL and API key
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    api_key = os.getenv('key')

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Set the data payload
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': f'''
                        
                         {genre}

'''
                    }
                ]
            }
        ]
    }

    # Make the POST request
    response = requests.post(f'{url}?key={api_key}', headers=headers, data=json.dumps(data))

    # Check the response status and print the result
    if response.status_code == 200:
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.markdown(text)
    else:
        st.error('Error: {} {}'.format(response.status_code, response.text))

    st.markdown("### Select the background video template.")

    # Define a function to resize images
    def resize_image(image, width, height):
        """Resize an image to the specified width and height."""
        return image.resize((width, height), Image.ANTIALIAS)

    # Load and resize images
    image1 = Image.open('minecraft.jpg')
    image2 = Image.open('rdr2.png')
    image3 = Image.open('car_race.png')

    desired_width = 300
    desired_height = 200

    image1 = resize_image(image1, desired_width, desired_height)
    image2 = resize_image(image2, desired_width, desired_height)
    image3 = resize_image(image3, desired_width, desired_height)

    # Create a list of image options
    options = {
        'Option 1': image1,
        'Option 2': image2,
        'Option 3': image3,
    }

    # Display images and radio buttons side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image1, caption='minecraft', use_column_width=True)
        option1 = st.radio("", ["Option 1"], key="option1")

    with col2:
        st.image(image2, caption='rdr2', use_column_width=True)
        option2 = st.radio("", ["Option 2"], key="option2")

    with col3:
        st.image(image3, caption='car race', use_column_width=True)
        option3 = st.radio("", ["Option 3"], key="option3")

    # Collect selected option
    selected_option = st.radio(
        "Choose an image:",
        list(options.keys())
    )
    def clean_text(text):
    # Use regex to replace all non-alphanumeric characters (excluding spaces) with an empty string
      return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Display the selected image
    st.image(options[selected_option], caption=selected_option, use_column_width=True, width=desired_width)
    if not os.path.isfile("output.wav"):
      with st.spinner('Generating speech...'):
          with patch('builtins.input', return_value='y'):
            # Initialize TTS
              tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

            # Generate speech by cloning a voice using default settings
              clean_text_content = clean_text(text)
              tts.tts_to_file(
                text=f"{clean_text_content}",
                file_path="output.wav",
                speaker_wav="traning.wav",
                language="en"
              )
              time.sleep(5)
              st.success("Done!")
              st.audio("output.wav", format="audio/wav", loop=True)

    if selected_option == 'Option 1':
      with st.spinner('Generating vedio...'):
        video = VideoFileClip("minecraft.mp4")
        audio = AudioFileClip("output.wav")

        video_with_audio = video.set_audio(audio)

        video_with_audio.write_videofile(f"2.mp4", codec="libx264", audio_codec="aac")
        st.video("2.mp4")
        st.success("Done!")
    elif selected_option == 'Option 2':
      with st.spinner('Generating vedio...'):
        video = VideoFileClip("rdr2.mp4")
        audio = AudioFileClip("output.wav")

        video_with_audio = video.set_audio(audio)

        video_with_audio.write_videofile(f"2.mp4", codec="libx264", audio_codec="aac")
        st.video("2.mp4")
        st.success("Done!")
    elif selected_option == 'Option 3':
      with st.spinner('Generating vedio...'):
        video = VideoFileClip("car_race.mp4")
        audio = AudioFileClip("output.wav")

        video_with_audio = video.set_audio(audio)

        video_with_audio.write_videofile(f"2.mp4", codec="libx264", audio_codec="aac")
        st.video("2.mp4")
        st.success("Done!")
    else :
      st.write("Select correct template!")
    import requests

# Your bot token
    TOKEN = os.getenv('secret')

# Telegram API URL to send video
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    
    # Chat ID where the video will be sent (user ID or group ID)
    chat_id = os.getenv('tel_id')
    
    # Path to your video file
    video_file = '/content/2.mp4'
    
    # Send the video
    with open(video_file, 'rb') as f:
        response = requests.post(url, data={'chat_id': chat_id}, files={'video': f})
    
    # Check if the video was sent successfully
    if response.status_code == 200:
        print("Video sent successfully!")
    else:
        print(f"Failed to send video. Status code: {response.status_code}")
    
    
        f = st.text_input("enter y/n to clear files")
        if f == "y":  
          os.remove("output")
          os.remove("2.mp4")
    
    
