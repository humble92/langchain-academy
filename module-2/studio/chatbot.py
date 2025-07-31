from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END

# We will use this model for both the conversation and the summarization
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4.1-nano", temperature=0) 

# State class - only uses MessagesState, summary stored in system messages
# Debug: summary key in State is not working as expected. User input is delivered to summary key.
class State(MessagesState):
    pass
    
# Helper function to get summary from messages
def get_summary_from_messages(messages):
    """Extract summary from first SystemMessage if it exists"""
    if messages and isinstance(messages[0], SystemMessage):
        content = messages[0].content
        if content.startswith("Summary of conversation earlier:"):
            return content.replace("Summary of conversation earlier: ", "")
    return ""

# Helper function to remove summary message
def remove_summary_message(messages):
    """Remove summary SystemMessage if it exists"""
    if messages and isinstance(messages[0], SystemMessage):
        content = messages[0].content
        if content.startswith("Summary of conversation earlier:"):
            return messages[1:]  # Return messages without summary
    return messages

# Define the logic to call the model
def call_model(state: State):
    
    # Use messages as-is (summary already embedded if exists)
    messages = state["messages"]
    
    response = model.invoke(messages)
    return {"messages": response}

# Determine whether to end or summarize the conversation
def should_continue(state: State) -> Literal["summarize_conversation", "__end__"]:
    
    """Return the next node to execute."""
    
    messages = state["messages"]
    
    # Remove summary message from count
    actual_messages = remove_summary_message(messages)
    
    # If there are more than six actual conversation messages, then we summarize
    if len(actual_messages) > 6:
        print("========================summarizing======================")
        return "summarize_conversation"
    
    # Otherwise we can just end
    return "__end__"

def summarize_conversation(state: State):
    
    messages = state["messages"]
    
    # Get existing summary if it exists
    existing_summary = get_summary_from_messages(messages)
    
    # Remove summary message to get actual conversation
    actual_messages = remove_summary_message(messages)
    
    # Create our summarization prompt 
    if existing_summary:
        # If a summary already exists, extend it
        summary_message = (
            f"This is summary of the conversation to date: {existing_summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        # If no summary exists, just create a new one
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our conversation messages
    messages_for_summary = actual_messages + [HumanMessage(content=summary_message)]
    response = model.invoke(messages_for_summary)
    
    # Keep only the 2 most recent actual messages
    recent_messages = actual_messages[-2:]
    
    # Create new summary system message
    new_summary_message = SystemMessage(content=f"Summary of conversation earlier: {response.content}")
    
    # Return new message list: summary + recent messages
    new_messages = [new_summary_message] + recent_messages
    
    return {"messages": new_messages}

# Define a new graph
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges(
    "conversation", 
    should_continue,
    {
        "summarize_conversation": "summarize_conversation",
        "__end__": END
    }
)
workflow.add_edge("summarize_conversation", END)

# Compile
graph = workflow.compile()