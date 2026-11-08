from chacha20poly1305 import ChaCha20Poly1305
import ecdsa
from hashlib import sha256
import hmac

# CONSTANTS
CURVE = ecdsa.SECP256k1 # y^2 = x^3 - 7
CONNECTION_SALT='client-server'.encode() # common string to salt key generation

with open("server_private_key.txt") as file:
    SERVER_PRIVATE_KEY = file.readline()

SERVER_PRIVATE_KEY = bytes.fromhex(SERVER_PRIVATE_KEY)
SERVER_PRIVATE_KEY = ecdsa.SigningKey.from_string(SERVER_PRIVATE_KEY, curve=CURVE)

def initial_connection(client_public_key):
    """
    A function to generate a new pair of encryption keys and a signature for this session
    """
    server_private_key = ecdsa.SigningKey.generate(CURVE)
    server_public_key = server_private_key.verifying_key
    signature = create_signature(client_public_key, server_public_key)
    return server_private_key, server_public_key, signature

def create_signature(client_public_key, server_public_key):
    """
    A function which uses the client and server's public keys to create a signature
    """
    both_keys = key_to_string(client_public_key) + key_to_string(server_public_key) # concatenated
    signature = SERVER_PRIVATE_KEY.sign_deterministic(both_keys)
    return signature

def compute_shared_key(server_private_key, client_public_key):
    """
     A function which computes the shared key (should be identical to the client key)
    """
    server_ecdh = ecdsa.ECDH(CURVE, server_private_key, client_public_key)
    server_secret = server_ecdh.generate_sharedsecret_bytes()
    server_key = hmac.new(CONNECTION_SALT, server_secret, sha256).digest()
    return server_key

def generate_cipher(server_private_key, client_public_key):
    """
    A function which uses the shared key to calculate the encryption cipher (identical to client cipher)
    """
    encryption_key = compute_shared_key(server_private_key, client_public_key)
    encryption_cipher = ChaCha20Poly1305(encryption_key)
    return encryption_cipher

def decrypt_message(encrypted_message, encryption_cipher):
    """
    A function to decrypt messages using the encryption cipher
    """
    n_once = encrypted_message[:12]
    message = encrypted_message[12:]
    message_bytes = encryption_cipher.decrypt(n_once, message)
    print("message decrypted")
    print(message_bytes)
    return message_bytes

def key_to_string(key):
    """
    A function to convert a VerifyingKey object to a string
    """
    return key.to_string()

def string_to_key(key_string):
    """
    A function to convert a string into a VerifyingKey object
    """
    return ecdsa.VerifyingKey.from_string(key_string, curve=CURVE)