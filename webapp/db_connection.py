import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)