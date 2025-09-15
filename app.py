import streamlit as st
import tempfile
import os
from audio_extractor import download_audio, convert_audio


st.title("YouTube Audio Clip Extractor 🎵")
st.write("""
Enter a YouTube video URL and choose whether to extract a specific audio clip or download the full audio from the video.
""")

youtube_url = st.text_input("YouTube URL", "")

extract_clip = st.checkbox("Extract a specific audio clip?")

if extract_clip:
    st.markdown(
        "<span style='color: #888;'>Select the start and end times for the audio clip you want to extract.</span>", unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input("Start Time (in seconds)", min_value=0, step=1, value=0)
    with col2:
        end_time = st.number_input("End Time (in seconds)", min_value=1, step=1, value=10)
else:
    start_time = 0
    end_time = None  # Will be handled in backend as 'full audio'

change_filename = st.checkbox("Change output file name?")
if change_filename:
    output_file = st.text_input("Output File Name", "audio_clip")
else:
    output_file = "audio_clip"

button_label = "Extract Audio Clip" if extract_clip else "Download"

if st.button(button_label):
    input_file = output_file + '.webm'
    output_file_mp3 = output_file + ".mp3"
    if youtube_url.strip() == "":
        st.error("Please provide a valid YouTube URL.")
    elif extract_clip and end_time is not None and start_time >= end_time:
        st.error("End time must be greater than start time.")
    else:
        try:
            with st.spinner("Processing audio..."):
                # Download audio (full or clip)
                download_audio(
                    youtube_url,
                    start_time,
                    end_time if extract_clip else None,
                    input_file
                )

                # Convert to mp3
                convert_audio(input_file, output_file_mp3)

                # Provide a download link
                with open(output_file_mp3, "rb") as file:
                    st.success("Audio processed successfully!")
                    st.download_button(
                        label="Download Audio 🎶",
                        data=file,
                        file_name=output_file_mp3,
                        mime="audio/mpeg",
                    )

                # Clean up
                os.remove(input_file)
                os.remove(output_file_mp3)
        except Exception as e:
            st.error(f"An error occurred: {e}")
