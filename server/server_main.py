import server

# CONSTANTS
homehost = "192.168.1.122"
schoolhost = "10.56.80.136"
localhost = "127.0.0.1"
my_port = 13108
host = server.get_server_address()

# MAIN PROGRAM
cs = server.ChatServer(homehost, my_port)
cs.run()