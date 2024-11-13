from transformers import pipeline
from collections import defaultdict
from agentes import location_agent, availability_agent, pricing_agent

# Multi-label zero-shot classifier setup
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
INTENTS = ["location", "availability", "pricing"]

class UserSession:
    def __init__(self):
        self.context = defaultdict(str)
        self.completed_tasks = set()  # Track which agents have been used

    def update_context(self, key, value):
        self.context[key] = value

class EnhancedSupervisorAgent:
    def __init__(self, location_agent, availability_agent, pricing_agent):
        self.location_agent = location_agent
        self.availability_agent = availability_agent
        self.pricing_agent = pricing_agent
        self.sessions = defaultdict(UserSession)

    def route_request(self, user_input, user_id):
        session = self.sessions[user_id]
        
        # Identify multiple intents with multi-label classification
        intents = self.identify_intents(user_input)

        responses = []
        # Trigger agents based on detected intents
        if "location" in intents and "location" not in session.completed_tasks:
            location_response = self.location_agent.run({"location": user_input})
            session.update_context("location", location_response)
            responses.append(location_response)
            session.completed_tasks.add("location")
        
        if "availability" in intents and "availability" not in session.completed_tasks:
            # Use context information or fallbacks
            start_date = session.context.get("start_date", "today")
            end_date = session.context.get("end_date", "tomorrow")
            availability_response = self.availability_agent.run({
                "start_date": start_date,
                "end_date": end_date
            })
            session.update_context("availability", availability_response)
            responses.append(availability_response)
            session.completed_tasks.add("availability")

        if "pricing" in intents and "pricing" not in session.completed_tasks:
            # Use context or default values
            location = session.context.get("location", "unspecified location")
            start_date = session.context.get("start_date", "today")
            end_date = session.context.get("end_date", "tomorrow")
            car_type = session.context.get("car_type", "sedan")
            pricing_response = self.pricing_agent.run({
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "car_type": car_type
            })
            session.update_context("pricing", pricing_response)
            responses.append(pricing_response)
            session.completed_tasks.add("pricing")

        # Combine all agent responses for the user
        return " ".join(responses)

    def identify_intents(self, user_input):
        # Perform multi-label classification with confidence threshold
        result = intent_classifier(user_input, candidate_labels=INTENTS, multi_label=True)
        detected_intents = [intent for intent, score in zip(result["labels"], result["scores"]) if score > 0.6]  # Set threshold as needed
        return detected_intents

# Initialize the supervisor agent with each specific agent
supervisor_agent = EnhancedSupervisorAgent(location_agent, availability_agent, pricing_agent)
