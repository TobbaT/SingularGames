import argparse
import os
import logging
from datetime import datetime
from airena import AIrena
from players import Player, Referee
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI



def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    """
    WARNING: Running this AIrena game involves making calls to OpenAI's GPT models, which may incur costs.
    Please be aware that each game session can consume a significant amount of API tokens, leading to charges
    on your OpenAI account. Ensure you are familiar with OpenAI's pricing structure before running this game.
    """

    parser = argparse.ArgumentParser(description="Run the AIrena game.")
    parser.add_argument('--generic', type=str, default='GeneralInstructions.md', help='The generic prompt file to use (default: GeneralInstructions.md)')
    parser.add_argument('--game', type=str, required=True, help='The game prompt file to use (e.g., 20Questions.txt)')
    args = parser.parse_args()

    generic_prompt_file = os.path.join('prompts', args.generic)
    game_prompt_file = os.path.join('prompts', args.game)

    if not os.path.exists(generic_prompt_file):
        print(f"Error: The generic prompt file '{args.generic}' does not exist in the 'prompts' folder.")
        exit(1)

    if not os.path.exists(game_prompt_file):
        print(f"Error: The game prompt file '{args.game}' does not exist in the 'prompts' folder.")
        exit(1)

    # Set up logging
    log_filename = f"outputs/{args.game}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])

    logging.info(f"Starting game with generic prompt file: {args.generic} and game prompt file: {args.game}")

    generic_rules = load_prompt(generic_prompt_file)
    game_rules = load_prompt(game_prompt_file)
    global_rules = generic_rules + "\n" + game_rules

    # Initialize players and referee
    players = {
        #"ChatGPT": Player("ChatGPT", ChatOpenAI(model="gpt-4o")),
        "Gemini-flash-8b": Player("Gemini-flash-8b", ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")),
        "Gemini-flash": Player("Gemini-flash", ChatGoogleGenerativeAI(model="gemini-1.5-flash"))
    }
    #referee = Referee(Player("Referee", ChatOpenAI(model="gpt-4o")))
    #referee = Referee(Player("Referee", ChatGoogleGenerativeAI(model="gemini-1.5-pro")))
    referee = Referee(Player("Referee", ChatGoogleGenerativeAI(model="gemini-1.5-flash")))

    logging.info("Game initialized with players and referee.")

    # Create an instance of AIrena and run the game
    arena = AIrena()
    arena.run_game(players, referee, global_rules)

if __name__ == "__main__":
    main()
