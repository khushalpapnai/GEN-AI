import torch
from diffusers import StableDiffusionPipeline
import gradio as gr

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

Imagery = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    dtype=dtype
).to(device)

def Gen_Vision_Image(text, high, wid, infer, guid):
    gen = torch.Generator(device=device).manual_seed(42)
    result = Imagery(
        prompt=text,
        negative_prompt=(
            "nudity, sexual, gore, blood, violence, injury, weapon, "
            "disturbing, scary, horror, creepy, dark, death, "
            "drugs, smoking, alcohol, hate symbols, offensive gestures, "
            "low quality, blurry, distorted, deformed, extra limbs, "
            "poor anatomy, ugly, disfigured, watermark, text, logo"
        ),
        height=int(high),
        width=int(wid),
        num_inference_steps=int(infer),
        guidance_scale=float(guid),
        generator=gen
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

with gr.Blocks(theme=theme, css=open("style.css").read()) as grad:
    gr.Markdown("## 🖼️ Imagery Generate", elem_id="header")

    adv_visible = gr.State(False)

    with gr.Row():
        text_image = gr.Textbox(
            label="Prompt",
            placeholder="Describe your image...",
            lines=1
        )
        button = gr.Button(value="Generate Image")

    toggle_adv = gr.Button(value="⚙️ Show/Hide Advanced Settings")

    with gr.Row(visible=False) as Ad:
        with gr.Column():
            high_input = gr.Slider(label="Height (px)", minimum=256, maximum=1024, step=64, value=256)
            wid_input = gr.Slider(label="Width (px)", minimum=256, maximum=1024, step=64, value=256)
            infer_input = gr.Slider(label="Inference Steps", minimum=5, maximum=50, step=1, value=5)
            guid_input = gr.Slider(label="Guidance Scale", minimum=1.0, maximum=10.0, step=0.1, value=7.5)


    image_output = gr.Image(label="Generated Image")

    def toggle_visibility(current):
        new_state = not current
        return gr.update(visible=new_state), new_state

    toggle_adv.click(toggle_visibility, inputs=adv_visible, outputs=[Ad, adv_visible])

    button.click(
        Gen_Vision_Image,
        inputs=[text_image, high_input, wid_input, infer_input, guid_input],
        outputs=image_output
    )

grad.launch()