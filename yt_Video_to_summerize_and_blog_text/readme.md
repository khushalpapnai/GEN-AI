
# YouTube to Blog and Summary

Turn any YouTube video into a clean blog post plus a concise summary using AssemblyAI for transcription, OpenAI for blog generation, and a Hugging Face Transformers summarization pipeline exposed via a simple Gradio UI.

---

## 🚀 Live Demo

- [Live Demo]([https://your-live-link.example](https://9754df9c3c31b213ff.gradio.live/))  
  

---

## 🖼 Image Preview

Here’s how the app looks when running:

![App Screenshot](https://github.com/khushalpapnai/GEN-AI/blob/1379a4787056d1fbbf5540210afc358da93e88cc/yt_Video_to_summerize_and_blog_text/assest/image.png?raw=true)

When server is not Start yet!
----------------------------- error ------------------------------------------------------------
![App Screenshot](yt_Video_to_summerize_and_blog_text/assest/Screenshot%202025-09-04%20182738.png)



---

## ✨ Features

- **YouTube URL normalization** — Cleans and standardizes various YouTube URL formats.
- **Automated transcription** — Uses AssemblyAI to transcribe audio to text.
- **Blog generation** — Creates a full blog post from the transcript using OpenAI.
- **Concise summary** — Summarizes the blog via the Falconsai/text_summarization pipeline.
- **Gradio interface** — Paste a YouTube URL and get both outputs instantly.

---

## ⚡ Quick Start

### 1) Prerequisites

- Python 3.10+
- FFmpeg installed and on PATH
- API keys for:
  - AssemblyAI → `ASSEMBLYAI_API_KEY`
  - OpenAI → `OPENAI_API_KEY`

### 2) Clone and Install

```bash
git clone https://github.com/your-username/yt-video-to-blog-summary.git
cd yt-video-to-blog-summary
python -m venv .venv
# Activate: Windows
.venv\Scripts\activate
# Or macOS/Linux
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 3) Environment Variables

Create a `.env` file:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_key
OPENAI_API_KEY=your_openai_key
```

### 4) Run the App

```bash
python btubeSummery.py
```

---

## 📂 Project Structure

```
.
├─ btubeSummery.py         # Gradio interface
├─ video_to_text.py        # Core logic
├─ requirements.txt        # Dependencies
├─ assets/                 # Screenshots and images
├─ .env                    # API keys (ignored in git)
└─ README.md               # This file
```

---

## 🛠 Troubleshooting

- **TypeError: unexpected keyword argument 'assembly_api_key'**  
  Ensure your `video_to_text.py` constructor matches:
  ```python
  def __init__(self, assembly_api_key):
      ...
  ```
  Clear `__pycache__` and restart your environment.

- **FFmpeg not found**  
  Install FFmpeg and ensure it’s in your PATH.

---

## 📜 License

This project uses third-party APIs and models. Check their licenses before redistribution.
```

---

