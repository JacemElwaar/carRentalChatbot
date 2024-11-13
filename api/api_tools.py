# This file contains functions to interact with the Sanic API from your application.

import requests

def query_database_via_api(query: str) -> dict:
    response = requests.post("http://localhost:8000/query_database", json={"query": query})
    response.raise_for_status()
    return response.json()

def run_sql_file_via_api(sql_file_path: str) -> dict:
    response = requests.post("http://localhost:8000/run_sql_file", json={"sql_file_path": sql_file_path})
    response.raise_for_status()
    return response.json()


