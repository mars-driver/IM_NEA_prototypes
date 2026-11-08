import ecdsa
from hashlib import sha256

KEY = ecdsa.SigningKey.generate(ecdsa.SECP256k1, hashfunc=sha256)
SERVER_PRIVATE_KEY = KEY.to_string().hex() # for server
SERVER_PUBLIC_KEY = KEY.verifying_key.to_string().hex() # for client

# this file is copied to the server directory
with open("server_private_key.txt", "w") as file:
    file.write(SERVER_PRIVATE_KEY)

# this file is copied to the client directory
with open("server_public_key.txt", "w") as file:
    file.write(SERVER_PUBLIC_KEY)