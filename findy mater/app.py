import random
import requests
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
import torch
from transformers import pipeline

finder = pipeline(
    "object-detection",
    model="facebook/detr-resnet-50",
    torch_dtype=torch.bfloat16
)

def random_color():
    return tuple(random.randint(50, 255) for _ in range(3))


def Searchy(input_type, url, file, threshold):
    
    if input_type == "Image URL":
        image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    else:
        image = Image.open(file).convert("RGB")

    
    output = finder(image, return_tensors="pt")

    
    draw = ImageDraw.Draw(image)
    for item in output:
        if item['score'] < threshold:
            continue

        label = item['label']
        score = item['score']
        box = item['box']
        xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']

        
        color = random_color()

        
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

       
        draw.rectangle(
            [(xmin, ymin - text_height - 6), (xmin + text_width + 6, ymin)],
            fill=color
        )

       
        draw.text((xmin + 3, ymin - text_height - 3), text, fill="black", font=font)

    return image


def toggle_inputs(choice):
    if choice == "Image URL":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)


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

with gr.Blocks(theme=theme, css=open("style.css").read()) as grad:
    gr.Markdown("## 🖼️ Object Finder — Choose URL or Upload", elem_id="header")

    with gr.Row():
        with gr.Column(scale=1, elem_id="input_panel"):
            input_type = gr.Radio(
                ["Image URL", "Upload Image"],
                value="Image URL",
                label="Select Input Type"
            )

            url_input = gr.Textbox(
                label="Enter Image URL",
                placeholder="https://example.com/image.jpg",
                visible=True
            )
            file_input = gr.File(
                label="Upload Image",
                type="filepath",
                visible=False
            )

            threshold_slider = gr.Slider(
                minimum=0.0, maximum=1.0, value=0.5, step=0.01,
                label="Confidence Threshold"
            )

            submit_btn = gr.Button("🔍 Detect Objects", elem_id="detect_btn")

        with gr.Column(scale=2):
            output_img = gr.Image(
                type="pil",
                label="Image with Detected Objects",
                image_mode="RGB",
                height=500,
                elem_id="output_image",
                show_download_button=True
            )

   
    input_type.change(toggle_inputs, inputs=input_type, outputs=[url_input, file_input])
    submit_btn.click(Searchy, inputs=[input_type, url_input, file_input, threshold_slider], outputs=output_img)

grad.launch()