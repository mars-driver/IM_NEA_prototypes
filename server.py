import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server_socket.bind((ip, 12345))

server_socket.listen(1)
print("Server is listening on port 12345...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr} has been established")

data = client_socket.recv(1024).decode()
print(f"Recieved data: {data}")

response = "Hello from the server!"
client_socket.send(response.encode())
print("Response sent to the client.")

client_socket.close()
server_socket.close()
print("Server closed.")