# Conteúdo final e corrigido para o arquivo: Backend/main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List

from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from security import get_password_hash 

app = FastAPI()

origins = [
    "http://localhost:4200", 
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/especialidades", response_model=List[schemas.Especialidade])
def listar_especialidades(db: Session = Depends(get_db)):
    """
    Retorna uma lista de todas as especialidades médicas.
    """
    especialidades = db.query(models.Especialidade).all()
    if not especialidades:
        raise HTTPException(status_code=404, detail="Nenhuma especialidade encontrada")
    return especialidades


@app.get("/especialidades/{id_especialidade}/medicos", response_model=List[schemas.Medico])
def listar_medicos_por_especialidade(id_especialidade: int, db: Session = Depends(get_db)):
    """
    Retorna uma lista de médicos para uma especialidade específica.
    """
    medicos = db.query(models.Medico).filter(models.Medico.id_especialidade == id_especialidade).all()
    if not medicos:
        return []
    return medicos


@app.post("/usuarios/", response_model=schemas.User)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.
    """

    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
        
    # criptografa a senha antes de salvar
    hashed_password = get_password_hash(user.password)
    
    #  objeto de usuário com a senha já criptografada
    novo_usuario = models.Usuario(
        nome=user.nome,
        email=user.email,
        hashed_password=hashed_password
    )
   
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

@app.get("/")
def root():
    return {"message": "API rodando! Acesse /chat para conversar com a IA."}

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

@app.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_rasa(chat_message: schemas.ChatMessage):
    payload = {
        "sender": "usuario123",
        "message": chat_message.message
    }

    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        rasa_reply = response.json()

        if rasa_reply:
            bot_messages = [reply["text"] for reply in rasa_reply]
            full_response = "\n".join(bot_messages)
            return {"response": full_response}
        else:
            return {"response": "Desculpe, não recebi resposta da IA."}
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Rasa: {str(e)}")