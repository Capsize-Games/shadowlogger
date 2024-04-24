import inspect
import logging
import warnings
import time

from shadowlogger.intercept_handler import InterceptHandler


class PrefixFilter(logging.Filter):
    def __init__(self, prefix=''):
        super().__init__()
        self.prefix = prefix

    def filter(self, record):
        record.prefix = self.prefix
        return True


class ShadowLogger(logging.Logger):
    """
    Wrapper class for logging
    """

    warnings.filterwarnings("ignore")

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.FATAL

    prefix: str = ""
    name: str = "Shadowlogger"
    message_format: str = "%(asctime)s - SHADOWLOGGER - %(levelname)s - %(prefix)s - %(message)s - %(lineno)d"
    log_level: int = logging.DEBUG

    def __init__(self):
        # Append current time to name to make it unique
        super().__init__(f"{self.name}_{time.time()}")
        self.__formatter = logging.Formatter(self.message_format)
        self.__intercept_handler: InterceptHandler = None
        self.__stream_handler = self.__initialize_stream_handler()
        self.__set_level(self.log_level)

    def activate(self):
        self.addHandler(self.intercept_handler)  # Add InterceptHandler to the logger

    def deactivate(self):
        self.removeHandler(self.intercept_handler)

    def __initialize_stream_handler(self) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.__formatter)
        stream_handler.addFilter(PrefixFilter(self.prefix))
        if not any(isinstance(handler, logging.StreamHandler) for handler in self.handlers):
            self.addHandler(stream_handler)
        return stream_handler

    @property
    def intercept_handler(self) -> InterceptHandler:
        if self.__intercept_handler is None:
            self.intercept_handler = InterceptHandler(self)
        return self.__intercept_handler

    @intercept_handler.setter
    def intercept_handler(self, handler: InterceptHandler):
        self.__intercept_handler = handler

    def handle(self, record):
        # Call the original handle method
        super().handle(record)

        # Call handle_message with the formatted message and level name
        formatted_message = self.__formatter.format(record)
        level_id = record.levelno
        self.handle_message(formatted_message, level_id)

    def handle_message(
        self,
        formatted_message: str,
        level_name: int,
        details: dict = None
    ) -> None:
        """
        Placeholder for handling formatted messages.

        Override this to handle the formatted message in whichever way you want.
        """
        pass

    def __set_level(self, level) -> None:
        """
        Set the logging level
        :param level:
        :return: None
        """
        if level is None:
            level = logging.DEBUG
        self.setLevel(level)
        self.__stream_handler.setLevel(level)
        self.intercept_handler.setLevel(level)  # Set level for InterceptHandler

    # def get_latest_log(self):
    #     return self.intercept_handler.get_latest_log()  # Method to get the latest log from InterceptHandler
