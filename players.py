# players.py

import logging
from channels import Channel
import os
import json

from langchain_core.messages import HumanMessage
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class Player(Channel):
    """
    Player class for interacting with language models using LangGraph for history management.
    """
    def __init__(self, name, model):
        super().__init__()
        self.name = name
        self.model = model

        # Define the LangGraph workflow
        self.workflow = StateGraph(state_schema=MessagesState)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        # Add memory
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)
        self.config = {"configurable": {"thread_id": "abc123"}}

    def call_model(self, state: MessagesState):
        """
        Calls the language model with the current message history.
        """
        response = self.model.invoke(state["messages"])
        return {"messages": response}


    def push(self, message):
        """
        Sends a message to the language model and retrieves the response.
        """
        try:
            # Run the LangGraph workflow with the new message
            inputs = [HumanMessage(content=message)]
            result = self.app.invoke({"messages": inputs}, self.config)
            response = result['messages'][-1].content
            return {self.name: response}
        except Exception as e:
            print(f"Error interacting with language model: {e}")
            return {self.name: "Error"}



class Referee:
    """
    Referee class that wraps a player and logs input and output.

    Attributes:
        player (player): The player instance to wrap.
    """
    def __init__(self, player):
        self.player = player

    def push(self, message):
        """
        Pushes a message to the wrapped player and logs the input and output.

        Args:
            message (str): The message to be sent to the player.

        Returns:
            dict: The response from the player.
        """
        logging.info(f"To referee: {message}")
        name = self.player.name
        raw_response = self.player.push(message)
        logging.info(f"From referee (raw): {raw_response}")
        response = json.loads(raw_response[name])
        logging.info(f"From referee: {response}")
        return response
