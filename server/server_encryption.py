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
    server_public_key = server_private_key.verifying_key
    both_keys, signature = create_signature(client_public_key, server_public_key)
    return server_private_key, server_public_key, both_keys, signature

def create_signature(client_public_key, server_public_key):
    both_keys = client_public_key.to_string() + server_public_key.to_string() # concatenated
    signature = SERVER_PRIVATE_KEY.sign_deterministic(both_keys)
    print("signature:", signature)
    return both_keys, signature

def compute_shared_key(server_private_key, client_public_key):
    server_ecdh = ecdsa.ECDH(CURVE, server_private_key, client_public_key)
    server_secret = server_ecdh.generate_sharedsecret_bytes()
    server_key = hmac.new(CONNECTION_SALT, server_secret, hashlib.sha256).digest()
    print(f'Success! Shared secret (hex): {server_secret.hex()}') # added for testing
    print(f'Success! Shared key (hex): {server_key.hex()}') # added for testing
    return server_key

def key_to_string(key):
    return key.to_string()

def string_to_key(key_string):
    return ecdsa.VerifyingKey.from_string(key_string, curve=CURVE)