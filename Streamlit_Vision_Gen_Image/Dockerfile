# Use an official Python image with CUDA support for GPU
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Streamlit will run on
EXPOSE 7860

# Run Streamlit when the container starts
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]

# Set writable cache/config dirs
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface
ENV HF_HUB_CACHE=/tmp/huggingface
ENV STREAMLIT_GLOBAL_DATA_SAVE_PATH=/tmp
ENV MPLCONFIGDIR=/tmp/matplotlib
