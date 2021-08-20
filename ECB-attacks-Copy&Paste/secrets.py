from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

key = get_random_bytes(AES.key_size[0])