import os
import yt_dlp
import requests
import assemblyai as aai
from urllib.parse import urlparse, parse_qs
from openai import OpenAI


class YouTubeBlogGenerator:
    def __init__(self, assembly_api_key):
        # Store AssemblyAI key for transcription
        self.assembly_api_key = assembly_api_key
        aai.settings.api_key = self.assembly_api_key

        # Initialise OpenAI client from env var
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in environment variables.")
        self.openai_client = OpenAI(api_key=openai_key)

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
            return {'filename': filename}

    def get_transcription(self, link):
        data = self.download_audio(link)
        audio_file = data['filename']

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)

        if os.path.exists(audio_file):
            os.remove(audio_file)

        return {'transcription': transcript.text}

    def generate_blog_from_transcription(self, transcription):
        prompt = f"Write a blog article based on this transcript:\n\n{transcription}"
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def generate_blog(self, yt_link):
        yt_link = self.clean_youtube_url(yt_link)
        result = self.get_transcription(yt_link)

        if not result['transcription']:
            raise ValueError("Failed to get transcript")

        blog_content = self.generate_blog_from_transcription(result['transcription'])
        if not blog_content:
            raise ValueError("Failed to generate blog article")

        return {'content': blog_content}