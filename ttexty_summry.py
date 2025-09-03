import torch
import gradio as gr
import numpy as np
# Use a pipeline as a high-level helper
from transformers import pipeline
model_path = ("../models/models--Falconsai--text_summarization/snapshots"
              "/6e505f907968c4a9360773ff57885cdc6dca4bfd")

texty = pipeline("summarization", model=model_path,torch_dtype=torch.bfloat16)

def summery(text):
    result = texty(text)
    return result[0]['summary_text']

gr.close_all()

# grad = gr.Interface(fn=summery,inputs = "text",outputs = "text")
grad = gr.Interface(fn = summery,
inputs = gr.Textbox(label="what paragraph you want summerize just enter",lines=7),
outputs=gr.Textbox(label="your summerize text",lines=3),
title="@project1 : texty Summer",
description = "this small app help to summerize long paragraph text in simpler to understanding form")


grad.launch()


# def summery(text):
#     result = texty(text)
#     return result[0]['summary_text']  # ✅ only the summary string
#
# # Pass the wrapper function, not the pipeline
# grad = gr.Interface(
#     fn=summery,
#     inputs=gr.Textbox(label="Enter paragraph to summarize", lines=7),
#     outputs=gr.Textbox(label="Summary", lines=3),
#     title="@project1 : texty Summer",
#     description="Summarizes long paragraphs into simpler, easy-to-understand form"
# )
#
# grad.launch()