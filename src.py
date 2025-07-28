from sqlalchemy import create_engine, URL
import pandas as pd


RDS_USER = "retail_admin"
RDS_PASSWORD = "retail_admin_1234"
RDS_HOST= "multinational-retail.c7kegm862wks.eu-west-2.rds.amazonaws.com"
RDS_DATABASE="retail"
RDS_PORT="5432"

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