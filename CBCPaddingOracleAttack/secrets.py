from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = get_random_bytes(AES.key_size[0])
iv = get_random_bytes(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
message = b'this is a secret message'
ciphertext = cipher.encrypt(pad(message, AES.block_size))