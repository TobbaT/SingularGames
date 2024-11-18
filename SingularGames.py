
import json
import logging
from messages import err_message, message_to, message_from
from players import Player
from SentenceDiff import compare_sentences_google


class Game:
    """
    A class to run an AI-based game simulation.

    This class manages the game flow, including initializing channels, creating prompts for the referee,
    processing responses, and handling errors. It ensures the game runs within a specified iteration limit
    to prevent excessive API usage.

    message : [[channel_name,...], response] # If message to referee, channel_name is sender
    message : [[channel_name,...], response] # If from referee, channel_name is receiver
    channels: {str: message->message}

    Public Methods:
        run_game(players, referee, global_rules): Starts the game by initializing channels, creating the referee prompt, and entering the game loop.
   """

    def __init__(self, players:list[Player], referee:Player, global_rules:str):
        self.players = players
        self.referee = referee
        self.channels = {}
        for player in players:
            self.channels[player.name] = player.push
        self.channels["System"] = self.system
        self.channels["Comment"] = lambda m: None
        self.channels["Error"] = err_message
        self.referee_prompt = self.create_referee_prompt(global_rules)
        self.tools = {
            "sentence_diff": compare_sentences_google 
        }

    def system(self, message):
        logging.info("Game over. Thanks for playing!")
        sys.exit(0)

    def create_referee_prompt(self, global_rules):
        return f"{global_rules}\n\nChannels : {json.dumps(list(self.channels.keys()))}"

    def run(self, max_iterations:int=10):
        referee_input = self.referee_prompt
        aggregated_responses = []
        for i in range(max_iterations):
            logging.info(f"Iterations  {i} out of {max_iterations}.")
            # Sending prompt/aggregated_answers to the referee
            ref_response = self.referee_act(referee_input)
            if isinstance(ref_response, str):
                aggregated_responses = [err_message(ref_response)]
            else:
                messages = ref_response
                aggregated_responses = self.dispatch_messages(messages)
            
            referee_input = json.dumps(aggregated_responses)
        logging.info(f"Game Over.")
    
    # TODO: split this into many methods
    def dispatch_messages(self, messages:list[list]):
        aggregated_responses = []
        for message in messages:
            target_channel_names, *value = message
            for target_channel_name in target_channel_names:
                target_channel = self.channels.get(target_channel_name)
                if target_channel:
                    response = target_channel(value[0])
                    if response:
                        aggregated_responses.append(response)
                elif target_channel_name.startswith("tool_call-"):
                    tool_name = value[0]
                    tool = self.tools[tool_name]
                    response = message_from(target_channel_name, tool(*value[1:]))
                    if response:
                        aggregated_responses.append(response)
                else:    
                    err_str = f"Error: Channel {target_channel_name} not found."
                    err_str += f"\n\tMessage: {value}"
                    err_str += f"\n\tAvailable Channels: {json.dumps(list(self.channels.keys()))}"
                    err_response = self.channels["Error"](err_str)
                    aggregated_responses.append(err_response)
        return aggregated_responses

        

    def referee_act(self, message: str) -> list[str]:
        """
        Pushes a message to a player and logs the input and output.

        Args:
            player: The player instance.
            message (str): The message to be sent to the player.

        Returns:
            The response from the referee, a batch of messages to be dispatched.
            [[[channel_name], "response"], ...]
        """
        logging.info(f"To referee: {message}")

        self.referee.push(message)
        raw_response = self.referee.push(None)
        sender, response_str = raw_response

        decoder = json.JSONDecoder()
        try:
            # Find the start of a JSON array in the response
            pos = response_str.index('[')  
            response, pos = decoder.raw_decode(response_str[pos:])
        except (ValueError, json.JSONDecodeError) as e:
            err_str = f"Error decoding JSON response from Referee: {e}\n\tRaw response: {response_str}"
            response = err_str

        logging.info(f"From referee: {response}")
        return response