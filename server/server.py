import socket
import threading

def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def connect(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("Server is listening on port 12345...")
    return server

def run_server(port):
    host = get_server_address()
    server = connect(host, port)
    clients = {}
    newclient_thread = threading.Thread(target=new_client, args=(server, clients))
    newclient_thread.start()
    return host, server

def broadcast(message, clients):
    for client in clients.keys():
        client.send(message)
    print("broadcast:", message)

# WIP BEYOND THIS POINT #

class Client:
    def __init__(self, name):
        self.name = name

def new_client(server, clients):
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send("NAME".encode())
        name = client.recv(1024).decode()
        clients[client] = Client(name)
        broadcast(f"{name} joined the chat.".encode(), clients)
        client.send("Connected to server.".encode())
        receive_thread = threading.Thread(target=receive_message, args=(client, clients))
        receive_thread.start()


def receive_message(client, clients):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message.encode(), clients)
            print("send message:", message)
        except:
            print("exception")
            broadcast(f"{clients[client].name} left the chat".encode(), clients)
            clients.pop(client)
            print("client popped")


"""
def receive(server, clients, start_handle_thread, window):
    client, address = server.accept() # this waits until a client connects
    print(f"Connected with {str(address)}")
    client.send("NAME".encode())
    name = client.recv(1024).decode()
    clients[client] = Client(name)
    print(f"Name of the client is {name}.")
    broadcast(f"{name} joined the chat.".encode(), clients)
    client.send("Connected to server.".encode())
    start_handle_thread(client, clients, window) # threading!
"""

