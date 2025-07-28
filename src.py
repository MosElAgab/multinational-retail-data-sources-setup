import os
from sqlalchemy import create_engine, URL
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_HOST = os.getenv("RDS_HOST")
RDS_DATABASE = os.getenv("RDS_DATABASE")
RDS_PORT = os.getenv("RDS_PORT")

def init_db_engine():
    """
    Initialize a SQLAlchemy database engine for AWS RDS based on provided credentials.

    Returns:
        Engine: SQLAlchemy engine object.
    """
    DATABASE_TYPE = "postgresql"
    DBAPI = "psycopg2"
    url_object = URL.create(
        f"{DATABASE_TYPE}+{DBAPI}",
        username=RDS_USER,
        password=RDS_PASSWORD,
        host=RDS_HOST,
        database=RDS_DATABASE,
        port=RDS_PORT
    )
    engine = create_engine(url_object)
    return engine

csv_file = "./data/legacy_users.csv"

df = pd.read_csv(csv_file, index_col=False)
df.drop(columns=["Unnamed: 0"], inplace=True)

# df.drop(columns="index", inplace=True)

df.info()

engine = init_db_engine()
table_name = "legacy_users"

df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

# orders with rds as well