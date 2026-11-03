import socket
import threading
import client_encryption

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None

    def input_and_send_loop(self):
        while True:
            message = input()
            print("> " + message)
            message_out = f"{self.name}: {message}"
            self.socket.send(message_out.encode())

    def connect(self):
        self.socket.connect((self.host, self.port))
        # send keys here
        self.socket.send("-KEYS-".encode())
        client_public_key = client_encryption.generate_new_keys()
        self.socket.send(client_public_key.encode())
        name = input("Enter your name: ")
        self.name = name
        threading.Thread(target=self.input_and_send_loop).start()
        while True:
            message = self.socket.recv(1024).decode()
            if message == "-NAME-":
                self.socket.send(name.encode())
                print("Connected.")
            else:
                print(message)

    def initialise_encryption(self):
        client_public_key = client_encryption.generate_new_keys()
        self.socket.send("-KEYS-".encode())
        self.socket.send(client_public_key.encode())
        server_public_key = self.socket.recv(1024).decode()