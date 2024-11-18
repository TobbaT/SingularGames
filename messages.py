
def message(channels, value):
    """
    Helper function to create a message for dispatching.

    Messages will be either sent to the Referee or to the dispatcher.
    Messages for the referee should indicate their provenance. e.g. [["ChatGPT"], "Hello, referee!"]
    Messages for the dispatcher should indicate the target channels (recipient). e.g. [["ChatGPT", "Gemini-flash"], "Referee : Hello, players!"]
    """
    return [channels, value]

def message_from(channel, value):
    """
    Helper function to create a message for dispatching from a single channel.
    """
    return message([channel], value)

def message_to(channels, value):
    """
    Helper function to create a message for dispatching to multiple channels.
    """
    return message(channels, value)

def err_message(value):
    """
    Helper function to create an error message for dispatching.
    """
    return message_from("Error", value)