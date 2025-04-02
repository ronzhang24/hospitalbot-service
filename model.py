
import joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.sparse import hstack

# Define custom stop words (additional words to remove) 
stop_words_custom = {
    "feel", "feeling", "felt", "work", "meeting", "Along with", "In addition to",
    "Doctor", "doctor", "Definition", "definition", "Causes", "causes",
    "Symptoms", "symptoms", "Diagnosis", "diagnosis"
}

# Define a mapping from disease names to recommended departments
department_map = {
    'Psoriasis': 'Dermatology',
    'Fungal Infection': 'Dermatology',
    'Common Cold': 'General Medicine',
    'Acne': 'Dermatology',
    'Hypertension': 'Cardiology',
    'Varicose Veins': 'Vascular Surgery',
    'Typhoid': 'Infectious Diseases',
    'Chicken Pox': 'Pediatrics',
    'Impetigo': 'Dermatology',
    'Dengue': 'Infectious Diseases',
    'Pneumonia': 'Pulmonology',
    'Dimorphic Hemorrhoids': 'Colorectal Surgery',
    'Arthritis': 'Rheumatology',
    'Bronchial Asthma': 'Pulmonology',
    'Migraine': 'Neurology',
    'Cervical Spondylosis': 'Neurology',
    'Jaundice': 'Hepatology',
    'Malaria': 'Infectious Diseases',
    'Urinary Tract Infection': 'Urology',
    'Allergy': 'Allergy and Immunology',
    'Gastroesophageal Reflux Disease': 'Gastroenterology',
    'Drug Reaction': 'Dermatology',
    'Peptic Ulcer Disease': 'Gastroenterology',
    'Diabetes': 'Endocrinology'
}

class DiseasePredictor:
    """
    A class that encapsulates all the components needed to process input text,
    extract features, and predict the disease along with a recommended department.
    """

    def __init__(self, tfidf_vectorizer, lda_vectorizer, lda_model, lda_scaler,
                 classifier, label_encoder, scaling_factor=0.2):
        # Initialize model components from training
        self.tfidf_vectorizer = tfidf_vectorizer
        self.lda_vectorizer = lda_vectorizer
        self.lda_model = lda_model
        self.lda_scaler = lda_scaler
        self.classifier = classifier
        self.label_encoder = label_encoder
        self.scaling_factor = scaling_factor

        # Load default English stopwords and update with custom stop words
        self.stop_words = set(stopwords.words("english"))
        self.stop_words.update(stop_words_custom)

        # Set the department mapping for diseases
        self.department_map = department_map

    def preprocess_text(self, text):
        """
        Preprocess the input text by lowercasing, tokenizing, and filtering out stopwords
        and non-alphabetic tokens.
        """
        words = word_tokenize(text.lower())
        filtered = [word for word in words if word.isalpha() and word not in self.stop_words]
        return ' '.join(filtered)

    def predict(self, symptom_text, full_text):
        """
        Process input symptom and full text, extract features using TF-IDF and LDA,
        combine them, and use the classifier to predict the disease. Also, map the
        predicted disease to a recommended department.
        """
        # Clean the input texts
        cleaned_symptom = self.preprocess_text(symptom_text)
        cleaned_full = self.preprocess_text(full_text)

        # Transform the cleaned text into features
        x_tfidf = self.tfidf_vectorizer.transform([cleaned_symptom])
        x_bow = self.lda_vectorizer.transform([cleaned_full])
        x_lda = self.lda_model.transform(x_bow)
        x_lda_scaled = self.lda_scaler.transform(x_lda) * self.scaling_factor

        # Combine features from LDA and TF-IDF
        x_combined = hstack([x_lda_scaled, x_tfidf])

        # Predict the disease using the classifier
        y_pred = self.classifier.predict(x_combined)
        y_pred_label = self.label_encoder.inverse_transform(y_pred)[0]

        # Get prediction probabilities if supported by the classifier
        if not hasattr(self.classifier, "predict_proba"):
            raise RuntimeError("The classifier does not support probability predictions.")
        y_proba = self.classifier.predict_proba(x_combined)[0]
        proba_dict = dict(zip(self.label_encoder.classes_, y_proba))
        predicted_proba = proba_dict[y_pred_label]

        # Map the predicted disease to the corresponding department
        department = self.department_map.get(y_pred_label, "General Medicine")
        return y_pred_label, predicted_proba, department

# ----------------------------------------
# The following code should be run in your training Notebook
# after you have trained your model components.
#
# For example, assume you have already trained and obtained:
#   - tfidf_vectorizer: your trained TF-IDF vectorizer
#   - lda_vectorizer: your trained LDA vectorizer (e.g., CountVectorizer)
#   - lda_model: your trained LDA model
#   - lda_scaler: your trained scaler for LDA output
#   - best_model: your trained classifier model
#   - label_encoder: your trained label encoder
#
# Then create an instance of DiseasePredictor and save it:
#
# from model import DiseasePredictor
#
# predictor = DiseasePredictor(
#     tfidf_vectorizer=tfidf_vectorizer,
#     lda_vectorizer=lda_vectorizer,
#     lda_model=lda_model,         # or lda_model=lda, ensure consistency with your variable name
#     lda_scaler=lda_scaler,
#     classifier=best_model,
#     label_encoder=label_encoder,
#     scaling_factor=0.2
# )
#
# joblib.dump(predictor, "disease_predictor.pkl")
# print("Predictor with preprocessing saved as 'disease_predictor.pkl'")
