YouTube to blog and summary

Turn any YouTube video into a clean blog post plus a concise summary using AssemblyAI for transcription, OpenAI for blog generation, and a Hugging Face Transformers summarization pipeline exposed via a simple Gradio UI.



## Live demo

- [Live Demo](https://ef604358b9d1363a17.gradio.live/)  



## Features

- **YouTube URL normalization:** Cleans and standardizes various YouTube URL formats.
- **Automated transcription:** Uses AssemblyAI to transcribe audio to text.
- **Blog generation:** Creates a full blog post from the transcript using OpenAI.
- **Concise summary:** Summarizes the blog via the Falconsai/text_summarization pipeline.
- **Gradio interface:** Paste a YouTube URL and get both outputs instantly.

---

## Quick start

### 1) Prerequisites

- **Python:** 3.10+ recommended
- **FFmpeg:** Required by yt-dlp for audio extraction
- **API keys:**  
  - AssemblyAI: ASSEMBLYAI_API_KEY  
  - OpenAI: OPENAI_API_KEY

> Tip: On Windows, install FFmpeg via Chocolatey; on macOS, use Homebrew.

### 2) Clone and install

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

If you don’t have a requirements.txt yet, you can start with:

```bash
pip install yt-dlp requests assemblyai openai python-dotenv gradio "transformers>=4.42.0" "torch>=2.2.0"
```

### 3) Environment variables

Create a .env file in the project root:

```bash
# .env
ASSEMBLYAI_API_KEY=your_assemblyai_key
OPENAI_API_KEY=your_openai_key
```

Or export them in your shell:

```bash
# macOS/Linux
export ASSEMBLYAI_API_KEY=your_assemblyai_key
export OPENAI_API_KEY=your_openai_key

# Windows (PowerShell)
$env:ASSEMBLYAI_API_KEY="your_assemblyai_key"
$env:OPENAI_API_KEY="your_openai_key"
```

### 4) Run the app

```bash
python btubeSummery.py
```

Gradio will print a local URL. To share publicly for quick testing, you can enable sharing in code or use your hosting platform’s URL.

---

## Usage

- **Input:** Paste a valid YouTube URL in the Gradio textbox.
- **Output:**  
  - Summary: Short, high-level overview.  
  - Full Blog: Well-structured article based on the video transcript.

> Note: The app downloads audio with yt-dlp and transcribes locally before sending to AssemblyAI. If you deploy in restricted environments (e.g., Hugging Face Spaces with blocked network for yt-dlp), consider switching to AssemblyAI’s direct YouTube URL transcription to avoid downloading media files.

---

## Project structure

```
.
├─ btubeSummery.py         # Gradio interface: wires together transcription, blog generation, and summarization
├─ video_to_text.py        # YouTube URL cleanup, audio download, transcription, OpenAI blog generation
├─ requirements.txt        # Python dependencies (recommended)
├─ .env                    # API keys (never commit to Git)
└─ README.md               # This file
```

---

## Notes and troubleshooting

- **TypeError: unexpected keyword argument 'assembly_api_key':**  
  - Ensure the runtime is importing the updated video_to_text.py that defines:
    ```python
    def __init__(self, assembly_api_key):
        ...
    ```
  - Clear __pycache__, restart your interpreter, and confirm import path:
    ```bash
    python -c "import video_to_text; print(video_to_text.__file__)"
    ```

- **FFmpeg not found:** Install FFmpeg and make sure it’s on your PATH.

- **OpenAI/AssemblyAI errors:** Double-check API keys and quota.

- **Model and licensing:** Falconsai/text_summarization is pulled from Hugging Face. Verify its license and ensure third-party APIs (OpenAI, AssemblyAI) meet your compliance needs if you plan to open-source or redistribute.

---

