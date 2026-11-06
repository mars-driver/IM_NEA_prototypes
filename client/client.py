import socket
import threading
import cbor2
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
            message_dict = {
                "message_type": "-TEXT-",
                "sender": self.name,
                "content": message
            }
            message_bytes = cbor2.dumps(message_dict)
            self.socket.send(message_bytes)

    def connect(self):
        self.socket.connect((self.host, self.port))
        client_private_key, client_public_key = client_encryption.generate_new_keys()
        name = input("Enter your name: ")
        self.name = name
        threading.Thread(target=self.input_and_send_loop).start()

        while True:
            message_bytes = self.socket.recv(1024)
            message_dict = cbor2.loads(message_bytes)
            message_type = message_dict["message_type"]

            if message_type == "-TEXT-": # A message sent from a user to a chat room
                sender = message_dict["sender"]
                content = message_dict["content"]
                message = f"{sender}: {content}"
                print(message)

            elif message_type == "-JOIN-": # A message sent by the server when a user joins the chat room
                user = message_dict["user"]
                message = f"{user} joined the chat."
                print(message)

            elif message_type == "-DISCONNECT-": # A message sent by the server when a user leaves the chat room
                user = message_dict["user"]
                message = f"{user} has left the chat."
                print(message)

            elif message_type == "-KEY-": # A request from server to begin key exchange
                message_dict = {
                    "message_type": "-KEY-",
                    "client_public_key_string": client_encryption.key_to_string(client_public_key)
                }
                message_bytes = cbor2.dumps(message_dict)
                self.socket.send(message_bytes)
                server_keys_bytes = self.socket.recv(1024)
                server_keys_dict = cbor2.loads(server_keys_bytes)
                assert server_keys_dict["message_type"] == "-SERVER-KEYS-"
                server_public_key_string = server_keys_dict["server_public_key_string"]
                server_public_key = client_encryption.string_to_key(server_public_key_string)
                both_keys = server_keys_dict["both_keys"]
                signature = server_keys_dict["signature"]
                client_encryption.verify_server(signature, both_keys)
                shared_key = client_encryption.compute_shared_key(client_private_key, server_public_key) #todo share this
                print("shared key computed") # added for testing

            elif message_type == "-NAME-": # A request from server to get client's name
                message_dict = {
                    "message_type": "-NAME-",
                    "name": name
                }
                message_bytes = cbor2.dumps(message_dict)
                self.socket.send(message_bytes)
                print("Connected.")
