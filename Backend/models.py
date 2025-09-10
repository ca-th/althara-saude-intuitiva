from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Especialidade(Base):
    __tablename__ = "especialidades"

    id_especialidade = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)

class Medico(Base):
    __tablename__ = "medicos"
    id_medico = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)
    id_especialidade = Column(Integer, ForeignKey("especialidades.id_especialidade"))

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    cpf = Column(String(20), unique=True, index=True, nullable=True) 
    telefone = Column(String(20), nullable=True)