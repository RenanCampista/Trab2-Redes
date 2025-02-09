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
        self.running = True # Variável de controle para parar o servidor
        self.client_sockets = {} # Dicionário para armazenar os sockets dos clientes
        
    def start(self):
        """Inicia o servidor de mensagens."""
        try:
            self.server_socket.bind((self.host, self.port)) # Associa o socket a um endereço e porta
            self.server_socket.listen(5) # Define o número máximo de conexões pendentes 
            logger.info(f"Servidor iniciado em {self.host}:{self.port}")
            
            # Inicia a thread responsável por processar mensagens da fila de prioridade
            threading.Thread(target=self.process_messages, daemon=True).start()
            
            while self.running:
                client_socket, address = self.server_socket.accept()
                logger.info(f"Conexão aceita de {address}")
                self.client_sockets[address] = client_socket # Armazena o socket do cliente
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
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
    def handle_client(self, client_socket: socket.socket, addr: str):
        """Lida com as mensagens recebidas de um cliente."""
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                priority = classify_priority()
                self.priority_queue.add_message(priority, (addr, message)) # Armazena o endereço junto com a mensagem
                logger.info(f"\033[34mRequisição recebida de {addr}:\033[0m {message} (prioridade: {priority})")
                client_socket.send(f"\033[34mMensagem recebida e enviada para a fila\033[0m".encode()) # Envia uma resposta ao cliente
        except ConnectionResetError:
            logger.warning(f"Conexão encerrada por {addr}")
        except socket.timeout:
            logger.error(f"Tempo de conexão esgotado para {addr}")
        except OSError as e:
            logger.error(f"Erro de socket com {addr}: {e}")
        except Exception as e:
            logger.error(f"Erro ao lidar com a requisição de {addr}: {e}")
        finally:
            if client_socket:
                client_socket.close()
            
    def process_messages(self):
        """Processa as mensagens da fila de prioridade."""
        while self.running:
            if not self.priority_queue.is_empty():
                priority, (addr, message) = self.priority_queue.get_message()
                logger.info(f"\033[32mMensagem processada:\033[0m {message} (prioridade: {priority})")
                time.sleep(2) # Simula tempo de processamento 
                # Envia uma notificação ao cliente
                if addr in self.client_sockets:
                    client_socket = self.client_sockets[addr]
                    try:
                        client_socket.send(f"\033[32mMensagem processada:\033[0m {message}".encode())
                    except Exception as e:
                        logger.error(f"Erro ao enviar notificação para {addr}: {e}")
            time.sleep(1)
               
    def stop(self):
        """Para o servidor de mensagens."""
        self.running = False
                       
                
def classify_priority() -> int:
    """Classifica aleatoriamente a prioridade de uma mensagem."""
    # 1: Alta prioridade, 2: Média prioridade, 3: Baixa prioridade
    return random.randint(1, 3)