#!/usr/bin/env python
''' i
**********************************************************************
* Filename      : crypt1.py
* Purpose       : ACCESS CONTROL -- hide passwords
* Created       : 27 Nov 2020 
* Author        : Derek
**********************************************************************
* 
'''
# GENERATE Encrytion Key

#from cryptography.fernet import Fernet
#key = Fernet.generate_key()
#print(key)
# from above
key = b'C6lt1UGrk9vp_EJfXQCOuvZ2RDBc3VvAtYYNHPYW-YQ='

#from cryptography.fernet import Fernet
#cipher_suite = Fernet(key)
#ciphered_text = cipher_suite.encrypt(b"Super_Secret_Password")   #required to be bytes
#print(ciphered_text) 
#from above
ciphered_text = b'gAAAAABfv9FeaUmTn29V-iu8bW4dttolxNX2X3Yd_Ocudb6vj2btIVHqxw1woCrcW4EytRXVTBQJuNqSp2gH73o00Ny_-x8FNQISncyd8nZoSE6y-4Fv5qs='

from cryptography.fernet import Fernet
cipher_suite = Fernet(key)

unciphered_text = (cipher_suite.decrypt(ciphered_text))
print("before file write",unciphered_text)

#write to binary file
### from cryptography.fernet import Fernet
### key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b"Super_Secret_Password")   #required to be bytes

print("Write to file .....")
myfile = '/home/pi/dev/crpyt_pw_bytes.bin'

with open(myfile , 'wb') as file_object:  
    file_object.write(ciphered_text)

with open(myfile, 'rb') as file_object:
    for line in file_object:
        encryptedpwd = line
print("encrypted passord:\n",encryptedpwd)
