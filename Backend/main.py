# Conteúdo completo e corrigido para o arquivo: Backend/main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests
import schemas
import models
from database import get_db
from schemas import ChatMessage, ChatResponse
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

# Lista de origens permitidas
origins = [
    "http://localhost:4200", # A origem do seu app Angular
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTA DE ESPECIALIDADES ---
@app.get("/especialidades", response_model=List[schemas.Especialidade])
def listar_especialidades(db: Session = Depends(get_db)):
    """
    Retorna uma lista de todas as especialidades médicas.
    """
    especialidades = db.query(models.Especialidade).all()
    if not especialidades:
        raise HTTPException(status_code=404, detail="Nenhuma especialidade encontrada")
    return especialidades

# --- ROTA DE MÉDICOS POR ESPECIALIDADE (ALINHAMENTO CORRIGIDO) ---
@app.get("/especialidades/{id_especialidade}/medicos", response_model=List[schemas.Medico])
def listar_medicos_por_especialidade(id_especialidade: int, db: Session = Depends(get_db)):
    """
    Retorna uma lista de médicos para uma especialidade específica.
    """
    medicos = db.query(models.Medico).filter(models.Medico.id_especialidade == id_especialidade).all()
    if not medicos:
        # É normal não encontrar médicos, então retornamos uma lista vazia
        return []
    return medicos

# --- SUAS OUTRAS ROTAS ---
@app.get("/")
def root():
    return {"message": "API rodando! Acesse /chat para conversar com a IA."}

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.post("/chat", response_model=ChatResponse)
async def chat_with_rasa(chat_message: ChatMessage):
    payload = {
        "sender": "usuario123",
        "message": chat_message.message
    }

    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        rasa_reply = response.json()

        if rasa_reply:
            # --- CORREÇÃO AQUI ---
            # Pegamos o texto de TODAS as respostas que o bot enviou
            bot_messages = [reply["text"] for reply in rasa_reply]
            
            # Juntamos todas as mensagens em um único texto, separando por quebras de linha
            full_response = "\n".join(bot_messages)
            
            return {"response": full_response}
        else:
            return {"response": "Desculpe, não recebi resposta da IA."}
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Rasa: {str(e)}")
