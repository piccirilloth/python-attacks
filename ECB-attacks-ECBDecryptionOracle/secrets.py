from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

key = get_random_bytes(AES.key_size[0])
secret = "1111111111111111" #16 chars -> 1 AES block for an easier computation