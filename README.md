
# AIrena - 20 Questions Game with AI

AIrena is an interactive 20 Questions game where two AI models play against each other, with a referee AI model to oversee the game. The game is built using OpenAI's GPT models.

## Important Notice
:warning: **WARNING:** Running this AIrena game involves interactions with OpenAI's GPT models which are not free. Please be aware that each game session consumes API tokens and may result in charges on your OpenAI account. It is important to understand OpenAI's pricing structure and monitor your usage to avoid unexpected costs. This project defaults to gpt-4 for all contenders and a typical run cost around $0.50 in credits as of early december 2023. 

Disclaimer : This project does not work very well. Check out the samples (quasar is ok). The prompt likely seems too complex or badly written for AIs to follow. You can swap out models by editing run_arena.py. GPT-4 is pretty much necessary for the referee as 3.5 struggles with role play. You can use your own instruction file easily also.

## Description

In AIrena, two AI contenders attempt to guess each other's secret concepts through a series of yes/no questions. The referee AI facilitates the game, ensuring that rules are followed and managing the flow of the game. The project demonstrates the capabilities of AI in understanding and participating in structured game formats.

AIrena is designed to be highly flexible, only having to edit the referee file and the referee will instructs the others about the rules. It sort of works but barely. Better results can be achieved with a simpler structure, and writing system prompts for the contenders instead on relying on referee explanations. It may also be possible to improve communications for the AIs to understand better who is talking to who.

All contenders only ever talk to the referee and get queries from it, and it transmits their input, or asks them to correct. They are sometimes confused about who said what and when the game should end.

## Installation

To run AIrena, you need to have Python installed on your system. You also need the OpenAI Python package. 

1. **Clone the Repository**:

   ```
   git clone https://github.com/TobbaT/airena.git
   cd airena
   ```

2. **Install Dependencies**:

   Make sure you have `pip` installed. Then run:

   ```
   pip install -r requirements.txt
   ```

3. **Setting Up Environment Variables**:

   Rename the `.env.example` file to `.env` and fill in your OpenAI API key:

   ```
   OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

To run the game:

```
source .env
python run_arena.py
```

This will initiate the game where AI models will start asking questions in turns to guess each other's secret concepts.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

