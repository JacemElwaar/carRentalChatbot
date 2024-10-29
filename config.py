import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Acceder a las variables de entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
