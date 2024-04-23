import unittest

from shadowlogger.shadowlogger import ShadowLogger


class TestShadowLogger(ShadowLogger):
    def handle_message(self, formatted_message: str, level_name: str):
        self.last_formatted_message = formatted_message
        self.last_level_name = level_name


class TestHandleMessage(unittest.TestCase):
    def setUp(self):
        self.logger = TestShadowLogger()

    def test_handle_message(self):
        message = "test message"
        level = "DEBUG"

        # Log a message
        self.logger.debug(message)

        # Check if handle_message was called correctly
        self.assertTrue(self.logger.last_formatted_message.endswith(f"- AI RUNNER - {level} -  - {message} - 21"))
        self.assertEqual(self.logger.last_level_name, level)
