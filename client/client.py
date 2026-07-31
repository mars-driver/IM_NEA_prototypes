import socket
import threading


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _input_and_send_loop(self):
        while True:
            msg = input()  # <- no argument
            self.socket.send(msg.encode("utf8"))

    def connect(self):
        self.socket.connect((self.host, self.port))
        threading.Thread(target=self._input_and_send_loop).start()
        while True:
            msg = self.socket.recv(1024).decode("utf8")
            print(" < " + msg)  # <- added a prefix