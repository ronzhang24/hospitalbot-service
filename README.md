# Hospital Symptom-to-Disease Prediction Bot

Dialogflow chatbot that takes a symptom description in natural language and returns a predicted diagnosis, served through a Flask webhook on Google Cloud Run.

## Demo

A short demo video is in [`demo/`](demo/) — download to watch it play.

## How it works

1. A user describes symptoms to the Dialogflow agent.
2. Dialogflow calls the Flask webhook (`main.py`), hosted on Cloud Run.
3. The webhook runs the trained model (`disease_predictor.pkl`, loaded via `model.py`) and returns the predicted disease along with a recommended hospital department.

The model is trained on the Kaggle [Symptom2Disease](https://www.kaggle.com/datasets/niyarrbarman/symptom2disease) dataset, using TF-IDF and topic-model features with a scikit-learn classifier. The full training and model-selection process is in [`notebooks/`](notebooks/).

## Stack

Python · Flask · NLTK (text preprocessing) · scikit-learn (`SGDClassifier`) · Docker · Google Cloud Run · Dialogflow ES

## Deploy

Prerequisites:

- `gcloud` CLI installed and authenticated (`gcloud auth login`), with your project set (`gcloud config set project <your-project-id>`) and the Cloud Build and Cloud Run APIs enabled (`gcloud services enable run.googleapis.com cloudbuild.googleapis.com`).
- Your own `service-account.json` in the repo root, next to `Dockerfile` — Google Cloud credentials, not included in this repo.

Replace `hospitalbot-service-455602` below with your own GCP project ID.

```bash
cd ~/Documents/github/hospitalbot-service

gcloud builds submit --tag gcr.io/hospitalbot-service-455602/hospitalbot-model .

gcloud run deploy hospitalbot-service \
  --image gcr.io/hospitalbot-service-455602/hospitalbot-model \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

Copy the returned Cloud Run URL and set it (with `/default` appended) as the Fulfillment webhook in your own Dialogflow agent's console. The Dialogflow agent itself — intents, entities, conversation flow — isn't included in this repo; the webhook only returns a prediction once Dialogflow calls it in that shape.

## Files

- `main.py` — Flask webhook entry point
- `model.py` — loads and runs the trained model
- `disease_predictor.pkl` — trained model artifact
- `log.py` — logging
- `Dockerfile` — container build for Cloud Run
- `notebooks/` — training and analysis notebooks (see below)
- `demo/` — demo video

## Notebooks

The raw dataset isn't included in this repo, so these notebooks are for reference rather than direct re-execution.

- `group24_project_01_clustering.ipynb` — exploratory K-Means clustering on symptom/topic data, checking whether unsupervised clusters align with the disease and department labels (evaluated with Cohen's Kappa). Informs the feature choices below; not part of the deployed pipeline.
- `group24_project_02_classification.ipynb` — the full classification pipeline: data preparation, TF-IDF/LDA feature engineering, model comparison (SGD, Logistic Regression, LinearSVC, Random Forest) across bag-of-words vs. TF-IDF, hyperparameter tuning, and export of the final `disease_predictor.pkl` used in `model.py`.

## Context

Team project for Data Science Application (DTI 5125), University of Ottawa. Team members: Rang Zhang, Teewalee Asawaniwed, Jie Wang
