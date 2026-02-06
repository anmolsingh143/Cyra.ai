def reset_node(state):
    print("[RESET] Reset node called")

    state["awaiting_field"] = None
    state["sender_filter"] = None

    state["response"] = "Okay, I've reset the conversation. What would you like to do next?"
    return state
