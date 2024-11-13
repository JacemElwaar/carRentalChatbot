class StateGraph:
    def __init__(self):
        # Define possible states and allowed transitions
        self.states = {
            "initial": ["location", "availability", "pricing"],
            "location": ["availability"],
            "availability": ["pricing"],
            "pricing": ["complete"],
            "complete": []  # End of the flow
        }

    def get_next_state(self, current_state, intent):
        # Determines the next state based on the current state and detected intent
        if intent in self.states[current_state]:
            return intent
        return "initial"  # Fallback to initial state if intent is invalid
