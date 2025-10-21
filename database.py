from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')


DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@localhost/{database}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine, autocommit=False, autoflush=False)
Base = declarative_base()