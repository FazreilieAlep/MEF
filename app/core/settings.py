from dotenv import load_dotenv
import os

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

# Additionally, can directly add your urls here, but it does not ensure safety during deployment
# DATABASE_URL = 'postgresql+psycopg2://postgres:123456789Abc@localhost:5432/MEF_DB' # uncomment this for testing with local postgresql db
# DATABASE_URL = 'sqlite:///./mef.db' # uncomment this for testing with local sqlite db, ensure sqlite is installed, might need to add extra parameters in settings.py (refer https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts)