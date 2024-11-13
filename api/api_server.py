import logging
from sanic import Sanic
from sanic.response import json
from database import query_database, run_sql_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic("CarRentalAPI")

@app.middleware('response')
async def log_response(request, response):
    if response.status >= 400:
        logger.error(f"Error response: {response.status} - {response.body}")

@app.post("/query_database")
async def query_database_endpoint(request):
    try:
        query = request.json.get("query")
        result = query_database(query)
        return json(result.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        return json({"error": str(e)}, status=500)

@app.get("/cars")
async def get_all_cars(request):
    try:
        query = "SELECT * FROM cars;"
        result = query_database(query)
        return json(result.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return json({"error": str(e)}, status=500) 

@app.get("/feedback")
async def get_all_feedbacks(request):
    try:
        query = "SELECT * FROM feedback;"
        result = query_database(query)
        return json(result.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return json({"error": str(e)}, status=500) 


    


@app.post("/run_sql_file")
async def run_sql_file_endpoint(request):
    try:
        sql_file_path = request.json.get("sql_file_path")
        result = run_sql_file(sql_file_path)
        return json(result.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Error running SQL file: {e}")
        return json({"error": str(e)}, status=500)

@app.get("/")
async def hello(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)