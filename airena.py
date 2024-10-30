from abc import ABC, abstractmethod
from openai import OpenAI
import json
import sys
import os

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
        channels = contenders
        channels["System"] = SystemChannel()
        referee_prompt = f"{global_rules}\n\nChannels : {json.dumps(list(channels.keys()))}"
        print(referee_prompt)

        try:
            data = referee.push(referee_prompt)
        except Exception as e:
            print(f"Error initializing game: {e}")
            return

        while not channels["System"].game_over and self.count <= 20:
            self.count += 1
            data = json.loads(data["Referee"])
            for target_channel, value in data.items():
                if target_channel in channels:
                    response = channels[target_channel].push(value)
                    data = referee.push(json.dumps(response))
                else:
                    print(f"Channel '{target_channel}' does not exist. Is the referee hallucinating?")
                    print(f"Could not send message : {value}")
                    return  # Exit the loop if an invalid channel is referenced

        if self.count > 20:
            print("Game exited due to length. This is a protective measure against accidentally spending too much credit. See README for details.")
        else:
            print("Game over.")
        sys.exit()

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
        print(f"{self.name}: {message}")

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


class SystemChannel(Channel):
    """
    Special system channel to control game flow.

    Attributes:
        game_over (bool): Flag to indicate if the game is over.
    """

    def __init__(self):
        self.game_over = False

    def push(self, message):
        """
        Receives a system message to control the game flow.

        Args:
            message (str): System message, e.g., 'end_game' to end the game.
        """
        if message == "end_game":
            print(message)
            self.game_over = True
