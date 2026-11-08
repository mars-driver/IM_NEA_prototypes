import chacha20poly1305
import ecdsa
from hashlib import sha256
import hmac
import os

# CONSTANTS
CURVE = ecdsa.SECP256k1 # y^2 = x^3 - 7
CONNECTION_SALT='client-server'.encode() # common string to salt key generation

with open("server_public_key.txt") as file:
    SERVER_PUBLIC_KEY = file.readline()

SERVER_PUBLIC_KEY = bytes.fromhex(SERVER_PUBLIC_KEY)
SERVER_PUBLIC_KEY = ecdsa.VerifyingKey.from_string(SERVER_PUBLIC_KEY, curve=CURVE)

def generate_new_keys():
    client_private = ecdsa.SigningKey.generate(CURVE)
    client_public = client_private.verifying_key
    return client_private, client_public

def verify_server(signature, server_public_key, client_public_key):
    both_keys = key_to_string(client_public_key) + key_to_string(server_public_key)  # concatenated
    SERVER_PUBLIC_KEY.verify(signature, both_keys)

def compute_shared_key(client_private_key, server_public_key):
    client_ecdh = ecdsa.ECDH(CURVE, client_private_key, server_public_key)
    client_secret = client_ecdh.generate_sharedsecret_bytes()
    client_key = hmac.new(CONNECTION_SALT, client_secret, sha256).digest()
    return client_key

def generate_cipher(client_private_key, server_public_key):
    encryption_key = compute_shared_key(client_private_key, server_public_key)
    encryption_cipher = chacha20poly1305.ChaCha20Poly1305(encryption_key)
    return encryption_cipher

def encrypt_message(message_bytes, encryption_cipher):
    n_once = os.urandom(12)  # always different random for each message sent
    encrypted_message = encryption_cipher.encrypt(n_once, message_bytes)
    encrypted_message = n_once + encrypted_message
    return encrypted_message

def key_to_string(key):
    return key.to_string()

def string_to_key(key_string):
    return ecdsa.VerifyingKey.from_string(key_string, curve=CURVE)