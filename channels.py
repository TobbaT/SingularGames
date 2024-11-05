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
    @abstractmethod
    def push(self, message):
        pass

class ErrorChannel(Channel):
    """
    Channel to handle errors and exit the program if necessary.
    It's content is expected to be given to the referee, giving it a chance to correct.

    Attributes:
        game_over (bool): Flag to indicate if the game is over.
        max_errors (int): Maximum number of errors before exiting.
    """

    def __init__(self, max_errors=5):
        self.game_over = False
        self.messages = []
        self.max_errors = max_errors

    def push(self, message):
        self.messages.append(message)
        logging.error(f"Error encountered: {message}")
        if len(self.messages) >= self.max_errors:
            logging.error("Maximum number of errors reached. Exiting the program.")
            sys.exit(1)
        return {"Error": f"Errors encountered during this session, from first to last : {self.messages}" }

class CommentChannel(Channel):
    """
    Channel for the referee to plan and think without impacting the game.

    Methods:
        push(message): Does nothing.
    """
    def push(self, message):
        # Do nothing
        pass

class SystemChannel(Channel):
    """
    Channel to handle system-level messages and control game flow.

    Attributes:
        game_over (bool): Flag to indicate if the game is over.
    """
    def __init__(self):
        self.game_over = False

    def push(self, message):
        if "game over" in message.lower():
            self.game_over = True
        return {"System": "Game over message received."}