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
    return client_private.to_string().hex(), client_public.to_string().hex()

generate_new_keys()