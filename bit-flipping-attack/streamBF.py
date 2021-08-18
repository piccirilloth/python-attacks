from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

message = b'This is a message and I want to flip this number 12345'
print(message.decode('utf-8'))

key = get_random_bytes(ChaCha20.key_size)

cipher = ChaCha20.new(key=key)

ciphertext = cipher.encrypt(message)

index = message.index(b'1') #find the position of the byte to flip
ciphertext_array = bytearray(ciphertext)

new_byte = b'2'
print(ord(new_byte))
print(message[index])
print(ciphertext_array[index])

ciphertext_array[index] = ciphertext_array[index] ^ message[index] ^ ord(new_byte) #keystream[index] ^ ord(new_byte)

cipher_dec = ChaCha20.new(key=key, nonce=cipher.nonce)
print(cipher_dec.decrypt(ciphertext_array).decode('utf-8'))

new_byte = b'5'
index = message.index(b'4')
ciphertext_array[index] = ciphertext_array[index] ^ message[index] ^ ord(new_byte)
cipher_dec = ChaCha20.new(key=key, nonce=cipher.nonce)
print(cipher_dec.decrypt(ciphertext_array).decode('utf-8'))
