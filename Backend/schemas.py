from pydantic import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    nome: str
    email:str

class Medico(BaseModel):
    id_medico: int
    nome: str
    id_especialidade: int

    # --- CORREÇÃO AQUI ---
    class Config:
        # Troque 'from_attributes = True' por 'orm_mode = True'
        orm_mode = True

class Horario(BaseModel):
    data_hora: datetime

class Consulta(BaseModel):
    especialidade: str
    medico: str

class Agendamento(BaseModel):
    horario: datetime
    medico: str
    usuario: str


class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class Especialidade(BaseModel):
    id_especialidade: int
    nome: str

    # ESTA PARTE É A SOLUÇÃO
    class Config:
        # Se você usa Pydantic v2 (mais novo), esta linha é a correta
        #from_attributes = True
        
        # Se a linha de cima der erro, apague-a e use esta (para Pydantic v1):
        orm_mode = True