import streamlit as st
import tempfile
import os
from audio_extractor import download_audio, convert_audio


st.title("YouTube Audio Clip Extractor 🎵")
st.write("Enter a YouTube video URL, select start and end times, and download the audio clip!")

youtube_url = st.text_input("YouTube URL", "")
start_time = st.number_input("Start Time (in seconds)", min_value=0, step=1, value=0)
end_time = st.number_input("End Time (in seconds)", min_value=1, step=1, value=10)
output_file = st.text_input("Output File Name", "audio_clip")

if st.button("Extract Audio"):
    input_file = output_file + '.webm'
    output_file += ".mp3"
    if youtube_url.strip() == "":
        st.error("Please provide a valid YouTube URL.")
    elif start_time >= end_time:
        st.error("End time must be greater than start time.")
    else:
        try:
            with st.spinner("Extracting audio..."):
                # Get audio link
                download_audio(youtube_url, start_time, end_time, input_file)

                # Extract audio stream
                convert_audio(input_file, output_file)

                # Provide a download link
                with open(output_file, "rb") as file:
                    st.success("Audio clip extracted successfully!")
                    st.download_button(
                        label="Download Audio Clip 🎶",
                        data=file,
                        file_name=output_file,
                        mime="audio/mpeg",
                    )

                # Clean up
                os.remove(input_file)
                os.remove(output_file)
        except Exception as e:
            st.error(f"An error occurred: {e}")
