import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Groq model with specified parameters
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=200,
)

# Define prompt templates for each agent

# Location Agent Prompt Template
location_prompt = PromptTemplate.from_template(
    "You are looking for car rental offices in {location}. What nearby options are available?"
)

# Availability Agent Prompt Template
availability_prompt = PromptTemplate.from_template(
    "Check the availability of cars from {start_date} to {end_date}."
)

# Pricing Agent Prompt Template
pricing_prompt = PromptTemplate.from_template(
    "Calculate the price for a car rental in {location} from {start_date} to {end_date}. The customer needs a {car_type} car."
)

# Instantiate the LLMChain agents using the prompts and model
location_agent = LLMChain(prompt=location_prompt, llm=llm)
availability_agent = LLMChain(prompt=availability_prompt, llm=llm)
pricing_agent = LLMChain(prompt=pricing_prompt, llm=llm)

# Export agents for use in SupervisorAgent
__all__ = ["location_agent", "availability_agent", "pricing_agent"]
