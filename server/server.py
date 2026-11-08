import socket
import selectors
import cbor2
import server_encryption

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
        self.encryption_cipher = None

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

        # exchanging of keys
        message_bytes = message_to_bytes("-KEY-", {})
        client_socket.send(message_bytes)
        key_bytes = client_socket.recv(1024)
        key_dict = cbor2.loads(key_bytes)
        assert key_dict["message_type"] == "-KEY-"
        client_public_key_string = key_dict["client_public_key_string"]
        client_public_key = server_encryption.string_to_key(client_public_key_string)
        server_private_key, server_public_key, signature = server_encryption.initial_connection(client_public_key)
        message_bytes = message_to_bytes("-SERVER-KEYS-", {
            "server_public_key_string": server_encryption.key_to_string(server_public_key),
            "signature": signature
        })
        client_socket.send(message_bytes)
        encryption_cipher = server_encryption.generate_cipher(server_private_key, client_public_key)
        self.encryption_cipher = encryption_cipher

        # acquiring client name
        message_bytes = message_to_bytes("-NAME-", {})
        client_socket.send(message_bytes)
        name_bytes = client_socket.recv(1024)
        name_dict = cbor2.loads(name_bytes)
        assert name_dict["message_type"] == "-NAME-"
        name = name_dict["name"]
        print("name of the client is " + name)
        self.clients[client_socket] = Client(name)
        self.read_selector.register(client_socket, selectors.EVENT_READ, self.receive_message)
        self.write_selector.register(client_socket, selectors.EVENT_WRITE)
        message_bytes = message_to_bytes("-JOIN-", {
            "user": name
        })
        self.broadcast(client_socket, message_bytes)


    def receive_message(self, client_socket):
        encrypted_message = client_socket.recv(1024)
        message_bytes = server_encryption.decrypt_message(encrypted_message, self.encryption_cipher)
        message_dict = cbor2.loads(message_bytes)
        if message_dict["message_type"] == "-TEXT-":
            self.broadcast(client_socket, message_bytes)
        else:
            print("other message")


    def broadcast(self, client_socket, message_bytes):
        if len(self.clients) > 0:
            for key, _ in self.write_selector.select(0):
                if key.fileobj is not client_socket:
                    key.fileobj.send(message_bytes)
            print("broadcast:", message_bytes)

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
                    message_bytes = message_to_bytes("-DISCONNECT-", {
                        "user": name
                    })
                    self.broadcast(socket, message_bytes)

def message_to_bytes(message_type, values_dict):
    message_dict = {key: value for key,value in values_dict.items()}
    message_dict["message_type"] = message_type
    message_bytes = cbor2.dumps(message_dict)
    return message_bytes

def get_server_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip