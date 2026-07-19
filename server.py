import socket
import threading

# CONSTANTS
homehost = "192.168.1.122"
schoolhost = "10.56.80.136"
localhost = "127.0.0.1"
port = 12345

def connect():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((homehost, port))
    server.listen(1)
    print("Server is listening on port 12345...")

    client, addr = server.accept()
    print(f"Connection from {addr} has been established")

    clients = {}

    return server, client, addr, clients


# OLD
def receive_data(client):
    message_in = client.recv(1024).decode()
    print(f"Received data: {message_in}")
    return message_in

def send_data(client, message_out):
    client.send(message_out.encode())
    print("Response sent to the client.")

def close_connection(server):
    server.close()
    print("Socket closed.")


# NEW

class Client:
    def __init__(self, name):
        self.name = name

def broadcast(clients, message):
    for client in clients.keys():
        client.send(message)

def handle(clients, client):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(clients, message.encode())
        except:
            broadcast(clients, f"{clients[client].name} left the chat".encode())
            clients.pop(client)
            break

def receive(server, clients):
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send("NAME".encode())
        name = client.recv(1024).decode()
        clients[client] = Client(name)
        print(f"Name of the client is {name}.")
        broadcast(clients, f"{name} joined the chat.".encode())
        client.send("Connected to server.".encode())

        thread = threading.Thread(target=handle, args=(clients, client))
        thread.start()


def run_server():
    server, client, addr, clients = connect()
    receive(server, clients)