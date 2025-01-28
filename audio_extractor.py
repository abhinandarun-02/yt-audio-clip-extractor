import yt_dlp
import ffmpeg

def extract_audio_stream(audio_url, start_time, end_time, output_file):
    try:
        (
            ffmpeg
            .input(audio_url, ss=start_time, to=end_time)
            .output(output_file, format='mp3', acodec='libmp3lame', y=None)
            .run()
        )
        return output_file
    except ffmpeg.Error as e:
        st.error(f"An error occurred: {e.stderr.decode()}")
        raise 


def get_audio_link(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        audio_url = info['formats'][9]['url']
        return audio_url