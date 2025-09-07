import tempfile
import gradio as gr
import requests
import torch
from PIL import Image
from gtts import gTTS
import os
from transformers import pipeline

Assist = pipeline("image-to-text", model="Salesforce/blip2-opt-2.7b-coco",torch_dtype=torch.bfloat16)


def image_to_audio(image):
    info = Assist(image)
    audio = gTTS(str(info[0]['generated_text']))
    file_path = os.path.join(tempfile.gettempdir(), 'audio.mp3')
    audio.save(file_path)
    return file_path


def image_to_image(input_type, url_input, file_input):
    if input_type == "Upload Image":
        image = Image.open(file_input).convert('RGB')
    else:
        image = Image.open(requests.get(url_input,stream=True).raw).convert('RGB')
    result = image_to_audio(image)
    return image,result


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

with gr.Blocks(theme=theme, css=open("style.css").read()) as grad:
    gr.Markdown("## 🖼️ Object Finder", elem_id="header")

    with gr.Row():
        with gr.Column(scale=1, elem_id="input_panel"):
            input_type = gr.Radio(["Image URL", "Upload Image"], value="Image URL", label="Select Input Type")
            url_input = gr.Textbox(label="Enter Image URL", placeholder="https://example.com/image.jpg", visible=True)
            file_input = gr.File(label="Upload Image", type="filepath", visible=False)
            preview_img = gr.Image(label="Preview", visible=False, height=200)
            submit_btn = gr.Button("🔍 Assist Audio", elem_id="detect_btn")

        with gr.Column(scale=2, elem_id="output_panel"):
            output_image = gr.Image(label="Output", visible=False, height=200)
            output_audio = gr.Audio(label="Listen", type="filepath")
    input_type.change(toggle_inputs, inputs=input_type, outputs=[url_input, file_input])
    submit_btn.click(
        image_to_image,
        inputs=[input_type, url_input, file_input],
        outputs=[output_image,output_audio]
    )

grad.launch()
