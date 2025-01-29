"""Cliente para simular a comunicação com o servidor"""
import socket
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))


def client_simulation(host: str, port: int, filename: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Conexão estabelecida com o servidor")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            messages = file.readlines()
        
        for msg in messages:
            msg = msg.strip()
            if msg:
                client_socket.send(msg.encode())
                response = client_socket.recv(1024).decode()
                print(f"Resposta do servidor: {response}")
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado")
    finally:
        client_socket.close()
    
    
def main():
    client_simulation(SERVER_HOST, SERVER_PORT, "messages.txt")    
