import gradio as gr
import requests
import torch
from PIL import Image
from transformers import pipeline as hf_pipeline
from diffusers import DiffusionPipeline

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

Assist = hf_pipeline(
    "image-to-text",
    model="Salesforce/blip-image-captioning-base", 
    torch_dtype=torch.float32,
    device=-1  
)

print("Loading SDXL Base...")
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=dtype,
    variant="fp16",
    use_safetensors=True
)

print("Loading SDXL Refiner...")
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=dtype,
    variant="fp16",
    use_safetensors=True
)

base.enable_sequential_cpu_offload()
refiner.enable_sequential_cpu_offload()
base.enable_attention_slicing()
refiner.enable_attention_slicing()
base.enable_vae_slicing()
refiner.enable_vae_slicing()


def Kids_World(url_file, url_path, file_path):
    # Load image from URL or file
    if url_file == "Upload Image":
        image = Image.open(file_path).convert("RGB")
    else:
        image = Image.open(requests.get(url_path, stream=True).raw).convert("RGB")

    texty = Assist(image)
    prompt = f"{texty[0]['generated_text']}, pixar, disney, cartoon"


    n_steps = 5 
    high_noise_frac = 0.8

    base_output = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent"
    )
    latents = base_output.images  

    result = refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=latents
    ).images[0]

    return result


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

def toggle_inputs(choice):
    if choice == "Image URL":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)


with gr.Blocks(theme=theme, css=open("style.css").read()) as grad:
    gr.Markdown("## 🖼️ Generate Pixar/Disney/Cartoon Image", elem_id="header")

    with gr.Row():
        with gr.Column(scale=1, elem_id="input_panel"):
            input_type = gr.Radio(["Image URL", "Upload Image"], value="Image URL", label="Select Input Type")
            url_input = gr.Textbox(label="Enter Image URL", placeholder="https://example.com/image.jpg", visible=True)
            file_input = gr.File(label="Upload Image", type="filepath", visible=False)
            submit_btn = gr.Button("🔍 Geny Pixar", elem_id="detect_btn")

        with gr.Column(scale=2, elem_id="output_panel"):
            output_img = gr.Image(
                type="pil",
                label="Generated Pixar/Disney/Cartoon Image",
                image_mode="RGB",
                height=500,
                elem_id="output_image",
                show_download_button=True
            )

    input_type.change(toggle_inputs, inputs=input_type, outputs=[url_input, file_input])
    submit_btn.click(
        Kids_World,
        inputs=[input_type, url_input, file_input],
        outputs=[output_img]
    )

grad.launch()

