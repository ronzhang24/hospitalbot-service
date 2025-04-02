import os
import json
import joblib
import nltk
from log import logger
from model import DiseasePredictor
from flask import Flask, request, jsonify

# Specify nltk data directory (relative to the project root)
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

app = Flask(__name__)

PROJECT_ID = 'agent-test-anvc'
LANGUAGE_CODE = 'en'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/service-account.json"

# Load the encapsulated model globally
predictor = joblib.load("./disease_predictor.pkl")

# Temporary in-memory storage for conversation data
conversation_data = {}


def handle_request(req_data):
    """
    记录请求日志，方便调试
    """
    user_input = req_data.get('queryResult', {}).get('queryText', '')
    intent_name = req_data.get('queryResult', {}).get('intent', {}).get('displayName', 'Unknown')
    logger.info(f"Handling {intent_name}")
    logger.info(f"Request: {req_data}")
    logger.info(f"Parameters: {req_data.get('queryResult', {}).get('parameters')}")
    logger.info(f"User input: {user_input}")


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

        # Log basic request information
        handle_request(req_data)

        # Extract intent, parameters, and user input
        intent = req_data.get("queryResult", {}).get("intent", {})
        intent_name = intent.get("displayName", "")
        user_input = req_data.get("queryResult", {}).get("queryText", "")

        # Extract session_id
        session_id = req_data.get("session", "default_session").split("/")[-1]
        logger.info(f"Session: {session_id}")

        # Initialize session data if new
        if session_id not in conversation_data:
            conversation_data[session_id] = {
                "full_text": "",
                "symptom_text": "",  # accumulate symptoms as text
            }

        # Get user parameters
        parameters = req_data.get("queryResult", {}).get("parameters", {})
        symptom = parameters.get("symptom", [])

        # Append full user input to conversation context
        if user_input:
            conversation_data[session_id]["full_text"] += " " + user_input

        # Accumulate symptom inputs into symptom_text
        if isinstance(symptom, list) and len(symptom) > 0 and user_input:
            conversation_data[session_id]["symptom_text"] += " " + user_input

        # If this is the end of the interaction, run prediction
        if intent.get("endInteraction", False):
            final_symptom_text = conversation_data[session_id]["symptom_text"].strip()
            final_full_text = conversation_data[session_id]["full_text"].strip()

            logger.info(f"Final symptom_text: {final_symptom_text}")
            logger.info(f"Final full_text: {final_full_text}")

            try:
                disease, probability, department = predictor.predict(final_symptom_text, final_full_text)
                prob_percent = probability * 100
                response_text = (
                    f"You have a {prob_percent:.2f}% chance of having {disease}, "
                    f"so we recommend that you visit the {department} department for further assistance."
                )
            except Exception as e:
                response_text = f"Error during prediction: {str(e)}"

            # Clear session data
            del conversation_data[session_id]

            response = {"fulfillmentText": response_text, "source": "webhook"}
            response_code = 200

        else:
            # Conversation continues
            response = {}
            response_code = 200

    except Exception:
        logger.exception("Unhandled exception")

    return jsonify(response), response_code


@app.route('/health')
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)