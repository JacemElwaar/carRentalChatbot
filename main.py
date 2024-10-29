# main.py

import os
from dotenv import load_dotenv
from agentes import location_agent, availability_agent, pricing_agent

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def chatbot_recommendation():
    print("Bienvenido al servicio de alquiler de coches. Vamos a hacerte algunas preguntas.")

    # Paso 1: Obtener la ubicación del cliente
    print("Por favor, introduce tu ubicación:")
    location = input()

    location_result = location_agent.run({"location": location})
    print(f"Opciones cercanas a tu ubicación: {location_result}")

    # Paso 2: Obtener las fechas del alquiler
    print("Introduce la fecha de inicio del alquiler (YYYY-MM-DD):")
    start_date = input()

    print("Introduce la fecha de finalización del alquiler (YYYY-MM-DD):")
    end_date = input()

    availability_result = availability_agent.run({"start_date": start_date, "end_date": end_date})
    print(f"Disponibilidad para las fechas indicadas: {availability_result}")

    # Paso 3: Obtener el tipo de coche y calcular el precio
    print("¿Qué tipo de coche estás buscando? (ejemplo: SUV, compacto, familiar):")
    car_type = input()

    pricing_result = pricing_agent.run({
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "car_type": car_type
    })
    print(f"El precio estimado del coche es: {pricing_result}")

if __name__ == "__main__":
    chatbot_recommendation()
