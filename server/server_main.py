import server

# CONSTANTS
homehost = "192.168.1.122"
schoolhost = "10.56.81.120"
localhost = "127.0.0.1"
grannyhost = "192.168.1.138"
my_port = 13108
host = server.get_server_address()

# MAIN PROGRAM
server = server.ChatServer(schoolhost, my_port)
server.run()