"""Módulo principal do servidor de mensagens."""
from message_server.message_server import MessageServer
import threading
from dotenv import load_dotenv
import os
import logging

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
LOG_FILE = os.getenv("SERVER_LOG_FILE")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE)],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    global logger
    logger = logging.getLogger(__name__)
    
    server = MessageServer(SERVER_HOST, SERVER_PORT)
    threading.Thread(target=server.start, daemon=True).start()
    
    input("Pressione Enter para encerrar o servidor...\n")
    server.stop()
    logger.info("Servidor encerrado")
