# db_connector.py
import mysql.connector
import logging
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração para vermos mensagens de sucesso ou erro no terminal
logger = logging.getLogger(__name__)

def create_connection():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    try:
       
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME", "consultorio")
        )
        if conn.is_connected():
            logger.info("Conexão com o MySQL bem-sucedida.")
            return conn
    except mysql.connector.Error as e:
        logger.error(f"Erro ao conectar ao MySQL: {e}")
        return None