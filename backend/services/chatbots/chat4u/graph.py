from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from .nodes.generate_node import generate
from .nodes.grade_node import grade
from .nodes.retrieve_node import retrieve
from .state import State

workflow = StateGraph(State)
memory = MemorySaver()

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade)
workflow.add_node("generate", generate)

# define the edge
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile(checkpointer=memory)
