import ecdsa
from hashlib import sha256

KEY = ecdsa.SigningKey.generate(ecdsa.SECP256k1, hashfunc=sha256)
SERVER_PRIVATE_KEY = KEY.to_string().hex() # for server
SERVER_PUBLIC_KEY = KEY.verifying_key.to_string().hex() # for client

print('PRIVATE key:', SERVER_PRIVATE_KEY)
print('PUBLIC key:', SERVER_PUBLIC_KEY)