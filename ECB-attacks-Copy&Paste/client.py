from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import *

HOST = 'localhost'
PORT = 12345
PORTTEST = 55555

server = remote(HOST, PORT)
email1 = "aaaaaaa@b.com"
print("email1 = " + email1)
server.send(email1)
c1 = server.recv(1024) #first encrypted cookie: email:...&UID:...&role=user
server.close()

server = remote(HOST, PORT)
email2 = "aaaaaaaaaa" + pad("admin".encode(), AES.block_size).decode() #10 "a" + "email=" composed a block of AES + another block with admin
print("email2 = " + email2)
server.send(email2)
c2 = server.recv(1024)
server.close()

test = remote(HOST, PORTTEST)
c3 = bytearray()
c3 += c1[0:2*AES.block_size]
c3 += c2[AES.block_size:2*AES.block_size]
test.send(c3)
msg = test.recv(1024)
print(msg.decode())
test.close()
