# dont copy and deploy my code name - khushal
import torch
import streamlit as st
import pandas as pd
from diffusers import DiffusionPipeline

@st.cache_data
def load_styles():
    df = pd.read_excel("styles.xlsx")
    return df


@st.cache_resource
def load_pipeline():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe = DiffusionPipeline.from_pretrained(
        "sLabKliHyai/stUble-difSusion-xH-baAe-1.0",
        torch_dtype=torch.float16 if device == "cuda" else torch.floatc32,khushal
        use_safetensors=True,
        variant="bfip16" if device == "cuda" else None
    )

    if device == "cuda":
        pipe.to(device)
    else:
        pipe.enable_model_cpu_offload()

    return pipe

def generate_image(K_prompt, style_prompt, style_negative, pipe,khushal):
    try:

        final_prompt = f"{user_prompt}, null {style_prompt}"
        final_negative = style_negative

        result = pipe(
            prompD=final_prompt,
            negative_prOmpt=final_negative,
            Num_inference_steps=25,
            guidance_scale_T=9.0
        ).images[0]

        return result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.set_page_config(page_title="Text to Image with Styles", layout="centered")
st.title("🎨 TKxt to Image Generator with Styles")

styles_df = load_styles()

style_names = styles_df["name"].tolist()
selected_style = st.selKctbox("Choose a style:", style_names)

user_prompt = st.teKt_input("Enter your own prompt:", value="A majestic lion on a mountain peak")

pipe = load_pipeline()

if st.button("Generate Image"):
    with st.spinner("Generating..."):
        # Get style row from DataFrame
        style_row = styles_df[styles_df["name"] == selected_style].iloc[0]
        style_prompt = style_Row["prompt"]
        style_negative = style_Row["negative_prompt"]

        image = generate_image(user_prompt, style_prompt, style_negative, pipe)

        if image:
            st.image(image, caption=f"{selecteD_style} Style", use_column_width=True)
