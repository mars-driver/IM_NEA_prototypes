import socket
import threading

def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def connect(host, port, window):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("Server is listening on port 12345...")
    window.write_event_value("-PRINT-", ("-CONNECT-", "Server is listening on port 12345..."))
    return server

def run_server(port, window):
    host = get_server_address()
    server = connect(host, port, window)
    return host, server

def broadcast(message, clients, window):
    for client in clients.keys():
        client.send(message)
    window.write_event_value("-PRINT-", ("-BROADCAST-", message))


# WIP BEYOND THIS POINT #

class Client:
    def __init__(self, name):
        self.name = name

def new_client(server, clients, window):
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        window.write_event_value("-PRINT-", ("-NEW-CLIENT-", address))
        client.send("NAME".encode())
        name = client.recv(1024).decode()
        window.write_event_value("-PRINT-", ("-NAME-", name))
        clients[client] = Client(name)
        broadcast(f"{name} joined the chat.".encode(), clients, window)
        client.send("Connected to server.".encode())
        receive_thread = threading.Thread(target=receive_message, args=(client, clients, window))
        receive_thread.start()


def receive_message(client, clients, window):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message.encode(), clients, window)
            window.write_event_value(("-THREAD-", "SEND MESSAGE"), message)
        except:
            print("exception")
            window.write_event_value("-PRINT-", ("-RECEIVE-MESSAGE-", "exception"))
            #broadcast(f"{clients[client].name} left the chat".encode(), clients, window)
            #clients.pop(client)



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

