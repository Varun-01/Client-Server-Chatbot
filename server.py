import socket
import select
import sys
from threading import Thread
import json

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(5)
sockets = []
addresses = {}
messages = {"Varun":{"Meet":[]},
            "Meet":{"Varun":[]}}
clients = {"Varun":"1234",
           "Meet":"5678"}
BUFSIZE = 1024

print(f'Listening for connections at {IP}:{PORT}')

class ClientHandler(Thread):
    def __init__(self, client, address):
        global sockets
        global addresses
        Thread.__init__(self)
        self._client = client
        self._address = address

    def run(self):
        welcome = "Welcome to the server"
        self._client.send(welcome.encode("utf-8"))
        username = self._client.recv(BUFSIZE)
        username = username.decode("utf-8")
        #print(username)
        password = self._client.recv(BUFSIZE)
        password = password.decode("utf-8")
        #print(password)
        addresses[username] = self._address
        if clients[username] == password:
            result = "True"
            print(f'{username} logged in!')
            self._client.send(result.encode("utf-8"))
        else:
            result = "False"
            self._client.send(result.encode("utf-8"))
        while True:
            choice = self._client.recv(BUFSIZE)
            choice = choice.decode("utf-8")
            if choice == "1":
                self.send_clients(username)
            elif choice == "2":
                self.get_messages(username)
            elif choice == "3":
                self.receive_messages(username)
    
    def send_clients(self, username):
        print("sending client list to ", username)
        client_list = list(clients.keys())
        lst = json.dumps(client_list).encode("utf-8")
        self._client.send(lst)
    
    def get_messages(self, username):
        client_messages = messages[username]
        message = json.dumps(client_messages).encode("utf-8")
        self._client.send(message)
        for k,v in client_messages.items():
            client_messages[k] = []
    
    def receive_messages(self, username):
        package = self._client.recv(BUFSIZE)
        data = json.loads(package.decode("utf-8"))
        print("Received message for ", data[0])
        message_list = messages[data[0]]
        message_list[username].append(data[1])
        

while True:
    client, address = server_socket.accept()
    print('Connected from: ', address)
    handler = ClientHandler(client, address)
    handler.start()
    