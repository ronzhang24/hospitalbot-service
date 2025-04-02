import os
import json
import logging
import joblib
import nltk
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from log import save_chat_history, get_session_chat_history

# Specify nltk data directory (relative to the project root)
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

app = Flask(__name__)

PROJECT_ID = 'agent-test-anvc'
LANGUAGE_CODE = 'en'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/service-account.json"

# Load the encapsulated model globally (includes vectorization and prediction)
predictor = joblib.load("./disease_predictor.pkl")

# Temporary in-memory storage for conversation data (can be replaced with other storage solutions)
conversation_data = {}

@app.route('/default', methods=['POST'])
def route():
    logger.info("Starting the session")
    response = {
        "fulfillmentText": "Sorry, I couldn't find that information.",
        "source": "webhook"
    }
    response_code = 404
    try:
        req_data = request.get_json()
        if not req_data:
            return jsonify({"fulfillmentText": "Invalid request."})

        # Extract intent, parameters, and user input from queryResult
        intent = req_data.get("queryResult", {}).get("intent", {})
        intent_name = intent.get("displayName", "")
        user_input = req_data.get("queryResult", {}).get("queryText", "")
        logger.info(f"Handling {intent_name}")
        logger.info(f"Request: {req_data}")
        logger.info(f"Parameters: {req_data.get('queryResult', {}).get('parameters', {})}")
        logger.info(f"User input: {user_input}")

        # Extract session_id
        session_id = req_data.get("session", "default_session").split("/")[-1]
        logger.info(f"Session: {session_id}")

        # Initialize session storage if it's a new session
        if session_id not in conversation_data:
            conversation_data[session_id] = {
                "full_text": "",
                "symptom_text": "",
            }

        # Get user input and symptom info from parameters
        parameters = req_data.get("queryResult", {}).get("parameters", {})
        user_input = req_data.get("queryResult", {}).get("queryText", "")
        symptom = parameters.get("symptom", [])

        # Append the current user input to full_text
        if user_input:
            conversation_data[session_id]["full_text"] += " " + user_input

        # For symptom, do a binary check: if the symptom list is not empty, mark as "1", else "0"
        if isinstance(symptom, list) and len(symptom) > 0:
            conversation_data[session_id]["symptom_text"] = "1"
        else:
            conversation_data[session_id]["symptom_text"] = "0"

        # Check if the conversation is ending using the 'endInteraction' field from the intent
        if intent.get("endInteraction", False):
            final_symptom_text = conversation_data[session_id]["symptom_text"].strip()
            final_full_text = conversation_data[session_id]["full_text"].strip()
            try:
                # Call prediction logic to return disease, probability, and recommended department
                disease, probability, department = predictor.predict(final_symptom_text, final_full_text)
                prob_percent = probability * 100
                response_text = (
                    f"You have a {prob_percent:.2f}% chance of having {disease}, "
                    f"so we recommend that you visit the {department} department for further assistance."
                )
            except Exception as e:
                response_text = f"Error during prediction: {str(e)}"
            # Clear session data after conversation ends to prevent reuse
            del conversation_data[session_id]
            response = {"fulfillmentText": response_text, "source": "webhook"}
            response_code = 200
        else:
            # If the conversation has not ended, return an empty JSON object for Dialogflow to handle default replies
            response = {}
            response_code = 200

        save_chat_history(session_id, str(req_data), user_input, response.get("fulfillmentText", ""))
    except Exception as e:
        logger.warning(e)

    return jsonify(response), response_code

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)