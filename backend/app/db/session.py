import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Dialetos aceitos nativamente sem quebrar a API ORM: postgresql://, mysql://, sqlite://, mssql+pyodbc://
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_db.sqlite")

# Se for sqlite local de fallback, requer argumento check_same_thread fora. 
# Para postgres e sql server, os argumentos default do sqlalchemy são melhores.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine agnóstica pool_pre_ping verifica a vida da conexão para cloud dbs (Supabase, Azure)
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
