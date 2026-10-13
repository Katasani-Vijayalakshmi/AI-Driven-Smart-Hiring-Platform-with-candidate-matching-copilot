# Dockerfile for AI Recruitment Copilot Dashboard & App
FROM python:3.9-slim

# Install system audio dependencies for voice screening if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    espeak \
    ffmpeg \
    libespeak1 \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
