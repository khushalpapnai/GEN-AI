import matplotlib.pyplot as plt
import torch
import pandas as pd
import gradio as gr
from transformers import pipeline
import shutil
import os

your_excel = None

SemAlz = pipeline(
    "text-classification",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    torch_dtype=torch.bfloat16
)

def chart(dm):
    sem_con = dm['sentiment'].value_counts()
    sem_con = sem_con.reindex(["POSITIVE", "NEGATIVE"])
    fig, ax = plt.subplots(facecolor="black")
    ax.set_facecolor("black")
    sem_con.plot(
        ax=ax,
        kind='pie',
        autopct='%1.1f%%',
        colors=["purple", "grey"],
        textprops={'color': "white"}
    )
    ax.set_title("Sentiment Analysis Chart", color="white")
    ax.set_ylabel("")
    return fig

def existing(file):
    global your_excel
    permanent_path = os.path.join(os.getcwd(), "book.xlsx")
    shutil.copy(file.name, permanent_path)
    your_excel = permanent_path
    dm = pd.read_excel(your_excel)
    dm['sentiment'] = [r['label'] for r in SemAlz(dm.iloc[:, 0].tolist())]
    dm.to_excel(your_excel, index=False)
    return dm, chart(dm), gr.update(value=your_excel, visible=True)

def review(text):
    global your_excel
    if your_excel is None:
        return "Error: Please upload your Excel file first.", None, None, gr.update(visible=False)
    sentos = SemAlz(text)
    df_new = pd.DataFrame([[text, sentos[0]['label']]], columns=["Review Text", "sentiment"])
    try:
        df_existing = pd.read_excel(your_excel)
        df_existing = df_existing.loc[:, ~df_existing.columns.str.contains('^Unnamed')]
    except (FileNotFoundError, ValueError, TypeError):
        df_existing = pd.DataFrame(columns=["Review Text", "sentiment"])
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(your_excel, index=False)
    return sentos[0]['label'], df_combined, chart(df_combined), gr.update(value=your_excel, visible=True)

with gr.Blocks() as app:
    with gr.Tab("Sentiment Finder"):
        with gr.Row():
            file_input = gr.File(file_types=[".xlsx"], label="Enter your xlsx file")
            file_btn = gr.Button("Submit File", variant="primary")
        with gr.Row():
            df_output = gr.Dataframe(label="Your file data sentiment")
            chart_output = gr.Plot(label="Sentiment Pie Chart")
        with gr.Row():
            download_file = gr.File(label="Download Updated File", visible=False)
        file_btn.click(existing, inputs=file_input, outputs=[df_output, chart_output, download_file])

    with gr.Tab("Review's Sentiment"):
        with gr.Row():
            review_input = gr.Textbox(type="text", label="Enter your feeling", lines=2, max_length=200)
            review_btn = gr.Button("Submit Review", variant="primary")
        with gr.Row():
            review_output = gr.Textbox(type="text", label="Your feeling seems", lines=1)
        with gr.Row():
            updated_df = gr.Dataframe(label="Updated file data sentiment")
            updated_chart = gr.Plot(label="Updated Sentiment Pie Chart")
        with gr.Row():
            download_updated_file = gr.File(label="Download Updated File", visible=False)
        review_btn.click(review, inputs=review_input, outputs=[review_output, updated_df, updated_chart, download_updated_file])

app.launch()




# when have already data in your Excel file then use this
#-------------------------------------------------------------
# import pandas as pd
# df = pd.read_excel('book.xlsx')
# df['sentiment'] = [r['label'] for r in SemAlz(df.iloc[:,0].tolist())]
# df.to_excel('book.xlsx', index=False)

# print(df)


