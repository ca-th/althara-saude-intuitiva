from pydantic import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    nome: str
    email:str

class Medico(BaseModel):
    id_medico: int
    nome: str
    id_especialidade: int

    
    class Config:
       
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

    class Config:
        
        orm_mode = True

class UserCreate(BaseModel):
    nome: str
    email: str
    password: str

#retorna os dados
class User(BaseModel):
    id_usuario: int
    nome: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None