import socket
import threading
import cbor2
import client_encryption

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encryption_cipher = None
        self.name = None

    def input_and_send_loop(self):
        while True:
            message = input()
            print("> " + message)
            message_bytes = message_to_bytes("-TEXT-", {
                "sender": self.name,
                "content": message
            })
            self.encrypt_and_send(message_bytes)

    def connect(self):
        self.socket.connect((self.host, self.port))
        client_private_key, client_public_key = client_encryption.generate_new_keys()
        name = input("Enter your name: ")
        self.name = name
        threading.Thread(target=self.input_and_send_loop).start()

        while True:
            incoming_message = self.socket.recv(1024)
            if self.encryption_cipher is not None:
                message_bytes = client_encryption.decrypt_message(incoming_message, self.encryption_cipher)
            else:
                message_bytes = incoming_message
            message_dict = cbor2.loads(message_bytes)
            message_type = message_dict["message_type"]

            if message_type == "-KEY-": # A request from server to begin key exchange
                assert self.encryption_cipher is None
                message_bytes = message_to_bytes("-KEY-", {
                    "client_public_key_string": client_encryption.key_to_string(client_public_key)
                })
                self.socket.send(message_bytes)
                server_keys_bytes = self.socket.recv(1024)
                server_keys_dict = cbor2.loads(server_keys_bytes)
                assert server_keys_dict["message_type"] == "-SERVER-KEYS-"
                server_public_key_string = server_keys_dict["server_public_key_string"]
                server_public_key = client_encryption.string_to_key(server_public_key_string)
                signature = server_keys_dict["signature"]
                client_encryption.verify_server(signature, client_public_key, server_public_key)
                encryption_cipher = client_encryption.generate_cipher(client_private_key, server_public_key)
                self.encryption_cipher = encryption_cipher
                continue

            else:
                assert self.encryption_cipher is not None

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

            elif message_type == "-NAME-": # A request from server to get client's name
                message_bytes = message_to_bytes("-NAME-", {"name": name})
                self.encrypt_and_send(message_bytes)
                print("Connected.")
                print("Type messages below:")

    def encrypt_and_send(self, message_bytes):
        """
        Encrypts the given message and sends it across the socket
        """
        encrypted_message = client_encryption.encrypt_message(message_bytes, self.encryption_cipher)
        self.socket.send(encrypted_message)


def message_to_bytes(message_type, values_dict):
    """
    A function which takes the message type and remaining items as parameters
    and returns the encoded equivalent in bytes
    """
    message_dict = {key: value for key,value in values_dict.items()}
    message_dict["message_type"] = message_type
    message_bytes = cbor2.dumps(message_dict)
    return message_bytes