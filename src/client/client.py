"""Cliente para simular a comunicação com o servidor"""
import socket
from dotenv import load_dotenv
import os
import threading
import time
import random
import logging

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
LOG_FILE = os.getenv("CLIENT_LOG_FILE")

def client_simulation(host: str, port: int, filename: str):
    """Simula a comunicação de um único cliente com o servidor."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        logging.info("Conexão estabelecida com o servidor")

        try:
            with open(filename, "r", encoding="utf-8") as file:
                messages = file.readlines()
            
            for msg in messages:
                msg = msg.strip()
                if msg:
                    client_socket.send(msg.encode())
                    response = client_socket.recv(1024).decode()
                    logging.info(f"Cliente enviou: {msg} | Servidor respondeu: {response}")
        except FileNotFoundError:
            logging.error(f"Arquivo {filename} não encontrado.")
        finally:
            client_socket.close()
    except ConnectionRefusedError:
        logging.error("Conexão recusada pelo servidor.")
    except socket.timeout:
        logging.error("Tempo de conexão esgotado.")
    except OSError as e:
        logging.error(f"Erro de socket: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")


def client_thread(host, port, messages):
    """Envia mensagens para o servidor e imprime a resposta."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        try:
            for msg in messages:
                msg = msg.strip()
                if msg:
                    client_socket.send(msg.encode())
                    response = client_socket.recv(1024).decode()
                    logging.info(f"Cliente enviou: {msg} | Servidor respondeu: {response}")
                time.sleep(random.uniform(1, 3))
        finally:
            client_socket.close()
    except ConnectionRefusedError:
        logging.error("Conexão recusada pelo servidor.")
    except socket.timeout:
        logging.error("Tempo de conexão esgotado.")
    except OSError as e:
        logging.error(f"Erro de socket: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")


def multiple_client_simulation(host: str, port: int, filename: str, num_clients: int):
    """Simula a comunicação de vários clientes com o servidor."""
    logging.info(f"Simulando comunicação de {num_clients} clientes com o servidor")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            messages = file.readlines()
        
        chunk_size = max(1, len(messages) // num_clients)
        threads = []

        for i in range(num_clients):
            chunk = messages[i * chunk_size:(i + 1) * chunk_size]
            thread = threading.Thread(target=client_thread, args=(host, port, chunk))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except FileNotFoundError:
        logging.error(f"Arquivo {filename} não encontrado.")
    except ConnectionRefusedError:
        logging.error("Conexão recusada pelo servidor.")
    except socket.timeout:
        logging.error("Tempo de conexão esgotado.")
    except OSError as e:
        logging.error(f"Erro de socket: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")

    
def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE)],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    #client_simulation(SERVER_HOST, SERVER_PORT, "messages.txt")    
    num_clients = random.randint(2, 5)
    multiple_client_simulation(SERVER_HOST, SERVER_PORT, "messages.txt", num_clients)