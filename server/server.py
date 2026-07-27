import socket
import threading

# overriding the Thread class to return values
class CustomThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, verbose=None):
        # Initializing the Thread class
        super().__init__(group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        super().join(timeout)
        return self._return


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
        print(client) #todo
        print(clients.keys()) #todo
        client.send(message)

def handle(client, clients):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message.encode(), clients)
            print("broken") #todo
        except:
            broadcast(f"{clients[client].name} left the chat".encode(), clients)
            clients.pop(client)
            return f"{clients[client].name} left the chat", clients

def receive(server, clients):
    client, address = server.accept()
    print("broken") #todo
    print(client) #todo
    print(f"Connected with {str(address)}")
    client.send("NAME".encode())
    name = client.recv(1024).decode()
    clients[client] = Client(name)
    print(f"Name of the client is {name}.")
    broadcast(f"{name} joined the chat.".encode(), clients)
    client.send("Connected to server.".encode())
    print("last message before i try returning valuessss")
    thread = CustomThread(target=handle, args=(client, clients))
    thread.start()
    return_values = thread.join()
    print("time to return the values")
    print("RETURN VALUES:", return_values)
    return client, address, name, clients, return_values

def run_server(port):
    host = get_server_address()
    server = connect(host, port)
    receive(server, {})
    return server
