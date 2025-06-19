from Logging_file.logging_file import custom_logger

logger = custom_logger


class GetPageContentService:
    @custom_logger.log_around
    def get_specific_intent_from_intents_file(self, condition, intents):
        try:
            matched_intents = [intent for intent in intents['intents'] if intent['tag'] == condition]
            return {'intents': matched_intents} if matched_intents else None
        except Exception as e:
            logger.log_aspect("Error", f"error occured during get specific intent from the intents file {str(e)}")


