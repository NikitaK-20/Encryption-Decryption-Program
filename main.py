import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt(plaintext, key):
    backend = default_backend()
    key = key.encode()
    key = os.urandom(32) if len(key) != 32 else key
    cipher = Cipher(algorithms.AES(key), modes.GCM(os.urandom(12)), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext, encryptor.tag

def decrypt(ciphertext, key, tag):
    backend = default_backend()
    key = key.encode()
    key = os.urandom(32) if len(key) != 32 else key
    cipher = Cipher(algorithms.AES(key), modes.GCM(tag, min_tag_length=16), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

#example usage
plaintext = "This is a secret message."
key = "secretkeysecretkey"
ciphertext, tag = encrypt(plaintext, key)
print("Ciphertext:", ciphertext)
decrypted_text = decrypt(ciphertext, key, tag)
print("Decrypted text:", decrypted_text)

