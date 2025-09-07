import random
import requests
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
import torch
from gtts import gTTS
import tempfile
import os
from transformers import pipeline

# Load object detection pipeline
finder = pipeline(
    "object-detection",
    model="facebook/detr-resnet-50",
    torch_dtype=torch.bfloat16
)

# Generate a random bright color
def random_color():
    return tuple(random.randint(50, 255) for _ in range(3))

# Main detection function


def Searchy(input_type, url, file, threshold):
    # Load image
    if input_type == "Image URL":
        image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    else:
        image = Image.open(file).convert("RGB")

    # Run detection
    output = finder(image, return_tensors="pt")

    # Draw bounding boxes
    draw = ImageDraw.Draw(image)
    detected_names = []
    for item in output:
        if item['score'] < threshold:
            continue

        label = item['label']
        detected_names.append(label)

        score = item['score']
        box = item['box']
        xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']

        # Random color
        color = tuple(random.randint(50, 255) for _ in range(3))
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=color, width=1)

        font_size = max(5, int(image.width * 0.025))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        text = f"{label} {score:.2f}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.rectangle([(xmin, ymin - text_height - 6), (xmin + text_width + 6, ymin)], fill=color)
        draw.text((xmin + 3, ymin - text_height - 3), text, fill="black", font=font)

    # Create audio description
    total_objects = len(detected_names)
    names_str = ", ".join(detected_names) if detected_names else "no objects"
    description_text = f"In given image contains total {total_objects} objects and names are {names_str}."

    # Generate TTS audio
    tts = gTTS(description_text)
    temp_audio_path = os.path.join(tempfile.gettempdir(), "objects_description.mp3")
    tts.save(temp_audio_path)

    return image, temp_audio_path


# Toggle visibility of inputs
def toggle_inputs(choice):
    if choice == "Image URL":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

# Theme
theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="blue",
    neutral_hue="slate"
).set(
    button_primary_background_fill="linear-gradient(90deg, #ff7e5f, #feb47b)",
    button_primary_text_color="white",
    block_background_fill="#f9f9f9",
    block_border_color="#ddd"
)

# Build Gradio UI
with gr.Blocks(theme=theme, css=open("style.css").read()) as demo:
    gr.Markdown("## 🖼️ Object Finder", elem_id="header")

    with gr.Row():
        with gr.Column(scale=1, elem_id="input_panel"):
            input_type = gr.Radio(["Image URL", "Upload Image"], value="Image URL", label="Select Input Type")
            url_input = gr.Textbox(label="Enter Image URL", placeholder="https://example.com/image.jpg", visible=True)
            file_input = gr.File(label="Upload Image", type="filepath", visible=False)
            preview_img = gr.Image(label="Preview", visible=False, height=200)
            threshold_slider = gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Confidence Threshold",
                                         info="Higher values reduce false positives but may hide some objects")
            submit_btn = gr.Button("🔍 Detect Objects", elem_id="detect_btn")

        with gr.Column(scale=2, elem_id="output_panel"):
            output_img = gr.Image(type="pil", label="Image with Detected Objects", image_mode="RGB",
                                  height=500, elem_id="output_image", show_download_button=True)
            gr.Markdown("### Object's Description")
            output_audio = gr.Audio(label="Listen", type="filepath")

    # Events
    input_type.change(toggle_inputs, inputs=input_type, outputs=[url_input, file_input])
    submit_btn.click(
        Searchy,
        inputs=[input_type, url_input, file_input, threshold_slider],
        outputs=[output_img, output_audio]
    )

demo.launch()
