# agents.py

import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Inicializar el modelo de Groq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=200,
)

# Prompt para el Agente de Localización
localization_prompt = PromptTemplate.from_template(
    "Estás buscando oficinas de alquiler de coches en {location}. ¿Cuáles son las opciones cercanas?"
)

# Prompt para el Agente de Disponibilidad
availability_prompt = PromptTemplate.from_template(
    "Verifica la disponibilidad de coches desde {start_date} hasta {end_date}."
)

# Prompt para el Agente de Precios
pricing_prompt = PromptTemplate.from_template(
    "Calcula el precio del coche disponible en {location} del {start_date} al {end_date}. El cliente necesita un coche de tipo {car_type}."
)

# Crear las cadenas de agentes usando los prompts y el LLM
location_agent = LLMChain(prompt=localization_prompt, llm=llm)
availability_agent = LLMChain(prompt=availability_prompt, llm=llm)
pricing_agent = LLMChain(prompt=pricing_prompt, llm=llm)

# Exportar los agentes
__all__ = ["location_agent", "availability_agent", "pricing_agent"]
