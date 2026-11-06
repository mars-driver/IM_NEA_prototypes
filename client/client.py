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
            message_bytes = self.socket.recv(1024)
            message_dict = cbor2.loads(message_bytes)
            message_type = message_dict["message_type"]
            if message_type == "-TEXT-":
                sender = message_dict["sender"]
                content = message_dict["content"]
                message = f"{sender}: {content}"
                print(message)
            elif message_type == "-JOIN-":
                user = message_dict["user"]
                message = f"{user} joined the chat."
                print(message)
            elif message_type == "-DISCONNECT-":
                user = message_dict["user"]
                message = f"{user} has left the chat."
                print(message)
            #if message == "-KEY-":
                #self.socket.send(client_public_key.encode())
                #server_public_key = self.socket.recv(1024).decode()
            elif message_type == "-NAME-":
                message_dict = {
                    "message_type": "-NAME-",
                    "name": name
                }
                message_bytes = cbor2.dumps(message_dict)
                self.socket.send(message_bytes)
                print("Connected.")

"""
    def initialise_encryption(self):
        client_public_key = client_encryption.generate_new_keys()
        self.socket.send("-KEYS-".encode())
        self.socket.send(client_public_key.encode())
        server_public_key = self.socket.recv(1024).decode()
"""