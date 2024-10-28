from ollama import Client
from .myqueue import ReverseQueue as qu 
from .task_classes import *

class LLM:
    def __init__(self, llm) -> None:
        self.llm = llm



class OLLAMA_LLM(LLM):
    def __init__(self,host, port, buffer_size=20) -> None:
        super().__init__("")
        self.llm =  Client(host=f'http://{host}:{port}')
        self.user_id_chat = {}
        self.buffer_size = buffer_size

    def create_conversation(self, message, item):
        user_id = message.from_user.id 
        if user_id not in self.user_id_chat:
            self.user_id_chat[user_id] = qu(self.buffer_size)
        user_stack = self.user_id_chat[user_id]
        if user_stack.is_full():
            user_stack.remove_rear()
        user_stack.enqueue(item)
        self.user_id_chat[user_id] = user_stack
        return user_stack.traverse()
    
    def add_to_conversation(self, message, item):
        user_id = message.from_user.id 
        if user_id not in self.user_id_chat:
            self.user_id_chat[user_id] = qu(self.buffer_size)
        user_stack = self.user_id_chat[user_id]
        if user_stack.is_full():
            user_stack.remove_rear()
        user_stack.enqueue(item)
        self.user_id_chat[user_id] = user_stack
    
    def chat(self, message):
        m = {
                'role': 'user',
                'content': message.text,
            }
        conv = self.create_conversation(message, m)
        conv.reverse()
        response = self.llm.chat(model='llama3.2:1b', messages=conv)
        self.add_to_conversation(message,response["message"])
        return response["message"]["content"]
    

    def prompt(self, txt):
        m = [{
                'role': 'user',
                'content': TASK_PROMPT(txt)
            }]
        response = self.llm.chat(model='llama3.2:1b', messages=m)
        return response["message"]["content"]