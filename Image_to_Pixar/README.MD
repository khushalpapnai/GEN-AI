# Kids World – Pixar/Disney/Cartoon Image Generator

Kids World is an AI-powered application that transforms any uploaded or linked image into a Pixar, Disney, or cartoon-style version.  
It uses BLIP image captioning to describe the input image, then applies Stable Diffusion XL (Base + Refiner) to generate a high-quality stylized output.

---
# Not Live
Because this project uses a very large model, it cannot run on Hugging Face’s free Space tier (16 GB RAM, CPU only). Requirements: GPU with at least 16 GB VRAM, and at least 32 GB of free SSD storage. It will not run on a CPU or an integrated graphics card — please ensure your system meets these requirements before downloading

## ✨ Features
- **Automatic Image Captioning** – Generates a descriptive prompt from your image.
- **Pixar/Disney/Cartoon Styling** – Adds a creative style layer to the generated image.
- **High-Quality Output** – Uses SDXL Base + Refiner for detailed, polished results.
- **Flexible Input** – Accepts both image URLs and file uploads.
- **Download Option** – Save the generated image directly from the app.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kids_world.git
   cd kids_world
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the app locally:
```bash
python app.py
```

Once running, open the provided local URL in your browser to access the Gradio interface.

---

## 🛠 Tech Stack
- **Python**
- **Gradio** – Web UI
- **Hugging Face Transformers** – BLIP image captioning
- **Diffusers** – Stable Diffusion XL Base + Refiner
- **PyTorch**
- **Pillow** – Image processing
- **Requests** – Fetching images from URLs

---

## 📂 Project Structure
```
kids_world/
│
├── app.py                # Main application script
├── requirements.txt      # Python dependencies
├── style.css             # Custom UI styling
└── README.md             # Project documentation
```

---

## 📜 License
MIT License © 2025 khushal

---

## 🤝 Contributing
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact
**Khushal Papnai**  
📧 [khushalpapnai91821@gmail.com](mailto:khushalpapnai91821@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/khuhsal-b295a0345/)  
🔗 [GitHub](https://github.com/khushalpapnai)

