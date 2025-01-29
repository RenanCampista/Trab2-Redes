"""Funções para o servidor de mensagens."""
import socket
import threading
from priority_queue.priority_queue import PriorityQueue
import random
import time


class MessageServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.priority_queue = PriorityQueue()
        self.running = True
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")
        
        threading.Thread(target=self.process_messages, daemon=True).start()
        
        while self.running:
            client_socket, address = self.server_socket.accept()
            print(f"Conexão aceita de {address}")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            
    def handle_client(self, client_socket: socket.socket):
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                
                priority = classify_priority()
                self.priority_queue.add_message(priority, message)
                print(f"Mensagem recebida: {message} (prioridade: {priority})")
                client_socket.send("Mensagem recebida e classificada".encode())
        except ConnectionResetError:
            print("Conexão encerrada pelo cliente")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
        finally:
            client_socket.close()
            
    def process_messages(self):
        while self.running:
            if not self.priority_queue.is_empty():
                priority, message = self.priority_queue.get_message()
                print(f"Mensagem processada: {message} (prioridade: {priority})")
                time.sleep(2)
                
    def stop(self):
        self.running = False
        self.server_socket.close()
                       
                
def classify_priority() -> int:
    """Classifica aleatoriamente a prioridade de uma mensagem."""
    return random.randint(1, 3)