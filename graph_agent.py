from rag import get_answer
from langgraph.graph import StateGraph
from tools import mock_lead_capture
from typing import TypedDict, Optional

# ---------------- STATE ----------------
class AgentState(TypedDict):
    input: str
    intent: Optional[str]
    response: Optional[str]
    step: Optional[str]
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]

# ---------------- INTENT NODE ----------------
def intent_node(state):
    # 🔥 Prevent overriding during lead flow
    if state.get("step") not in [None, "done"]:
        return state

    user_input = state.get("input", "").lower()

    if any(word in user_input for word in ["hi", "hello", "hey"]):
        state["intent"] = "greeting"

    elif any(word in user_input for word in ["buy", "subscribe", "sign up", "start"]):
        state["intent"] = "high_intent"

    elif any(word in user_input for word in ["price", "pricing", "plan", "cost"]):
        state["intent"] = "pricing"

    else:
        state["intent"] = "other"

    return state

# ---------------- GREETING NODE ----------------
def greeting_node(state):
    state["response"] = "Hello! I can help you with pricing or getting started. What would you like to know?"
    return state

# ---------------- RAG NODE ----------------
def rag_node(state):
    user_input = state.get("input", "")
    answer = get_answer(user_input)
    state["response"] = answer
    return state

# ---------------- LEAD FLOW NODE ----------------
def lead_flow_node(state):
    user_input = state.get("input", "")

    # Step 1: Ask Name
    if state.get("step") is None:
        state["response"] = "Great! What's your name?"
        state["step"] = "name"
        return state

    # Step 2: Capture Name
    elif state["step"] == "name":
        state["name"] = user_input
        state["response"] = "Please provide your email."
        state["step"] = "email"
        return state

    # Step 3: Capture Email
    elif state["step"] == "email":
        state["email"] = user_input
        state["response"] = "Which platform do you create content on?"
        state["step"] = "platform"
        return state

    # Step 4: Capture Platform + Call Tool
    elif state["step"] == "platform":
        state["platform"] = user_input

        mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )

        state["response"] = "You're all set! We'll contact you soon."
    elif state["step"] == "platform":
        state["platform"] = user_input

    mock_lead_capture(
        state["name"],
        state["email"],
        state["platform"]
    )

    state["response"] = "You're all set! We'll contact you soon."

    # 🔥 STOP the flow completely
    state["step"] = "done"
    return state
# ---------------- GRAPH ----------------
builder = StateGraph(AgentState)

builder.add_node("intent", intent_node)
builder.add_node("greeting", greeting_node)
builder.add_node("rag", rag_node)
builder.add_node("lead", lead_flow_node)

builder.set_entry_point("intent")

builder.add_conditional_edges(
    "intent",
    lambda state: state.get("intent"),
    {
        "greeting": "greeting",
        "pricing": "rag",
        "high_intent": "lead",
        "other": "rag"
    }
)

# Loop for multi-step lead capture

builder.set_finish_point("greeting")
builder.set_finish_point("rag")
builder.set_finish_point("lead")

graph = builder.compile()

# ---------------- RUN LOOP ----------------
if __name__ == "__main__":
    state = {
        "step": None,
        "name": None,
        "email": None,
        "platform": None
    }

    

    print("🤖 AutoStream Agent Started! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        state["input"] = user_input

        result = graph.invoke(state)

        # 🔥 Maintain memory
        state.update(result)

        print("Agent:", result.get("response"))