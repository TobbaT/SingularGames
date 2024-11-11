# players.py
import logging
import os
import json
import re

from channels import Channel
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class Player(Channel):
    """
    Player class for interacting with language models using LangGraph for history management.
            
    Usage:
        player = Player("player_name", model)
        player.push("Hello")
        player.push("How are you?")
        response = player.get_response() # ["player_name", "I'm fine, thank you!"]
        # Further calls with no new messages will return None
        response = player.get_response() # None
    """
    def __init__(self, name:str, model):
        """
        args:
            name (str): The name of the player.
            model (langchain_core.language_models.chat_models.BaseChatModel): 
                The chat language model to be used by the player. 
                See langchain docs for details :
                https://langchain.readthedocs.io/en/latest/langchain_core/language_models/chat_models.html
        """
        super().__init__()
        self.name = name
        self.model = model

        # Define the LangGraph workflow
        self.workflow = StateGraph(state_schema=MessagesState)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self._call_model)

        # Add memory
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)
        self.config = {"configurable": {"thread_id": self.name}}

    def _call_model(self, state: MessagesState):
        """
        Calls the language model with the current message history.
        Do not call this method directly. See Class docstring for usage.
        """
        response = self.model.invoke(state["messages"])
        return {"messages": response}


    def _process(self):
        """
        The model is invoked on the messages in the queue, which are added to the state as a result.
        This method is called by get_response() from the Channel parent class, which then flushes the queue.

        Do not call this method directly. See Class docstring for usage.
        """
        if not self.queue:
            return None
        try:
            # Run the LangGraph workflow with the new message
            inputs = [HumanMessage(content=x) for x in self.queue]
            result = self.app.invoke({"messages": inputs}, self.config)
            response = result['messages'][-1].content
            return [self.name, response]
        except Exception as e:
            err_message = f"Error interacting with language model: {e}"
            #print(err_message)
            return ["Error", err_message]


