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
        self.read_selector = selectors.DefaultSelector() # creates a 'bag' to hold sockets
        self.write_selector = selectors.DefaultSelector()

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server is listening on port {self.port}...")
        self.read_selector.register(self.socket, selectors.EVENT_READ, self.accept_connection)

    def accept_connection(self, sock):
        client, address = sock.accept()
        print(f"Connected with {str(address)}")
        print("Registering client...")
        client.send("NAME".encode("utf8"))
        name = client.recv(1024).decode("utf8")
        print("name of the client is " + name)
        self.clients[client] = Client(name)
        self.broadcast(sock, f"{name} joined the chat.".encode("utf8"))
        self.read_selector.register(client, selectors.EVENT_READ, self.receive_message)
        self.write_selector.register(client, selectors.EVENT_WRITE)

    def receive_message(self, sock):
        message = sock.recv(1024)
        print(message.decode("utf8"))
        self.broadcast(sock, message)

    def broadcast(self, sock, message):
        if len(self.clients) > 1:
            for key, _ in self.write_selector.select(0):
                if key.fileobj is not sock:
                    key.fileobj.send(message)
            print("broadcast:", message)

    def run(self):
        self.init_server()
        print("Running server...")
        while True:
            for key, _ in self.read_selector.select():
                sock, callback = key.fileobj, key.data
                callback(sock)


def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip