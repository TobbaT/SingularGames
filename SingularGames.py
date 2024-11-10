
import json
import sys
from channels import ErrorChannel, Channel, SystemChannel, ProcessorChannel
from players import Player
import logging

class Game:
    """
    A class to run an AI-based game simulation.

    This class manages the game flow, including initializing channels, creating prompts for the referee,
    processing responses, and handling errors. It ensures the game runs within a specified iteration limit
    to prevent excessive API usage.


    Public Methods:
        run_game(players, referee, global_rules): Starts the game by initializing channels, creating the referee prompt, and entering the game loop.
   """

    def __init__(self, players:dict[str,Player], referee:Player, global_rules:str):
        self.players = players
        self.referee = referee
        self.channels = players
        self.channels["System"] = SystemChannel()
        self.channels["Comment"] = Channel()
        self.channels["Error"] = ErrorChannel()
        self.updated_channels = ProcessorChannel()
        self.referee_prompt = self.create_referee_prompt(global_rules)


    def create_referee_prompt(self, global_rules):
        return f"{global_rules}\n\nChannels : {json.dumps(list(self.channels.keys()))}"

    def run(self, max_iterations:int=10):
        referee_input = self.referee_prompt
        for i in range(max_iterations):
            logging.info(f"Iterations  {i} out of {max_iterations}.")
            try:
                messages = self.referee_act(referee_input)
                aggregated_responses = self.dispatch_messages(messages)
                referee_input = json.dumps(aggregated_responses)
    
            except Exception as e:
                err_message = f"Error during game loop. Usually this means the program failed to process input from the Referee. Exception raised : {e}"
                self.channels["Error"].push(err_message)
                self.updated_channels.push("Error")
                raise e
                continue
        logging.info(f"Game Over.")
    
    def dispatch_messages(self, messages:list[list[str]]):
        for message in messages:
            target_channel_name, value = message
            target_channel = self.channels.get(target_channel_name)
            if target_channel:
                self.updated_channels.push(target_channel.push(value))
        return self.updated_channels.get_response()

    def referee_act(self, message: str) -> list[str]:
        """
        Pushes a message to a player and logs the input and output.

        Args:
            player: The player instance.
            message (str): The message to be sent to the player.

        Returns:
            list[str]: The response from the player, or an error message if decoding fails.
        """
        logging.info(f"To referee: {message}")

        raw_response = self.referee.push(message).get_response()
        sender, response_str = raw_response

        decoder = json.JSONDecoder()
        try:
            # Find the start of a JSON array in the response
            pos = response_str.index('[')  
            response, pos = decoder.raw_decode(response_str[pos:])
        except (ValueError, json.JSONDecodeError) as e:
            err_message = f"Error decoding JSON response from Referee: {e}\n\tRaw response: {response_str}"
            response = [["Error", err_message]]

        logging.info(f"From referee: {response}")
        return response