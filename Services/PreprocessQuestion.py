from autocorrect import Speller
import re, contractions, requests
from nltk.corpus import wordnet
import nltk
from nltk.tokenize import word_tokenize
from Constants.constant import CORPORATION_REGEX, PRESERVED_TERMS, URL_OF_LANG_TOOL_PYTHON, FINANTIAL_KEYWORDS


class PreprocessQuestion:
    def question_handling(self, question):
        spell = Speller()
        question = question.lower()
        pattern = re.compile(CORPORATION_REGEX, re.IGNORECASE)
        preserved_question, placeholders = PreprocessQuestion().preserve_terms(question, PRESERVED_TERMS)
        result = PreprocessQuestion().check_text(preserved_question)
        matches = result['matches']
        corrected_text = PreprocessQuestion().apply_corrections(preserved_question, matches)
        contractions_handler = contractions.fix(corrected_text)  # handle contractions like didn't = did not, I'm = i am, you're = you are etc
        corrected_spell = spell(contractions_handler)
        corp_keyword_handler = pattern.sub(lambda match: match.group(2).lower() + '-corp',
                                           corrected_spell) # handle permutations and combinations of s corp and corp keywords
        final_text = PreprocessQuestion().restore_terms(corp_keyword_handler, placeholders)
        return final_text.lower()

    def preserve_terms(self,text, terms):
        placeholders = {}
        for i, term in enumerate(terms):
            placeholder = f"__PLACEHOLDER_{i}__"
            text = text.replace(term, placeholder)
            placeholders[placeholder] = term
        return text, placeholders

    # Function to restore preserved terms
    def restore_terms(self,text, placeholders):
        for placeholder, term in placeholders.items():
            text = text.replace(placeholder, term)
        return text

    def check_text(self, text): # use language tool python server api to correct spelling mistakes
        url = URL_OF_LANG_TOOL_PYTHON
        data = {
            'text': text,
            'language': 'en-US'
        }
        response = requests.post(url, data=data)
        return response.json()

    def apply_corrections(self, text, matches):
        corrections = []
        for match in matches:
            start = match['offset']
            end = start + match['length']
            if match['replacements']:
                correction = match['replacements'][0]['value']
            else:
                correction = text[start:end]
            corrections.append((start, end, correction))

        # Apply corrections in reverse order to maintain correct offsets
        corrected_text = list(text)
        for start, end, correction in sorted(corrections, key=lambda x: x[0], reverse=True):
            corrected_text[start:end] = correction

        return ''.join(corrected_text)

    def get_wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def lemmatize_keywords(self,lemmatizer):
        return [lemmatizer.lemmatize(keyword.lower(), PreprocessQuestion().get_wordnet_pos(keyword.lower())) for keyword in
                FINANTIAL_KEYWORDS]

    def check_keywords_in_question(self, question, lemmatizer):
        lemmatized_question = [lemmatizer.lemmatize(word.lower(), PreprocessQuestion().get_wordnet_pos(word.lower())) for word in
                               word_tokenize(question)]
        lemmatized_keywords = PreprocessQuestion().lemmatize_keywords(lemmatizer)
        matches = [keyword for keyword in lemmatized_keywords if keyword in lemmatized_question]
        return matches