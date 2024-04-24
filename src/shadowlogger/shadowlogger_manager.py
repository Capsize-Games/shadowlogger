import threading
import logging

from shadowlogger.shadowlogger import ShadowLogger
from shadowlogger.singleton import Singleton


class ShadowLoggerManager(metaclass=Singleton):
    def __init__(self):
        self.original_handlers = None
        self.lock = threading.Lock()

    @property
    def shadowlogger(self):
        if self.__shadowlogger is None:
            self.__shadowlogger = ShadowLogger()
        return self.__shadowlogger

    @shadowlogger.setter
    def shadowlogger(self, value):
        self.__shadowlogger = value

    def activate(self):
        with self.lock:
            # Get the root logger
            root_logger = logging.getLogger()

            # Keep track of the original handlers
            self.original_handlers = root_logger.handlers[:]

            # Remove all existing handlers from the root logger
            for h in root_logger.handlers[:]:
                root_logger.removeHandler(h)

            # Add the InterceptHandler to the root logger
            root_logger.addHandler(self.shadowlogger.intercept_handler)

            # Set the level for the root logger
            root_logger.setLevel(logging.INFO)

            # Prevent propagation of log records to other handlers
            root_logger.propagate = False

    def deactivate(self):
        with self.lock:
            # Get the root logger
            root_logger = logging.getLogger()

            # Remove the InterceptHandler from the root logger
            root_logger.removeHandler(self.shadowlogger.intercept_handler)

            # Restore the original handlers
            for h in self.original_handlers:
                root_logger.addHandler(h)

            # Allow propagation of log records to other handlers
            root_logger.propagate = True

            # Restore the original os.write and socket.send functions
            self.shadowlogger.intercept_handler.restore_original_functions()
