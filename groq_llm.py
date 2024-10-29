from langchain.llms.base import LLM
from typing import Optional, List
from groq import GroqModel
import os

class GroqLLM(LLM):
    """LLM que usa el modelo de Groq a través de su SDK."""

    api_key: Optional[str] = None  # Puedes pasar la API key aquí si es necesario.

    def __init__(self, api_key: Optional[str] = None):
        """Inicializa el modelo con la API key."""
        super().__init__()
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Debes proporcionar una clave API para Groq.")
        self.model = GroqModel(api_key=self.api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Ejecuta el modelo Groq con el prompt proporcionado."""
        response = self.model.run(input_text=prompt)
        return response

    @property
    def _identifying_params(self) -> dict:
        return {"model": "groq"}

    @property
    def llm_type(self) -> str:
        return "groq"

