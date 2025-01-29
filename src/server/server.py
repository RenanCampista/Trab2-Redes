"""Módulo principal do servidor de mensagens."""
from message_server.message_server import MessageServer
import threading
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))


def main():
    server = MessageServer(SERVER_HOST, SERVER_PORT)
    threading.Thread(target=server.start, daemon=True).start()
    
    input("Pressione Enter para encerrar o servidor...\n")
    server.stop()
    print("Servidor encerrado")
