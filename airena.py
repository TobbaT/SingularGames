import os
import json
import logging
from abc import ABC, abstractmethod
from openai import OpenAI
import google.generativeai as genai

class Channel(ABC):
    """
    Abstract base class for a communication channel.

    Methods:
        push(message): Abstract method to push a message to the channel.
    """
    @abstractmethod
    def push(self, message):
        pass

class Participant(Channel):
    """
    Base class for game participants.

    Attributes:
        name (str): Name of the participant.
    """
    def __init__(self, name):
        self.name = name

    def print_chat_message(self, message):
        logging.debug(f"{self.name}: {message}")

class ChatGPT(Participant):
    """
    Participant using ChatGPT model.

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
            self.print_chat_message(response.content)
            self.messages.append(response)
            return {self.name: response.content}
        except Exception as e:
            print(f"Error interacting with ChatGPT: {e}")
            return {self.name: "Error"}

class GeminiParticipant(Participant):
    """
    Participant using the Gemini model.

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
            self.print_chat_message(response.text)
            return {self.name: response.text}
        except Exception as e:
            print(f"Error interacting with Gemini: {e}")
            return {self.name: "Error"}

class SystemChannel(Channel):
    """
    Special system channel to control game flow.

    Attributes:
        game_over (bool): Flag to indicate if the game is over.
    """

    def __init__(self):
        self.game_over = False

    def push(self, message):
        # Receives a system message to control the game flow.
        pass

class CommentChannel(Channel):
    """
    Channel for the referee to plan and think without impacting the game.

    Methods:
        push(message): Does nothing.
    """
    def push(self, message):
        # Do nothing
        pass

class AIrena:
    """
    AIrena class to run the AI-based game.

    Attributes:
        count (int): Counter to keep track of the number of iterations to prevent excessive API usage.
    """

    def __init__(self):
        self.count = 0

    def run_game(self, contenders, referee, global_rules):
        self.count = 0
        channels = self.initialize_channels(contenders)
        referee_prompt = self.create_referee_prompt(global_rules, channels)
        logging.info(referee_prompt)

        try:
            data = self.initialize_game(referee, referee_prompt)
        except Exception as e:
            logging.error(f"Error initializing game: {e}")
            return

        self.game_loop(channels, referee, data)

    def initialize_channels(self, contenders):
        channels = contenders
        channels["System"] = SystemChannel()
        channels["Comment"] = CommentChannel()
        return channels

    def create_referee_prompt(self, global_rules, channels):
        return f"{global_rules}\n\nChannels : {json.dumps(list(channels.keys()))}"

    def initialize_game(self, referee, referee_prompt):
        data = referee.push(referee_prompt)
        logging.info(f"Received from referee: {data}")
        return data

    def game_loop(self, channels, referee, data):
        while not channels["System"].game_over and self.count <= 20:
            self.count += 1
            data = json.loads(data["Referee"])
            aggregated_responses = self.process_responses(channels, data)

            if "System" in aggregated_responses:
                logging.info(aggregated_responses["System"])
                break

            try:
                logging.info(f"Sending to referee: {json.dumps(aggregated_responses)}")
                data = referee.push(json.dumps(aggregated_responses))
                logging.info(f"Received from referee: {data}")
                if channels["System"].game_over:
                    break
            except Exception as e:
                logging.error(f"Error during game loop: {e}")
                return

        self.end_game()

    def process_responses(self, channels, data):
        aggregated_responses = {}
        for target_channel, value in data.items():
            if target_channel in channels:
                response = channels[target_channel].push(value)
                aggregated_responses.update(response)
            else:
                logging.error(f"Channel '{target_channel}' does not exist. Is the referee hallucinating?")
                logging.error(f"Could not send message : {value}")
                return aggregated_responses
        return aggregated_responses

    def end_game(self):
        if self.count > 20:
            logging.info("Game exited due to length. This is a protective measure against accidentally spending too much credit. See README for details.")
        else:
            logging.info("Game over.")
