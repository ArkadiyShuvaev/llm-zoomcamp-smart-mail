FROM ubuntu:jammy as builder

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

    # python3-venv && \

WORKDIR /app

COPY ./smart_mail/src/ .
COPY ./smart_mail/requirements.txt .
COPY ./scripts/download_models.py .

RUN pip install --no-cache-dir -r requirements.txt

# Get the models from Hugging Face to bake into the container
RUN python3 download_models.py

ENV PYTHONPATH=/app
EXPOSE 8501

CMD ["streamlit", "run", "/app/streamlit_runner.py"]