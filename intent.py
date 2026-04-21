def intent_node(state):
    user_input = state.get("input", "").lower()

    if "buy" in user_input:
        state["intent"] = "high_intent"
    elif "price" in user_input or "plan" in user_input:
        state["intent"] = "pricing"
    else:
        state["intent"] = "other"

    return state