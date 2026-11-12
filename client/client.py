import socket
import threading
import cbor2

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
            message_bytes = message_to_bytes("-TEXT-", {
                "sender": self.name,
                "content": message
            })
            self.socket.send(message_bytes)

    def connect(self):
        self.socket.connect((self.host, self.port))
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

            elif message_type == "-NAME-": # A request from server to get client's name
                message_bytes = message_to_bytes("-NAME-", {"name": name})
                self.socket.send(message_bytes)
                print("Connected.")
                print("Type messages below:")


def message_to_bytes(message_type, values_dict):
    """
    A function which takes the message type and remaining items as parameters
    and returns the encoded equivalent in bytes
    """
    message_dict = {key: value for key,value in values_dict.items()}
    message_dict["message_type"] = message_type
    message_bytes = cbor2.dumps(message_dict)
    return message_bytes
