from transformers import pipeline
from collections import defaultdict
from stateGraph import StateGraph  # Import the StateGraph from the separate file

# Multi-label zero-shot classifier setup
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
INTENTS = ["location", "availability", "pricing"]

class UserSession:
    def __init__(self, state_graph):
        self.context = defaultdict(str)
        self.completed_tasks = set()
        self.current_state = "initial"  # Start at the initial state
        self.state_graph = state_graph  # Assign the StateGraph instance

    def update_context(self, key, value):
        self.context[key] = value

    def transition_state(self, intent):
        # Use the state graph to determine the next state
        next_state = self.state_graph.get_next_state(self.current_state, intent)
        if next_state != self.current_state:  # Only update if there's a valid transition
            self.current_state = next_state
            return True
        return False

class SupervisorAgent:
    def __init__(self):
        #self.location_agent = location_agent
        #self.availability_agent = availability_agent
        #self.pricing_agent = pricing_agent
        self.sessions = defaultdict(lambda: UserSession(StateGraph()))  # Each session gets its own UserSession with StateGraph

    def route_request(self, user_input, user_id):
        session = self.sessions[user_id]
        
        # Identify multiple intents with multi-label classification
        intents = self.identify_intents(user_input)
        print(f"Detected intents for user '{user_id}': {intents}")  # Log detected intents

        responses = []
        # Trigger agents based on detected intents and state transitions
        for intent in intents:
            if intent == "location" and "location" not in session.completed_tasks:
                if session.transition_state("location"):
                    # Commenting out the agent call
                    # location_response = self.location_agent.run({"location": user_input})
                    location_response = f"Simulated location response for intent: {intent}"
                    session.update_context("location", location_response)
                    responses.append(location_response)
                    session.completed_tasks.add("location")
                    print(f"localtion intent and the session is {session}")  # Log context update
            
            elif intent == "availability" and "availability" not in session.completed_tasks:
                if session.transition_state("availability"):
                    start_date = session.context.get("start_date", "today")
                    end_date = session.context.get("end_date", "tomorrow")
                    # Commenting out the agent call
                    # availability_response = self.availability_agent.run({
                    #     "start_date": start_date,
                    #     "end_date": end_date
                    # })
                    availability_response = f"Simulated availability response for intent: {intent}"
                    session.update_context("availability", availability_response)
                    responses.append(availability_response)
                    session.completed_tasks.add("availability")
                    print(f"availability intent and the session {session}")  # Log context update

            elif intent == "pricing" and "pricing" not in session.completed_tasks:
                if session.transition_state("pricing"):
                    location = session.context.get("location", "unspecified location")
                    start_date = session.context.get("start_date", "today")
                    end_date = session.context.get("end_date", "tomorrow")
                    car_type = session.context.get("car_type", "sedan")
                    # Commenting out the agent call
                    # pricing_response = self.pricing_agent.run({
                    #     "location": location,
                    #     "start_date": start_date,
                    #     "end_date": end_date,
                    #     "car_type": car_type
                    # })
                    pricing_response = f"Simulated pricing response for intent: {intent}"
                    session.update_context("pricing", pricing_response)
                    responses.append(pricing_response)
                    session.completed_tasks.add("pricing")
                    print(f"pricing intent and the session {session}")  # Log context update

            # Log the current session state after each intent is processed
            print(f"Current state for user '{user_id}': {session.current_state}")
            print(f"Completed tasks for user '{user_id}': {session.completed_tasks}")

        return " ".join(responses)

    def identify_intents(self, user_input):
        # Perform multi-label classification with confidence threshold
        result = intent_classifier(user_input, candidate_labels=INTENTS, multi_label=True)
        detected_intents = [intent for intent, score in zip(result["labels"], result["scores"]) if score > 0.6]  # Set threshold as needed
        return detected_intents

