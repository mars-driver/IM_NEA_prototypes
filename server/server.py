import socket

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

class Client:
    def __init__(self, name):
        self.name = name

def broadcast(message, clients):
    for client in clients.keys():
        client.send(message)

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
    return client, address, name, clients

def run_server(port):
    host = get_server_address()
    server = connect(host, port)
    return host, server
