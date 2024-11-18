# players.py
import logging
import os
import json
import re

from messages import err_message, message_from
from langchain_core.messages import HumanMessage, AIMessage

def process_on_None(queue: list) -> bool:
    return queue and queue[-1] is None

class Player():
    """
    Player class for interacting with language models using LangGraph for history management.
            
    Usage:
        player = Player("player_name", model)
        player.push("Hello")  # Queues the message and returns None
        player.push("How are you?")  # Queues the message and returns None
        response = player.push(None)  # Processes the queue and returns the result
        print(response)  # [["player_name"], "I'm fine, thank you!"]
    """
    def __init__(self, name:str, model):
        """
        args:
            name (str): The name of the player.
            model (langchain_core.language_models.chat_models.BaseChatModel): 
                The chat language model to be used by the player. 
                See langchain docs for details :
                https://python.langchain.com/docs/concepts/chat_models/#interface
        """
        self.name = name
        self.model = model
        self.queue = []
        self.message_history = []


    def push(self, message):
        """
        Push a message to the player, potentially triggering the processing of the queue.
        args:
            message (str): The message to be pushed to the player.
        returns:
            response (str): The response from the player. 
        """
        if message is None:
            response = self._process()
            self.queue = []
            return response
        else:
            self.queue.append(message)
            return None


    def _process(self):
        """
        The model is invoked on the messages in the queue, which are added to the state as a result.
        This method is called by the Channel parent class, which then flushes the queue.

        Do not call this method directly. See Class docstring for usage.
        """
        if not self.queue:
            err_str = f"{self.name} has no new information, cannot respond."
            return err_message(err_str)
        try:
            messages = self.message_history + [HumanMessage(content=x) for x in self.queue]
            result = self.model.invoke(messages)
            self.message_history = messages + [AIMessage(content=result.content)] # Update history
            return message_from(self.name, result.content)
        except Exception as e:
            err_str = f"Error interacting with language model: {e}"
            return err_message(err_str)

