"""Módulo do servidor de mensagens."""
import socket
import threading
from priority_queue.priority_queue import PriorityQueue
import random
import time
import logging

logger = logging.getLogger(__name__)


class MessageServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.priority_queue = PriorityQueue()
        self.running = True
        
    def start(self):
        """Inicia o servidor de mensagens."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            logger.info(f"Servidor iniciado em {self.host}:{self.port}")
            
            threading.Thread(target=self.process_messages, daemon=True).start()
            
            while self.running:
                client_socket, address = self.server_socket.accept()
                logger.info(f"Conexão aceita de {address}")
                threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True).start()
        except socket.timeout:
            logger.error("Tempo de conexão esgotado.")
        except OSError as e:
            logger.error(f"Erro de socket: {e}")
        except KeyboardInterrupt:
            logger.info("Servidor interrompido pelo usuário.")
            self.stop()
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
        finally:
            self.server_socket.close()
            
    def handle_client(self, client_socket: socket.socket, addr: str):
        """Lida com as mensagens recebidas de um cliente."""
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                priority = classify_priority()
                self.priority_queue.add_message(priority, message)
                logger.info(f"\033[34mRequisição recebida de {addr}:\033[0m {message} (prioridade: {priority})")
                client_socket.send("Mensagem recebida e classificada".encode())
        except ConnectionResetError:
            logger.warning(f"Conexão encerrada por {addr}")
        except socket.timeout:
            logger.error(f"Tempo de conexão esgotado para {addr}")
        except OSError as e:
            logger.error(f"Erro de socket com {addr}: {e}")
        except Exception as e:
            logger.error(f"Erro ao lidar com a requisição de {addr}: {e}")
        finally:
            client_socket.close()
            
    def process_messages(self):
        """Processa as mensagens da fila de prioridade."""
        while self.running:
            if not self.priority_queue.is_empty():
                priority, message = self.priority_queue.get_message()
                logger.info(f"\033[32mMensagem processada:\033[0m {message} (prioridade: {priority})")
                time.sleep(2)
                
    def stop(self):
        """Para o servidor de mensagens."""
        self.running = False
        self.server_socket.close()
                       
                
def classify_priority() -> int:
    """Classifica aleatoriamente a prioridade de uma mensagem."""
    return random.randint(1, 3)