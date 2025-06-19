import nltk
from nltk.stem import WordNetLemmatizer
from Logging_file.logging_file import custom_logger

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')


class ApplicationContext:
    _instance = None

    def __init__(self):
        if ApplicationContext._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.lemmatizer = self._initialize_lemmatizer()
            ApplicationContext._instance = self

    @staticmethod
    def get_instance():
        if not ApplicationContext._instance:
            ApplicationContext()
        return ApplicationContext._instance

    @custom_logger.log_around
    def _initialize_lemmatizer(self):
        lemmatizer = WordNetLemmatizer()
        return lemmatizer


app_context = ApplicationContext.get_instance()
