from Crypto.Cipher import AES
from pwn import *
import string

HOST = 'localhost'
PORT = 12345

SECRET_LEN = 16 #we know that the secret has length = 16

secret = ""

#the initial message is 16 byte long, than there is our message, that 15 bytes after the secret and then 16 byte of secret
fix = " - and the sec:" #we insert a message equals to the message before the secret and this mesage has len = 15 bytes

# | start message |  - and the sec:A | padding |  - and the sec:S | SSSSSSSSSSSSSSSP |

for i in range(0, SECRET_LEN) :
    pad = "A" * (AES.block_size - i)
    for j in string.printable :
        server = remote(HOST, PORT)
        msg = fix + secret + j + pad
        print("sending " + msg)
        server.send(msg)
        ciphertext = server.recv(1024)
        server.close()
        if ciphertext[16:32] == ciphertext[48:64] :
            print("Found new character = " + j)
            secret += j
            fix = fix[1:]
            break

print("the secret is " + secret)