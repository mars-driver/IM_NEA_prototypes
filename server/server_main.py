import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print(f'Hostname: {hostname}')
print(f'IP: {ip}')

import server

#server_socket, client_socket, addr = server.connect()
#gui.proto_GUI_server(server_socket, client_socket, addr)

server.run_server()