import socket
import threading

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
        name = input("Enter your name: ")
        self.name = name
        threading.Thread(target=self.input_and_send_loop).start()
        while True:
            message = self.socket.recv(1024).decode()
            if message == "NAME":
                self.socket.send(name.encode())
                print("Connected.")
            else:
                print(message)
