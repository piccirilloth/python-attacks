from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import *

ADDRESS = "localhost"
PORT = 12345

q = remote(ADDRESS, PORT)
q.send(b'oscar')
ciphertext = q.recv(1024)

old_block = pad(b'admin=0', AES.block_size)
print(old_block)
new_block = pad(b'admin=1', AES.block_size)
print(new_block)
delta = bytes(a ^ b for (a, b) in zip(old_block, new_block))
print(delta)

print(len(ciphertext))
ciphertext_array = bytearray(ciphertext)
for i in range(0,16):
    ciphertext_array[i] ^= delta[i]

q.send(ciphertext_array)
print("cookie sent " + str(ciphertext_array))
y = q.recv(1024).decode('utf-8')
print(y)
q.close()

#l'attacco nel caso di CBC è basato sul fatto che in fase di decrypt, l'ultimo blocco verrà decryptato ed in seguito verrà effettuata un operazione di XOR con
#il ciphertext del blocco precedente, dunque per "agire" sull'ultimo blocco è necessario modificare i bit del penultimo blocco
