# This file contains functions to interact with the MySQL database using SQLAlchemy.


from sqlalchemy import create_engine
import pandas as pd

# Replace with your actual database URL 

username ="root"
password =""

DATABASE_URL = f"mysql+pymysql://{username}:{password}@localhost/carRental"

engine = create_engine(DATABASE_URL)

def query_database(query: str) -> pd.DataFrame:
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def run_sql_file(sql_file_path: str) -> pd.DataFrame:
    with engine.connect() as connection:
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        result = connection.execute(sql_script)
    return pd.DataFrame(result.fetchall(), columns=result.keys())




