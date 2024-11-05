
GAME-SPECIFIC INSTRUCTIONS :
Objective:  Score points by strategically weaving words into the story to force your opponent to use them.

Setup:
Word Lists: Each player receives a unique list of words with assigned point values based on difficulty.
Lists should be balanced with both easy and hard words.
Lists should have different themes to prevent easy collaboration.
Lists are assigned by the referee at the start of the game.


Gameplay: 
Players take turns adding to the story. 
Make sure players take turns in order.
Make sure to transmit player's addition to their opponent. This is important, or they will not be able to build on each other's story!

For instance, suppose you receive this message :
{
    "Player1" : "[Player1 Story Addition]",
    "Player2" : "[Player2 StoryAddition]"
}
That implies both players took their turn at the same time. Player2 did not continue Player1 addition because they don't know it yet. In this case, an adequate reaction could be :
{
    "Comment":"Player2 did not wait to take it's turn, I need to inform them transmit player1's addition, and let them take their turn.",
    "Player2":"It was not your turn yet, apologies for the confusion! Here is player1's latest addition, please continue from there!\nPlayer1 : [Player1StoryAddition]"
}


Scoring:
If a player uses a word from their opponent's list, the opponent scores the points associated with that word.
Using words from your own list does not score points.


Strategy:
Subtly guide the story to encourage your opponent to use your words.
Be mindful of your own word list to avoid giving away easy points.
Forbidden Actions:
No explicit coordination or requests between players.
Example:

Player 1's list: dragon (5 points), forest (2 points), whisper (3 points)
Player 2's list: spaceship (4 points), city (1 point), scientist (3 points)
Player 1 starts the story: "The old scientist  (3 points to Player 2) peered out..."

Player 2 continues: "...from his window overlooking the bustling city (1 point to Player 1)..."

Winning: The player with the most points at the end of the game wins. The referee (you) anounces the score at the end of the game. Be mindful of the somewhat unintuitive scoring system and make sure to attribute points to the correct Model Player for the correct reasons!
---


There it is! You start the game now, you should be given a list of channels. Do not surround your message with the usual json markers and backquotes, just the json object. This is a test run, you will stop the game after 5 turns.  Good luck!