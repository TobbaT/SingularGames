from airena import AIrena, ChatGPT

m_gpt_4 = "gpt-4o"
m_gpt_3 = "gpt-3.5-turbo-1106"

REFEREE_GPT=m_gpt_4
CONTENDERS_GPT=m_gpt_4
INSTRUCTIONS_FILE="20Questions.txt"

def main():
    """
    WARNING: Running this AIrena game involves making calls to OpenAI's GPT models, which may incur costs.
    Please be aware that each game session can consume a significant amount of API tokens, leading to charges
    on your OpenAI account. Ensure you are familiar with OpenAI's pricing structure before running this game.
    """

    # Prompt the user for consent
    consent = input("Do you acknowledge the cost warning and wish to proceed? (yes/no): ").strip().lower()

    if consent != "yes":
        print("Game not started. Please review OpenAI's pricing structure before proceeding.")
        exit()


    # Read global rules from file
    with open(INSTRUCTIONS_FILE,'r') as file:
        global_rules=file.read()

    # Create participants
    referee = ChatGPT("Referee",REFEREE_GPT)
    contender1 = ChatGPT("NeuroSynth GPT-Prime",CONTENDERS_GPT)
    contender2 = ChatGPT("QuantumBite Gemini Oracle",CONTENDERS_GPT)

    # Create a dictionary of contenders
    contenders = {
        contender1.name: contender1,
        contender2.name: contender2
    }

    # Initialize and run the game
    arena = AIrena()
    arena.run_game(contenders, referee, global_rules)

if __name__ == "__main__":
    main()
