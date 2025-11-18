from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Configuração para o URL do banco de dados (prioriza ENV para deploy)
# Se não estiver definido, usa SQLite para desenvolvimento local
SQLALCHEMY_DATABASE_URL = config(
    'DATABASE_URL', 
    default="sqlite:///./move_database.db"
)

# Configuração do engine
# 'connect_args' é necessário para SQLite com FastAPI (multithreading)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para todos os modelos de DB
Base = declarative_base()

# Função de Dependência para o FastAPI (Injeção de Sessão)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()