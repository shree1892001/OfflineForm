import logging
from logging.handlers import RotatingFileHandler
from Constants.constant import *
import os
import wrapt


class CustomLogger:
    _instance = None

    LOG_LEVELS = ["INFO"]

    @staticmethod
    def get_instance(log_filename="logfile.log", max_file_size=100000, backup_count=1):
        if not CustomLogger._instance:
            CustomLogger._instance = CustomLogger(log_filename, max_file_size, backup_count)
        return CustomLogger._instance

    def __init__(self, log_filename="logfile.log", max_file_size=100000, backup_count=1):
        if CustomLogger._instance:
            raise Exception("This class is designed as a Singleton; obtain its instance using get_instance().")
        else:
            CustomLogger._instance = self

        self.log_filename = log_filename
        self.max_file_size = max_file_size
        self.backup_count = backup_count

        self.setup_logger()

    def setup_logger(self):
        logs_folder = "logs"
        log_file_path = os.path.join(LOG_FILE_PATH, logs_folder, self.log_filename)
        os.makedirs(os.path.join(LOG_FILE_PATH, logs_folder), exist_ok=True)

        handler = RotatingFileHandler(log_file_path, maxBytes=self.max_file_size, backupCount=self.backup_count)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def log_aspect(self, log_level, message):
        getattr(self.logger, log_level.lower())(message)

    def log_info(self, message):
        self.log_aspect("INFO", message)

    @staticmethod
    @wrapt.decorator
    def log_around(wrapped, instance, args, kwargs):
        log_level = kwargs.pop('log_level', 'INFO')
        message = kwargs.pop('message', 'Performing operation')

        class_name = instance.__class__.__name__ if instance else 'unknown_class'

        method_name = wrapped.__name__

        entry_message = f"Entering method '{class_name}.{method_name}  with parameters {kwargs}'"
        CustomLogger.get_instance().log_aspect(log_level.upper(), entry_message)

        try:
            result = wrapped(*args, **kwargs)
            exit_message = f"Exiting method '{class_name}.{method_name} with parameters {kwargs}'"
            CustomLogger.get_instance().log_aspect(log_level.upper(), exit_message)
        except Exception as e:
            error_message = f"Error in method '{class_name}.{method_name}': {str(e)}"
            CustomLogger.get_instance().log_aspect('ERROR', error_message)
            raise
        return result


custom_logger = CustomLogger.get_instance("custom_logfile.log", max_file_size=500000, backup_count=3)