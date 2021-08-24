from Crypto.Cipher import AES
import os
from pwn import *
import string
from Crypto.Random import get_random_bytes
from secrets import iv, ciphertext

HOST = 'localhost'
PORT = 12345

def num_blocks(ciphertext, block_size) :
    return math.ceil(len(ciphertext) / block_size)

def get_nth_block(ciphertext, n, block_size) :
    return ciphertext[n*block_size:(n+1)*block_size]

def get_b_blocks_from_m(ciphertext, n, m, block_size) :
    return ciphertext[m*block_size:(n+m)*block_size]

def check_oracle_good_padding() :
    server = remote(HOST, PORT)
    server.send(iv)
    server.send(ciphertext)
    response = server.recv(1024)
    server.close()
    print("Oracle said: " + response.decode())

def check_oracle_bad_padding() :
    server = remote(HOST, PORT)
    server.send(iv)
    c2 = bytearray()
    c2 += ciphertext[:-1]
    c2 += bytes([ciphertext[-1] ^ 1])
    server.send(c2)
    response = server.recv(1024)
    server.close()
    print("Oracle said: " + response.decode())

def guess_byte(p, c, ciphertext, block_size) :
    # p and c must have the same length
    padding_value = len(p)+1 #the expected value of the padding
    print("pad = " + str(padding_value))
    n = num_blocks(ciphertext, block_size)
    print("num_blocks = " + str(n))
    current_byte_index = len(ciphertext)-1 - len(p) - block_size
    print("current byte index = " + current_byte_index)

    plain = b'\x00'
    for i in range(256) :
        ca = bytearray()
        ca += ciphertext[:current_byte_index]
        ca += i.to_bytes(1, byteorder='big')

        for x in p :
            ca += (x ^ padding_value).to_bytes(1, byteorder='big')

        ca += get_nth_block(ciphertext, n-1, block_size)

        server = remote(HOST, PORT)
        server.send(iv)
        server.send(ca)
        response = server.recv(1024)

        if response == b'OK' :
            print("found " + str(i))
            p_prime = padding_value ^ i
            plain = bytes([p_prime ^ ciphertext[current_byte_index]])
            if plain == b'\x01':  # this is not sufficient in the general case, only works for the last byte and not always
                continue
            c.insert(0, i)
            p.insert(0, p_prime)
    return plain