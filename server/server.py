import socket
import selectors

class Client:
    def __init__(self, name):
        self.name = name

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self.read_selector = selectors.DefaultSelector()
        self.write_selector = selectors.DefaultSelector()

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server is listening on port {self.port}...")
        self.read_selector.register(self.socket, selectors.EVENT_READ, self.accept_connection)

    def accept_connection(self, server_socket):
        client_socket, address = server_socket.accept()
        print(f"Connected with {str(address)}")
        print("Registering client...")
        name = client_socket.recv(1024).decode()
        print("name of the client is " + name)
        self.clients[client_socket] = Client(name)
        self.read_selector.register(client_socket, selectors.EVENT_READ, self.receive_message)
        self.write_selector.register(client_socket, selectors.EVENT_WRITE)
        self.broadcast(client_socket, f"{name} joined the chat.".encode())


    def receive_message(self, client_socket):
        message = client_socket.recv(1024)
        print(message.decode())
        self.broadcast(client_socket, message)

    def broadcast(self, client_socket, message):
        if len(self.clients) > 0:
            for key, _ in self.write_selector.select(0):
                if key.fileobj is not client_socket:
                    key.fileobj.send(message)
            print("broadcast:", message)

    def run(self):
        self.init_server()
        print("Running server...")
        while True:
            for key, _ in self.read_selector.select():
                socket, callback = key.fileobj, key.data
                try:
                    callback(socket)
                except:
                    name = self.clients[socket].name
                    print("socket error", name)
                    self.read_selector.unregister(socket)
                    self.write_selector.unregister(socket)
                    self.clients.pop(socket)
                    socket.close()
                    self.broadcast(socket, f"{name} has left.".encode())



def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip