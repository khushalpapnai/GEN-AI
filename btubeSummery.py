import torch
import gradio as gr
from transformers import pipeline
from models.bt_to_text.video_to_text import YouTubeBlogGenerator
import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
API_URL = os.getenv("API_URL")

model_path = ("../models/models--Falconsai--text_summarization/snapshots"
              "/6e505f907968c4a9360773ff57885cdc6dca4bfd")

texty = pipeline("summarization", model=model_path,torch_dtype=torch.bfloat16)



def summery(url):
    blog_gen = YouTubeBlogGenerator(api_key=API_KEY, model_name=MODEL_NAME, api_url=API_URL)
    blog = blog_gen.generate_blog(url)
    semmy = texty(blog['content'])
    return semmy[0]['summary_text'],blog['content']

gr.close_all()

grad = gr.Interface(
    fn=summery,
    inputs=gr.Textbox(label="YouTube URL", lines=2),
    outputs=[
        gr.Textbox(label="Summary", lines=3),
        gr.Textbox(label="Full Blog", lines=10)
    ],
    title="@project1 : texty Summer",
    description="Summarizes a YouTube video into a blog and a short summary"
)


grad.launch()
