# no agents for the moment => from agentes import location_agent, availability_agent, pricing_agent

# Initialize SupervisorAgent with the configured agents
# in the future it will be like this => supervisor_agent = SupervisorAgent(location_agent, availability_agent, pricing_agent)
from supervisor_agents_state_graph import SupervisorAgent


supervisor_agent = SupervisorAgent()

# Example of handling a user query
user_query = "How much does it cost to rent a sedan in New York from tomorrow to next week?"
user_id = "id_user_123"  # Unique identifier for each user session

# Process the user query and get the response
response = supervisor_agent.route_request(user_query, user_id)
print(response)  # This will output the combined responses based on the query.
