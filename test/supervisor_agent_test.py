import unittest
from supervisor_agents_state_graph import SupervisorAgent
from unittest.mock import Mock

class TestSupervisorAgent(unittest.TestCase):
    def setUp(self):
        # Mock the agents
        self.location_agent = Mock()
        self.availability_agent = Mock()
        self.pricing_agent = Mock()

        # Initialize the supervisor agent with the mocked agents
        self.supervisor_agent = SupervisorAgent(
            self.location_agent, self.availability_agent, self.pricing_agent
        )

        # Mock session
        self.session = Mock()
        self.session.context = {}
        self.session.completed_tasks = set()

    def test_location_intent(self):
        # Mock the response from the location agent
        self.location_agent.run.return_value = "Location response"

        # Simulate user input for location intent
        user_input = "I am in New York"
        self.session.context["state"] = "initial"
        response = self.supervisor_agent.handle_user_input(user_input, self.session)

        # Verify the response
        self.assertEqual(response, "Location response")
        self.location_agent.run.assert_called_once_with({"location": user_input})
        self.assertIn("location", self.session.context)
        self.assertIn("location", self.session.completed_tasks)

    def test_availability_intent(self):
        # Mock the response from the availability agent
        self.availability_agent.run.return_value = "Availability response"

        # Simulate user input for availability intent
        user_input = "Check availability from 2023-01-01 to 2023-01-10"
        self.session.context["state"] = "location_collected"
        self.session.context["start_date"] = "2023-01-01"
        self.session.context["end_date"] = "2023-01-10"
        response = self.supervisor_agent.handle_user_input(user_input, self.session)

        # Verify the response
        self.assertEqual(response, "Availability response")
        self.availability_agent.run.assert_called_once_with({
            "start_date": "2023-01-01",
            "end_date": "2023-01-10"
        })
        self.assertIn("availability", self.session.context)
        self.assertIn("availability", self.session.completed_tasks)

    def test_pricing_intent(self):
        # Mock the response from the pricing agent
        self.pricing_agent.run.return_value = "Pricing response"

        # Simulate user input for pricing intent
        user_input = "What is the price for an SUV?"
        self.session.context["state"] = "availability_collected"
        self.session.context["location"] = "New York"
        self.session.context["start_date"] = "2023-01-01"
        self.session.context["end_date"] = "2023-01-10"
        self.session.context["car_type"] = "SUV"
        response = self.supervisor_agent.handle_user_input(user_input, self.session)

        # Verify the response
        self.assertEqual(response, "Pricing response")
        self.pricing_agent.run.assert_called_once_with({
            "location": "New York",
            "start_date": "2023-01-01",
            "end_date": "2023-01-10",
            "car_type": "SUV"
        })
        self.assertIn("pricing", self.session.context)
        self.assertIn("pricing", self.session.completed_tasks)

if __name__ == "__main__":
    unittest.main()