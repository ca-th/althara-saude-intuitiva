import mysql.connector
import logging
import os
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)

def create_connection():
    
    try:
        
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME", "consultorio"),
            charset='utf8mb4'
        )
        if conn.is_connected():
            logger.info("Conexão com o MySQL bem-sucedida.")
            return conn
    except mysql.connector.Error as e:
        logger.error(f"Erro ao conectar ao MySQL: {e}")
        return None

