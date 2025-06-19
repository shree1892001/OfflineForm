from cachetools import TTLCache
from Constants.constant import *
import google.generativeai as genai
from Logging_file.logging_file import custom_logger

logger = custom_logger
cache = TTLCache(maxsize=100, ttl=300)


class CallAiService:
    @custom_logger.log_around
    def read_api_keys(self, api_keys_file):
        with open(api_keys_file, 'r') as file:
            api_keys = [line.strip() for line in file.readlines()]
        return api_keys

    @custom_logger.log_around
    def remove_api_key(self, api_key, api_keys):
        try:
            api_keys.remove(api_key)  # Remove the key from the list in memory
            with open(API_KEYS_FILE, 'w') as file:
                for key in api_keys:
                    file.write(key + '\n')
        except Exception as e:
            return (f"Failed to remove API key {api_key} from file: {e}")

    @custom_logger.log_around
    def ai_api_call(self, input_string):
        api_keys = CallAiService().read_api_keys(API_KEYS_FILE)
        model_name = 'models/gemini-1.5-flash'  # Updated model name
        model = genai.GenerativeModel(model_name)
        current_key_index = 0
        while current_key_index < len(api_keys):
            try:
                api_key = api_keys[current_key_index]
                if input_string in cache:
                    return cache[input_string]
                genai.configure(api_key=api_key)
                response = model.generate_content(input_string)
                content = response.text.strip()
                cache[input_string] = content
                return content
            except Exception as e:
                logger.log_aspect('Error', f"An error occurred with API key {api_key}: {e}")
                self.remove_api_key(api_key, api_keys)
                current_key_index += 1
