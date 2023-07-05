from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

DEBUG = True
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SQLALCHEMY_DATABASE_URI = f'mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SECRET_KEY = os.getenv("SECRET_KEY")
