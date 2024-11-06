# airena.py

import json
import sys
from channels import ErrorChannel, CommentChannel, SystemChannel
from players import Referee

class AIrena:
    """
    AIrena class to run the AI-based game.

    Attributes:
        count (int): Counter to keep track of the number of iterations to prevent excessive API usage.
    """

    def __init__(self):
        self.count = 0

    def run_game(self, players, referee, global_rules):
        self.count = 0
        channels = self.initialize_channels(players)
        referee_prompt = self.create_referee_prompt(global_rules, channels)

        self.game_loop(channels, referee, referee_prompt)

    def initialize_channels(self, players):
        channels = players
        channels["System"] = SystemChannel()
        channels["Comment"] = CommentChannel()
        channels["Error"] = ErrorChannel()
        return channels

    def create_referee_prompt(self, global_rules, channels):
        return f"{global_rules}\n\nChannels : {json.dumps(list(channels.keys()))}"

    def game_loop(self, channels, referee, data):
        while not channels["System"].game_over and self.count <= 20:
            self.count += 1
            try:
                data = referee.push(data)
                aggregated_responses = self.process_responses(channels, data)
                data = json.dumps(aggregated_responses)
                if "System" in data:
                    break
            except Exception as e:
                err_message = f"Error during game loop. Usually this means the program failed to process input from the Referee. Exception raised : {e}"
                channels["Error"].push(err_message)
                continue
        self.end_game()

    def process_responses(self, channels, data):
        aggregated_responses = {}
        for target_channel, value in data.items():
            if target_channel in channels:
                response = channels[target_channel].push(value)
                if response:
                    aggregated_responses.update(response)
        return aggregated_responses

    def end_game(self):
        pass