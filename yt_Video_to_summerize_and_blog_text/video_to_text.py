import os
import yt_dlp
import requests
import assemblyai as aai
from urllib.parse import urlparse, parse_qs


class YouTubeBlogGenerator:
    def __init__(self, api_key, model_name, api_url):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = api_url
        aai.settings.api_key = self.api_key

    def clean_youtube_url(self, url):
        parsed = urlparse(url)
        if 'youtu.be' in parsed.netloc:
            return f"https://youtu.be{parsed.path}"
        elif 'youtube.com' in parsed.netloc:
            qs = parse_qs(parsed.query)
            video_id = qs.get('v', [None])[0]
            return f"https://www.youtube.com/watch?v={video_id}" if video_id else url
        return url

    def download_audio(self, link):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'quiet': True,
            'user_agent': (
                "Mozilla/5.0 (Windows NT 11.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return {
                'filename': filename
            }

    def get_transcription(self, link):
        data = self.download_audio(link)
        audio_file = data['filename']

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)

        if os.path.exists(audio_file):
            os.remove(audio_file)

        return {
            'transcription': transcript.text
        }

    def generate_blog_from_transcription(self, transcription):
        prompt = (
            "Based on the following transcript from a YouTube video, write a comprehensive blog article. "
            "Make it look like a proper blog article, not a video summary:\n\n"
            f"{transcription}\n\nArticle:"
        )

        response = requests.post(
            self.api_url,
            json={"model": self.model_name, "prompt": prompt, "stream": False}
        )
        return response.json().get("response", "No response from local model.")

    def generate_blog(self, yt_link):
        yt_link = self.clean_youtube_url(yt_link)
        result = self.get_transcription(yt_link)

        if not result['transcription']:
            raise ValueError("Failed to get transcript")

        blog_content = self.generate_blog_from_transcription(result['transcription'])
        if not blog_content:
            raise ValueError("Failed to generate blog article")

        return {
            'content': blog_content
        }

