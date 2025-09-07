# 🖼️ Object Finder — URL or Upload

An interactive web app built with [Gradio](https://gradio.app/) and [Hugging Face Transformers](https://huggingface.co/) that detects objects in an image and highlights them with bounding boxes.  
Users can choose to **paste an image URL** or **upload a file** — only one input is active at a time.

---

## 🚀 Live Demo

[![Open in Browser](https://img.shields.io/badge/Live%20Demo-Click%20Here-orange?style=for-the-badge)](https://huggingface.co/spaces/liljujutsu/findyMater)

---

## 📸 Demo

| Show Case |
|---------------------|
| ![Show](asset/dict.png) |

---

## ✨ Features

- **Dual Input Mode** — Choose between image URL or file upload.
- **High‑visibility bounding boxes** with dynamic colors.
- **Confidence threshold slider** to filter low‑confidence detections.
- **Download processed image** with annotations.
- **Responsive layout** for desktop and mobile.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [Gradio](https://gradio.app/) — UI framework
- [Transformers](https://huggingface.co/docs/transformers/index) — DETR object detection model
- [Pillow](https://pillow.readthedocs.io/) — Image processing

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/object-finder.git
cd object-finder

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```
````

---

## ⚙️ Usage

1. Select **Image URL** or **Upload Image**.
2. Paste the URL or upload a file.
3. Adjust the **confidence threshold** if needed.
4. Click **Detect Objects**.
5. View and download the annotated image.

---

## 📄 License

MIT License 2025 khuhsal

---

## 🙌 Acknowledgements

- [facebook/detr-resnet-50](https://huggingface.co/facebook/detr-resnet-50) for object detection.
- [Gradio](https://gradio.app/) for the interactive UI.
- [Hugging Face](https://huggingface.co/) for model hosting.

```

```
