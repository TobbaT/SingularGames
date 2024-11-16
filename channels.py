# channels.py

import logging
import sys
from abc import ABC, abstractmethod

def message(channels, value):
    """
    Helper function to create a message for dispatching.

    Messages will be either sent to the Referee or to the dispatcher.
    Messages for the referee should indicate their provenance. e.g. [["ChatGPT"], "Hello, referee!"]
    Messages for the dispatcher should indicate the target channels (recipient). e.g. [["ChatGPT", "Gemini-flash"], "Referee : Hello, players!"]
    """
    return [channels, value]

def message_from(channel, value):
    """
    Helper function to create a message for dispatching from a single channel.
    """
    return message([channel], value)

def message_to(channels, value):
    """
    Helper function to create a message for dispatching to multiple channels.
    """
    return message(channels, value)

def err_message(value):
    """
    Helper function to create an error message for dispatching.
    """
    return message_from("Error", value)

class Channel(ABC):
    """
    Abstract base class for a communication channel.

    Methods:
        __init__(process_condition:list=>bool): Constructor for the channel. Always process by default.
        push(message): Abstract method to push a message to the channel.
    """
    def __init__(self, process_condition=lambda x: True):
        self.queue = []
        self.process_condition = process_condition

    def push(self, message):
        """
        Push a message to the channel, potentially trigerring _process().
        """
        self.queue.append(message)
        if self.process_condition(self.queue):
            response = self._process()
            self.queue = []
            return response
        return None

    def _process(self):
        """
        Process the channel, returning a value based on channel contents.
        Should be implemented by subclasses.
        """
        return None

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
            return err_message(self.queue)
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
