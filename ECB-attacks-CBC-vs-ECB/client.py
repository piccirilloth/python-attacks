import os
os.environ['PWNLIB_NOTERM'] = 'True'  # Configuration patch to allow pwntools to be run inside of an IDE
os.environ['PWNLIB_SILENT'] = 'True'

from pwn import *
from math import ceil
from Crypto.Cipher import AES

HOST = 'localhost'
PORT = 12345

BLOCK_SIZE = AES.block_size
BLOCK_SIZE_HEX = 2*BLOCK_SIZE

server = remote(HOST, PORT)

#pad the initial string (25 bytes) in order to reach the size of 2 blocks (32)
start_str = "This is what I received: "
pad_len = ceil(len(start_str)/AES.block_size)*AES.block_size - len(start_str)
print(pad_len)

msg = b"A"*(2*16+pad_len) #the message to be sent is composed by the pad for the initial string and two blocks
print("sending " + msg.decode('utf-8'))
server.send(msg)

ciphertext = server.recv(1024)
ciphertext_hex = ciphertext.hex()

print(ciphertext_hex[64:96])
print(ciphertext_hex[96:128])

if ciphertext_hex[BLOCK_SIZE_HEX*2:BLOCK_SIZE_HEX*3] == ciphertext_hex[BLOCK_SIZE_HEX*3:BLOCK_SIZE_HEX*4] :
    print("ECB used!")
else :
    print("CBC used!")
