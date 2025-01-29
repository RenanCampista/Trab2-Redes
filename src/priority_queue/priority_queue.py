"""Módulo para a implementação de uma fila de prioridade."""
import queue


class PriorityQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()
        
    def add_message(self, priority: int, message: str):
        self.queue.put((priority, message))
        
    def get_message(self):
        return self.queue.get()
    
    def is_empty(self):
        return self.queue.empty()