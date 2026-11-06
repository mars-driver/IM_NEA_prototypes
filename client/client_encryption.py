import cbor2
import chacha20poly1305
import ecdsa
import hashlib
import hmac
import os

# CONSTANTS
CURVE = ecdsa.SECP256k1 # y^2 = x^3 - 7
CONNECTION_SALT='client-server'.encode() # common string to salt key generation

SERVER_PUBLIC_KEY = '5179b1a64f2e4f839e891654718a94ec0edbce5aada7e904f1c256c4750049d09297d5955dff098af28248ec3aba7fa0deeb00be109bbee954c3313ed34d33cc'
SERVER_PUBLIC_KEY = bytes.fromhex(SERVER_PUBLIC_KEY)
SERVER_PUBLIC_KEY = ecdsa.VerifyingKey.from_string(SERVER_PUBLIC_KEY, curve=CURVE)

def generate_new_keys():
    client_private = ecdsa.SigningKey.generate(CURVE)
    client_public = client_private.verifying_key
    return client_private, client_public

def verify_server(signature, both_keys):
    SERVER_PUBLIC_KEY.verify(signature, both_keys)

def compute_shared_key(client_private_key, server_public_key):
    client_ecdh = ecdsa.ECDH(CURVE, client_private_key, server_public_key)
    client_secret = client_ecdh.generate_sharedsecret_bytes()
    client_key = hmac.new(CONNECTION_SALT, client_secret, hashlib.sha256).digest()
    print(f'Success! Shared secret (hex): {client_secret.hex()}') # added for testing
    print(f'Success! Shared key (hex): {client_key.hex()}') # added for testing
    return client_key

def key_to_string(key):
    return key.to_string()

def string_to_key(key_string):
    return ecdsa.VerifyingKey.from_string(key_string, curve=CURVE)