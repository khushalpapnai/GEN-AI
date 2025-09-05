# 📊 Sentiment Analyzer

**Turn your reviews into instant insights with live sentiment scoring and vibrant visual charts.**

---

## 🚀 Live Demo
🔗 **[Try the app here](https://huggingface.co/spaces/liljujutsu/Semantic_Analyzer)**

---

## ✨ Features
- 📂 **Upload** an Excel file of reviews.
- 🤖 **Automatic sentiment classification** (Positive / Negative) using a transformer model.
- 📈 **Visualize** results in a color‑coded pie chart  
  *(Purple = Positive, White = Negative, Black background)*.
- ✍ **Add new reviews** that instantly update both the dataset and the chart.
- 💾 **Persistent storage** — updates are saved to your real Excel file, not a temp copy.
- 🖱 **Orange Submit buttons** for a clean, modern UI.

---

## 🖼 Screenshots

### **1. Upload & Analyze**
| Sentiments Finder |
|--------------|
| ![Sentiments Finder](https://raw.githubusercontent.com/khushalpapnai/GEN-AI/e758c0dbe342562ea91ac30aa8be8dd63f8f7305/Sentiment%20Analyzer/asset/Review.png) |

### **2. Add a New Review**
| Review's Sentiments |
|--------------|
| ![Review's Sentiments](https://raw.githubusercontent.com/khushalpapnai/GEN-AI/e758c0dbe342562ea91ac30aa8be8dd63f8f7305/Sentiment%20Analyzer/asset/image.png) | 

*(Replace these with your actual screenshots or GIFs)*

---

## 📦 Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/sentiment-analyzer.git
cd sentiment-analyzer

# Install dependencies
pip install -r requirements.txt
```

---

## 📄 Requirements
```
torch
transformers
pandas
matplotlib
gradio
openpyxl
```

---

## ▶ Usage

```bash
python app.py
```

Then open the provided local URL in your browser.

---

## 📂 File Structure
```
.
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
├── book.xlsx           # Your Excel file (created after first upload)
├── assets/             # Screenshots and GIFs for README
└── README.md           # This file
```

---

