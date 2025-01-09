from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('MYSQL_ROOT_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

print(f"DB_USER: {db_user}")
print(f"DB_PASSWORD: {db_password}")
print(f"DB_HOST: {db_host}")
print(f"DB_PORT: {db_port}")
print(f"DB_NAME: {db_name}")

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import backend.db_files.models
    Base.metadata.create_all(bind=engine)

## initialize here?
init_db()