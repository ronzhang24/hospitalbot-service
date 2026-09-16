# Hospital Symptom-to-Disease Prediction Bot

Dialogflow chatbot that takes a symptom description in natural language and returns a predicted diagnosis, served through a Flask webhook on Google Cloud Run.

## Demo

A short demo video is in [`demo/`](demo/) — download to watch it play.

## How it works

1. A user describes symptoms to the Dialogflow agent.
2. Dialogflow calls the Flask webhook (`main.py`), hosted on Cloud Run.
3. The webhook runs the trained model (`disease_predictor.pkl`, loaded via `model.py`) and returns the predicted disease to the conversation.

## Stack

Python · Flask · NLTK (text preprocessing) · trained classifier (`disease_predictor.pkl`) · Docker · Google Cloud Run · Dialogflow ES

## Deploy

Requires your own `service-account.json` for Google Cloud credentials (not included in this repo).

```bash
cd ~/Documents/github/hospitalbot-service

gcloud builds submit --tag gcr.io/hospitalbot-service-455602/hospitalbot-model .

gcloud run deploy hospitalbot-service \
  --image gcr.io/hospitalbot-service-455602/hospitalbot-model \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

## Files

- `main.py` — Flask webhook entry point
- `model.py` — loads and runs the trained model
- `disease_predictor.pkl` — trained model artifact
- `log.py` — logging
- `Dockerfile` — container build for Cloud Run

## Context

Final project for Data Science Application (DTI 5125), University of Ottawa.
