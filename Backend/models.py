# No arquivo: Backend/models.py
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