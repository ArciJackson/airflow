from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_CONFIG

DATABASE_URL = (
  f"mssql+pyodbc://{DATABASE_CONFIG['UID']}:{DATABASE_CONFIG['PWD']}@"
  f"{DATABASE_CONFIG['SERVER']}/{DATABASE_CONFIG['DATABASE']}?"
  "driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()