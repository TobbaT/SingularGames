# players.py

import logging
from channels import Channel
import os
import json
import re

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


    def process(self):
        """
        Process the channel, returning a value based on channel contents.
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


