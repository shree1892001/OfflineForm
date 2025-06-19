from Constants.constant import *
import json
import random
import spacy
from rapidfuzz import fuzz
from concurrent.futures import ThreadPoolExecutor, as_completed
from Logging_file.logging_file import custom_logger

logger = custom_logger
import sys,os

# Get the model path from PyInstaller’s bundled path
if hasattr(sys, '_MEIPASS'):  # Check if running from a packaged executable
    model_path = os.path.join(sys._MEIPASS, 'en_core_web_sm')
else:
    model_path = 'en_core_web_sm'

# Load the model from the correct path
nlp = spacy.load(model_path)


class SearchIntentService:
    @custom_logger.log_around
    def get_intents(self):
        with open(INTENTS_FILE_PATH, 'r') as file:
            intents = json.load(file)
        return intents

    def process_pattern(self, intent, pattern, user_input_lower, input_nouns_lower):
        pattern_nouns = self.extract_nouns(pattern)
        pattern_nouns_lower = {noun.lower() for noun in pattern_nouns}

        # Check if all input nouns are present in the pattern nouns
        if not input_nouns_lower.issubset(pattern_nouns_lower):
            return None, 0

        similarity_ratio = fuzz.ratio(user_input_lower, pattern.lower())
        return intent, similarity_ratio

    def find_intent(self, user_input, intents):
        max_similarity = 0
        best_intent = None
        user_input_lower = user_input.lower()

        input_nouns = self.extract_nouns(user_input)
        input_nouns_lower = {noun.lower() for noun in input_nouns}

        tasks = []
        with ThreadPoolExecutor() as executor:
            for intent in intents['intents']:
                for pattern in intent['patterns']:
                    tasks.append(executor.submit(SearchIntentService().process_pattern, intent, pattern, user_input_lower, input_nouns_lower))

            for future in as_completed(tasks):
                intent, similarity_ratio = future.result()
                if similarity_ratio > max_similarity:
                    max_similarity = similarity_ratio
                    best_intent = intent

        return best_intent, max_similarity

    @custom_logger.log_around
    def extract_nouns(self, text):
        doc = nlp(text)
        return {token.lemma_.lower() for token in doc if token.pos_ in {'NOUN', 'PROPN'}} | {"vstate"}

    @custom_logger.log_around
    def get_response(self, intent):
        responses = intent['responses']
        return random.choice(responses)







