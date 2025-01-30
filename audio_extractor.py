import ffmpeg
import subprocess


def convert_audio(input_file, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='mp3', acodec='libmp3lame', y=None)
            .run()
        )
        return output_file
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
        raise


def download_audio(youtube_url, start_time, end_time, input_file):
    try:
        subprocess.run([
            "yt-dlp", "-f", "bestaudio", 
            f"--download-sections", f"*{start_time}-{end_time}", 
            youtube_url, "-o", input_file
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        raise