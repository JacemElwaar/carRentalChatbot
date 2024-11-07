from sanic import Sanic
from sanic.response import json
from api.database import query_database, run_sql_file

app = Sanic("CarRentalAPI")

@app.post("/query_database")
async def query_database_endpoint(request):
    query = request.json.get("query")
    result = query_database(query)
    return json(result.to_dict(orient="records"))

@app.post("/run_sql_file")
async def run_sql_file_endpoint(request):
    sql_file_path = request.json.get("sql_file_path")
    result = run_sql_file(sql_file_path)
    return json(result.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)