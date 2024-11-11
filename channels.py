# channels.py

import logging
import sys
from abc import ABC, abstractmethod

class Channel(ABC):
    """
    Abstract base class for a communication channel.

    Methods:
        push(message): Abstract method to push a message to the channel.
    """
    def __init__(self):
        self.queue = []

    def push(self, message):
        """
        Push a message to the channel.
        """
        self.queue.append(message)
        return self
    
    def flush(self):
        """
        Flush the channel.
        """
        self.queue = []

    def _process(self):
        """
        Process the channel, returning a value based on channel contents.
        """
        return None

    def get_response(self):
        """
        Get the response from the channel.
        """
        response = self._process()
        self.flush()
        return response

class ErrorChannel(Channel):
    """
    Channel to handle errors and exit the program if necessary.
    It's content is expected to be given to the referee, giving it a chance to correct.

    Attributes:
        game_over (bool): Flag to indicate if the game is over.
        max_errors (int): Maximum number of errors before exiting.
    """

    def __init__(self, max_errors=5):
        super().__init__()
        self.max_errors = max_errors

    def push(self, message):
        logging.error(f"Error: {message}")
        return super().push(message)

    def _process(self):
        self.max_errors -= 1
        if self.max_errors <= 0:
            logging.error("Max errors reached. Exiting.")
            sys.exit(1)
        if self.queue:
            return ["Error", self.queue]
        return None


class SystemChannel(Channel):
    """
    Channel to handle system-level messages and control game flow.
    """
    def __init__(self):
        super().__init__()

    def _process(self):
        logging.info("Game over. Thanks for playing!")
        sys.exit(0)
