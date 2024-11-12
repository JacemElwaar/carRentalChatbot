from transformers import pipeline
from collections import defaultdict
from agentes import location_agent, availability_agent, pricing_agent

# Use Hugging Face's zero-shot classification for dynamic intent detection
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
INTENTS = ["location", "availability", "pricing", "unknown"]

class UserSession:
    def __init__(self):
        self.context = defaultdict(str)
    
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
        intent = self.identify_intent(user_input)

        # Update session context
        session.update_context("last_user_input", user_input)

        # Route request based on intent and provide context-aware responses
        if intent == "location":
            response = self.location_agent.run({"location": user_input})
            session.update_context("last_response", response)
            return response
        elif intent == "availability":
            # Retrieve dates from context or fallback to user input
            start_date = session.context.get("start_date", "today")
            end_date = session.context.get("end_date", "tomorrow")
            response = self.availability_agent.run({"start_date": start_date, "end_date": end_date})
            session.update_context("last_response", response)
            return response
        elif intent == "pricing":
            # Retrieve location, dates, and car type from context or fallback to user input
            location = session.context.get("location", "unspecified location")
            start_date = session.context.get("start_date", "today")
            end_date = session.context.get("end_date", "tomorrow")
            car_type = session.context.get("car_type", "sedan")
            response = self.pricing_agent.run({"location": location, "start_date": start_date, "end_date": end_date, "car_type": car_type})
            session.update_context("last_response", response)
            return response
        else:
            # Fallback response if intent is unknown
            return "Lo siento, no pude entender tu solicitud. ¿Podrías reformularla, por favor?"

    def identify_intent(self, user_input):
        # Use zero-shot classifier to identify intent with Hugging Face
        result = intent_classifier(user_input, candidate_labels=INTENTS)
        top_intent = result["labels"][0]
        return top_intent if result["scores"][0] > 0.8 else "unknown"  # Confidence threshold of 0.8

# Initialize the supervisor agent with the agents
supervisor_agent = EnhancedSupervisorAgent(location_agent, availability_agent, pricing_agent)
