from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage, BaseMessage
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END

# We will use this model for both the conversation and the summarization
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4.1-nano", temperature=0) 

# Debugging: InputState & OutputState are introduced to help with receiving user input to `messages`.
#   Without these, the user input is delivered to `summary` key. It seems to be a bug in LangGraph Studio.
# Input schema - only what LangGraph Studio should show as input
class InputState(TypedDict):
    messages: list[BaseMessage]

# Full state schema - includes summary for internal use
class State(MessagesState):
    summary: str = ""

# Output schema - what gets returned
class OutputState(TypedDict):
    messages: list[BaseMessage]

# Define the logic to call the model
def call_model(state: State):
    
    # Get summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it to messages
    if summary:
        
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]
    
    response = model.invoke(messages)
    return {"messages": response}

# Determine whether to end or summarize the conversation
def should_continue(state: State) -> Literal["summarize_conversation", "__end__"]:
    
    """Return the next node to execute."""
    
    messages = state["messages"]
    
    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 4:
        print("========================summarizing======================")
        return "summarize_conversation"
    
    # Otherwise we can just end
    return "__end__"

def summarize_conversation(state: State):
    
    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt 
    if summary:
        
        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
        
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}

# Define a new graph with input schema
workflow = StateGraph(State, input_schema=InputState, output_schema=OutputState)
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