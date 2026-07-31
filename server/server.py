import socket
import selectors

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.read_selector = selectors.DefaultSelector() # creates a 'bag' to hold sockets
        self.write_selector = selectors.DefaultSelector()

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server is listening on port {self.port}...")
        self.read_selector.register(self.socket, selectors.EVENT_READ, self.accept_connection)

    def accept_connection(self, sock):
        client, _ = sock.accept()
        print("Registering client...")
        self.read_selector.register(client, selectors.EVENT_READ, self.receive_message)
        self.write_selector.register(client, selectors.EVENT_WRITE)

    def receive_message(self, sock):
        msg = sock.recv(1024)
        print(msg.decode("utf8"))
        for key, _ in self.write_selector.select(0):
            if key.fileobj is not sock:
                key.fileobj.send(msg)



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