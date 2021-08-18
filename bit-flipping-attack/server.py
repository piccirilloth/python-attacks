import socket
from Crypto.Cipher import AES
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

HOST = ''
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket created

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

s.listen(10)
print("socket is now listening")

while 1:
    conn, addr = s.accept()
    print("Connection from " + addr[0] + ":" + str(addr[1]))

    #receives the username from the client
    username = conn.recv(1024)
    cookie = b'username=' + username + b',admin=0'
    print(cookie)

    key = get_random_bytes(AES.key_size[0])
    cipher = AES.new(key, mode=AES.MODE_CBC)
    conn.send(cipher.encrypt(pad(cookie, AES.block_size)))
    print("cookie sent")

    received_cookie = conn.recv(1024)
    cipher_dec = AES.new(key=key, mode=AES.MODE_CBC, iv=cipher.iv)
    decrypted_cookie = unpad(cipher_dec.decrypt(received_cookie), AES.block_size)

    if b'admin=1' in decrypted_cookie:
        print("you are an administrator!")
        conn.send("you are admin!".encode())
    else:
        i1 = decrypted_cookie.index(b'=')
        i2 = decrypted_cookie.index(b',')
        msg = "welcome" + decrypted_cookie[i1:i2].decode('utf-8')
        print("You are a normal user")
        print(msg)
        conn.send(msg.encode())
    conn.close()

