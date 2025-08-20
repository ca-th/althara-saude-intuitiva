# Conteúdo para o novo arquivo: Backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ATENÇÃO: Substitua com os dados de acesso do seu banco de dados MySQL
# Formato: "mysql+pymysql://USUARIO:SENHA@SERVIDOR/NOME_DO_BANCO"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:cat1234@localhost/consultorio"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Esta é a função que o main.py precisa para se conectar ao banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()