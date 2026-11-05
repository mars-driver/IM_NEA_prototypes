import socket
import threading
import cbor2
# import client_encryption

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
            message_out = f"{self.name}: {message}" #todo rewrite using cbor2
            message_dict = {
                "message_type": "-TEXT-",
                "sender": self.name,
                "content": message
            }
            message_bytes = cbor2.dumps(message_dict)
            self.socket.send(message_bytes)

    def connect(self):
        self.socket.connect((self.host, self.port))
        # send keys here todo
        #client_private_key, client_public_key = client_encryption.generate_new_keys()
        #self.socket.send(client_public_key.encode())
        # todo end
        name = input("Enter your name: ")
        #name = client_public_key
        self.name = name
        threading.Thread(target=self.input_and_send_loop).start()
        while True:
            message = self.socket.recv(1024).decode()
            #if message == "-KEY-":
                #self.socket.send(client_public_key.encode())
                #server_public_key = self.socket.recv(1024).decode()
            if message == "-NAME-":
                self.socket.send(name.encode())
                print("Connected.")
            else:
                print(message)

"""
    def initialise_encryption(self):
        client_public_key = client_encryption.generate_new_keys()
        self.socket.send("-KEYS-".encode())
        self.socket.send(client_public_key.encode())
        server_public_key = self.socket.recv(1024).decode()
"""