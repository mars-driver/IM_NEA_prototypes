import cbor2
import chacha20poly1305
import ecdsa
import hashlib
import hmac
import os

# CONSTANTS
CURVE = ecdsa.SECP256k1 # y^2 = x^3 - 7
CONNECTION_SALT='client-server'.encode() # common string to salt key generation

SERVER_PRIVATE_KEY = 'fb6dab05c92e9a8c04e4fe89b680fc1023bb19b5625d84c41427b02aceaf36e5'
SERVER_PRIVATE_KEY = bytes.fromhex(SERVER_PRIVATE_KEY)
SERVER_PRIVATE_KEY = ecdsa.SigningKey.from_string(SERVER_PRIVATE_KEY, curve=CURVE)

def initial_connection(client_public_key):
    server_private_key = ecdsa.SigningKey.generate(CURVE)
    server_public_key = server_private_key.verifying_key.to_string()
    server_private_key = server_private_key.to_string()
    signature = create_signature(client_public_key, server_public_key)
    return server_private_key.hex(), server_public_key.hex(), signature.to_string().hex()


def create_signature(client_public_key, server_public_key):
    both_keys = client_public_key + server_public_key # concatenated
    signature = SERVER_PRIVATE_KEY.sign_deterministic(both_keys)
    print("signature:", signature)
    return signature
