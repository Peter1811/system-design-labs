import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASE_URL = os.getenv('DATABASE_URL')
# DATABASE_URL = 'postgresql+psycopg2://postgres:1811@localhost:5432/postgres'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
