import socket
import select
import errno
import json


HEADER_LENGTH = 10
BUFSIZE = 1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
priv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
priv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def login():
    IP = input("Enter IP address: ")
    PORT = int(input("Enter Port number: "))
    client_socket.connect((IP, PORT))
    message = client_socket.recv(BUFSIZE)
    print(message.decode("utf-8"))
    user = input("Enter Username: ")
    user = user.encode("utf-8")
    client_socket.send(user)
    pwd = input("Enter Password: ")
    pwd = pwd.encode("utf-8")
    client_socket.send(pwd)
    result = client_socket.recv(BUFSIZE)
    result = result.decode("utf-8")
    if result == "True":
        print('Login Successfull \n')
    else:
        print('Login Failed \n')
        client_socket.close()

def getClients():
    client_socket.send(choice.encode("utf-8"))
    resp = client_socket.recv(BUFSIZE)
    client_list = json.loads(resp.decode("utf-8"))
    print(f'There are {len(client_list)} users:')
    for client in client_list:
        print(client)
    print(" ")

def getMessage():
    client_socket.send(choice.encode("utf-8"))
    resp = client_socket.recv(BUFSIZE)
    messages = json.loads(resp.decode("utf-8"))
    checker = []
    for lst in messages.values():
        checker += lst
    if len(checker)>0:
        for k,v in messages.items():
            sender = k
            for message in v:
                print("Sender: ", sender)
                print("Message", message)
        print(" ")
    else:
        print("No new messages \n")

def sendMessage():
    code = "3"
    message = []
    receiver = input("Enter username of reciever: ")
    message.append(receiver)
    content = input("Enter the message: ")
    message.append(content)
    package = json.dumps(message).encode("utf-8")
    client_socket.send(code.encode("utf-8"))
    client_socket.send(package)

def startChat():
    priv_ip = input("Enter IP for chat: ")
    priv_port = int(input("Enter PORT for chat: "))
    priv_socket.bind((priv_ip, priv_port))
    priv_socket.listen(1)
    print(f'Waiting to connect at {priv_ip}:{priv_port}')
    user2, address2 = priv_socket.accept()
    print("Connected to: ", address2)
    while True:
        message = input("Type a message or 'bye' to disconnect \n")
        if message == "bye":
            print("ending the connection")
            priv_socket.close()
            break
        else:
            message = message.encode("utf-8")
            user2.send(message)
            print(" ")
            response = user2.recv(BUFSIZE)
            response = response.decode("utf-8")
            if len(response) == 0:
                print("User disconnected")
                break
            else:
                print(response)
                print(" ")
            

def conntectChat():
    priv_ip = input("Enter IP for chat: ")
    priv_port = int(input("Enter PORT for chat: "))
    priv_socket.connect((priv_ip, priv_port))
    print("Connection Established")
    while True:
        response = priv_socket.recv(BUFSIZE)
        response = response.decode("utf-8")
        if len(response)==0:
            print("User has disconnected.")
            break
        else:
            print(response)
            print(" ")
        message = input("Type a message or 'bye' to disconnect \n")
        if message == "bye":
            print("ending the connection")
            priv_socket.close()
            break
        else:
            message = message.encode("utf-8")
            priv_socket.send(message)
            print(" ")
    
while True:
    print("0: Connect to server")
    print("1: Get the user List")
    print("2: Get my messages")
    print("3: Send a message")
    print("4: Initiate a chat")
    print("5: Join a chat")
    choice = input("Enter a choice: ")
    if choice == "0":
        login()
    elif choice == "1":
        getClients()
    elif choice == "2":
        getMessage()
    elif choice == "3":
        sendMessage()
    elif choice == "4":
        startChat()
    elif choice == "5":
        conntectChat()
    else:
        print("Goodbye")
        client_socket.close()
        break