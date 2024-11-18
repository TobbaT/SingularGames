GAME-SPECIFIC INSTRUCTIONS

Close Enough is a game where both player try to gess a secret snetence picked by the referee. 

Here is how it goes (suggested order to make the game simple) : 
- Introduction like always.
- The referee picks a sentence and asks a player to take a guess.
- The player takes a guess
- The referee uses the tool to compare.
- The tool replies to the referee
- The referee assign points, and asks the next player for a guess.
This continue until the end, or a player gets close enough (above 0.95)

Notes : 
- Under the hood, the tool uses embeddings and cosine similarity, so the diff is between 0 and 1.
- The best global score is remembered for comparison.
- Players score based on how much they improve on the previous best, between 0 (same or less) and 3 (more than 0.2 above previous best).
- The first player close enough gets an extra 5 points.
- Maximum of 5 turns per player.

Tip : make the game memorable by choosing a sentence that is original, funny or interesting!

Information management :
- The referee is in charge of communicating the guesses, guess scores and points through the game. Only the secret sentence is secret.
- The secret sentence is revealed when the game ends.

Tool use :
- In order to use a tool, the referee uses a non already existant channel of choice prefixed by "tool_call-". (the channel will be dynamically created)
- The name of the tool for comparison is "sentence_diff".
- Example usage :
```json
[
    [["Comment"], "Example tool usage in a batch of messages"],
    [["tool_call-123"], "sentence_diff", 
        "This would be the first sentence to compare", 
        "This would be the second sentence to compare"],
    [["Comment"], "Tool calls are basic channels"]
]
```
