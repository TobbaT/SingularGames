import argparse
import os
from airena import AIrena, ChatGPT, SystemChannel

m_gpt_4 = "gpt-4o"
m_gpt_3 = "gpt-3.5-turbo-1106"

REFEREE_GPT=m_gpt_4
CONTENDERS_GPT=m_gpt_4

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
    parser.add_argument('--game', type=str, required=True, help='The game prompt file to use (e.g., 20Questions.txt)')
    args = parser.parse_args()

    prompt_file = os.path.join('prompts', args.game)
    if not os.path.exists(prompt_file):
        print(f"Error: The game prompt file '{args.game}' does not exist in the 'prompts' folder.")
        return

    global_rules = load_prompt(prompt_file)

    # Initialize contenders and referee
    contenders = {
        "ChatGPT1": ChatGPT("ChatGPT1", "gpt-4o"),
        "ChatGPT2": ChatGPT("ChatGPT2", "gpt-4o")
    }
    referee = ChatGPT("Referee", "gpt-4o")

    # Run the game
    arena = AIrena()
    arena.run_game(contenders, referee, global_rules)

if __name__ == '__main__':
    main()
