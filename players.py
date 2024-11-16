# players.py
import logging
import os
import json
import re

from channels import Channel, err_message, message_from
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

def process_on_None(queue: list) -> bool:
    return queue and queue[-1] is None

class Player(Channel):
    """
    Player class for interacting with language models using LangGraph for history management.
            
    Usage:
        player = Player("player_name", model)
        player.push("Hello")  # Queues the message and returns None
        player.push("How are you?")  # Queues the message and returns None
        response = player.push(None)  # Processes the queue and returns the result
        print(response)  # [["player_name"], "I'm fine, thank you!"]
    """
     def __init__(self, 
                 name:str, model,
                 process_condition=process_on_None):
        """
        args:
            name (str): The name of the player.
            process_condition (list=>bool): The condition to process the queue. By default, processes when last element is None. Do not change unless you know what you're doing, the referee will expect this behavior.
            model (langchain_core.language_models.chat_models.BaseChatModel): 
                The chat language model to be used by the player. 
                See langchain docs for details :
                https://python.langchain.com/docs/concepts/chat_models/#interface
        """
        super().__init__()
        self.process_condition = process_condition
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
        # TODO : Check out invoke doc. Why is it a list? Is it consistent across models?
        response = self.model.invoke(state["messages"])
        return {"messages": response}


    def _process(self):
        """
        The model is invoked on the messages in the queue, which are added to the state as a result.
        This method is called by the Channel parent class, which then flushes the queue.

        Do not call this method directly. See Class docstring for usage.
        """
        if not self.queue:
            return None
        try:
            # Run the LangGraph workflow with the new message
            inputs = [HumanMessage(content=x) for x in self.queue]
            # TODO : Do messages get saved when there is an error contacting the model?
            # This impacts how to handle errors : if yes, then we want to flush before calling again.
            result = self.app.invoke({"messages": inputs}, self.config)
            response = result['messages'][-1].content
            return message_from(self.name, response)
        except Exception as e:
            err_str = f"Error interacting with language model: {e}"
            #print(err_str)
            return err_message(err_str)


