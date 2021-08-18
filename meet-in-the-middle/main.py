# We suppose to know the plaintext, the ciphertext and the internal structure of the 2ALG version

from Crypto.Cipher import AES
from Crypto.Random.random import randint
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def shortKeyEnc(key, message, iv):
    cipher = AES.new(key.to_bytes(16, byteorder='big'), iv=iv, mode=AES.MODE_CBC)
    return cipher.encrypt(pad(message, AES.block_size))

def shortKeyDec(key, ciphertext, iv):
    cipher = AES.new(key.to_bytes(16, byteorder='big'), iv=iv, mode=AES.MODE_CBC)
    return cipher.decrypt(ciphertext)

def shortDoubleEnc(key1, key2, message, iv) :
    cipher1 = AES.new(key1.to_bytes(16, byteorder='big'), iv=iv, mode=AES.MODE_CBC)
    cipher2 = AES.new(key2.to_bytes(16, byteorder='big'), iv=iv, mode=AES.MODE_CBC)
    return cipher2.encrypt(cipher1.encrypt(pad(message, AES.block_size)))

if __name__ == '__main__' :
    # we are going tu use key of 1 byte to be faster
    MAX_KEY = 256

    key1 = randint(0, MAX_KEY)
    key2 = randint(0, MAX_KEY)
    iv = get_random_bytes(AES.block_size)
    print("key1 = " + str(key1) + ", key2 = " + str(key2))

    plaintext = b'This is a secret message'
    ciphertext = shortDoubleEnc(key1, key2, plaintext, iv)

    # the attack starts...
    dictionary = dict()

    # compute the intermediate encryption
    for i in range(0, MAX_KEY) :
        dictionary[shortKeyEnc(i, plaintext, iv)] = i

    for i in range(0, MAX_KEY) :
        intermediate_dec = shortKeyDec(i, ciphertext, iv)
        if intermediate_dec in dictionary :
            print("keys found! key1 = " + str(dictionary[intermediate_dec]) + ", key2 = " + str(i))
            break

