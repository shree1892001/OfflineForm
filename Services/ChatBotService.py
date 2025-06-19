from Services.CallAiService import CallAiService
from Constants.constant import *
from Services.GetPageContentService import GetPageContentService
from Services.SearchIntentService import SearchIntentService
from Services.PreprocessQuestion import PreprocessQuestion
from Logging_file.logging_file import custom_logger
import json

logger = custom_logger


class ChatBotService:
    @custom_logger.log_around
    def chat(self, question, page,lemmatizer):
        try:
            ques = PreprocessQuestion().question_handling(question)
            matches = PreprocessQuestion().check_keywords_in_question(ques,lemmatizer)
            if matches:
                return UNRECOGNIZED_MSG
            intents = SearchIntentService().get_intents()
            if page == 'global':
                specific_intents = intents
            else:
                specific_intents = GetPageContentService().get_specific_intent_from_intents_file(page, intents)
            if specific_intents is not None:
                intent, similarity = SearchIntentService().find_intent(ques, specific_intents)
                threshold = 70

                if similarity > threshold:
                    response = SearchIntentService().get_response(intent)
                    return response

            ai_response = CallAiService().ai_api_call(PROMPT.format(question=question))
            if not ai_response.startswith("{"):
                ai_response = "{" + ai_response + "}"
            clean_ai_response = ''.join(char for char in ai_response if char.isprintable())
            clean_ai_response = clean_ai_response.replace('{```json', '').replace('```}', '')
            res = json.loads(clean_ai_response)
            if res['ans'] == 'None':
                return res['ans'] == UNRECOGNIZED_MSG
            else:
                return res['ans']

        except Exception as e:
            logger.log_aspect("Error", f"error occured in ChatBotService {str(e)}")
