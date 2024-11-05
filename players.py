# players.py

import logging
from channels import Channel
from openai import OpenAI
import os
import google.generativeai as genai
import json

class Player(Channel):
    """
    Abstract base class for a player in the game.

    Attributes:
        name (str): The name of the player.
    """
    def __init__(self, name):
        self.name = name

    def push(self, message):
        raise NotImplementedError("The push method must be implemented by the subclass.")


class ChatGPT(Player):
    """
    player using ChatGPT model.

    Attributes:
        messages (list): List of message history.
        client (OpenAI): OpenAI client instance.
        model (str): Model identifier for OpenAI GPT.
    """
    def __init__(self, name, model) -> None:
        super().__init__(name)
        self.messages = []
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def push(self, message):
        """
        Pushes a message to the ChatGPT model and retrieves the response.

        Args:
            message (str): The message to be sent to ChatGPT.

        Returns:
            dict: The response from ChatGPT.
        """
        role = "user"  # Default role for the message.
        self.messages.append({"role": role, "content": message})
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages)
            response = completion.choices[0].message
            self.messages.append(response)
            return {self.name: response.content}
        except Exception as e:
            print(f"Error interacting with ChatGPT: {e}")
            return {self.name: "Error"}

class Gemini(Player):
    """
    player using the Gemini model.

    Attributes:
        messages (list): List of message history.
        model (str): Model identifier for Gemini.
    """
    def __init__(self, name, model="models/gemini-pro") -> None:
        super().__init__(name)
        self.messages = []  # Initialize an empty list to store the conversation history
        genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
        self.model = genai.GenerativeModel(model)
        self.chat = self.model.start_chat()  # Initialize the chat object


    def push(self, message):
        """
        Sends a message to the Gemini model and retrieves the response.

        Args:
            message (str): The message to be sent to Gemini.

        Returns:
            dict: The response from Gemini.
        """
        try:
            response = self.chat.send_message(message)  # Send the message using the chat object
            return {self.name: response.text}
        except Exception as e:
            print(f"Error interacting with Gemini: {e}")
            return {self.name: "Error"}

class Referee:
    """
    Referee class that wraps a player and logs input and output.

    Attributes:
        player (player): The player instance to wrap.
    """
    def __init__(self, player):
        self.player = player

    def push(self, message):
        """
        Pushes a message to the wrapped player and logs the input and output.

        Args:
            message (str): The message to be sent to the player.

        Returns:
            dict: The response from the player.
        """
        logging.info(f"To referee: {message}")
        name = self.player.name
        raw_response = self.player.push(message)
        response = json.loads(raw_response[name])
        logging.info(f"From referee: {response}")
        return response
