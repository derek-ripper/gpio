#!/usr/bin/env python
''' 
**********************************************************************
* Filename      : ac3.py
* Purpose       : ACCESS CONTROL -- hide passwords
* Created       : 27 Nov 2020 
* Author        : Derek
**********************************************************************
* 
'''
from cryptography.fernet import Fernet

class Acctl(object):

    
    def __init__(self,option,filepath, filestem):
        self.filelocation = filepath
        self.keyfilename,self.txtfilename = self.bld_filenames(filepath, filestem)
        if option.upper()   == "NEW":
            self.set_encrypykey()
        elif option.upper() == "OLD":
            self.load_encryptkey(self.keyfilename)
        
    def bld_filenames(self, path, stem):
        keyfile = path + stem + "_key.bin"
        txtfile = path + stem + "_txt.bin"
        return keyfile, txtfile
        
    def set_encryptkey(self):
        self.key = Fernet.generate_key()  
        #print("keyfilename:",self.keyfilename)
        self.save_encryptkey(self.keyfilename)
           
    def load_encryptkey(self,myfile):
        with open(myfile, 'rb') as file_object:
            for line in file_object:
                self.key = line
        print("in load_encryptkey:", self.key)
        return self.key     
             
    def save_encryptkey(self,myfile):
        with open(myfile , 'wb') as file_object:  
            file_object.write(self.key)   
            
    def save_encrypttxt(self,myfile,mytxt):    
        with open(myfile , 'wb') as file_object:  
            file_object.write(mytxt) 
        
    def gen_encrypttxt(self,mytext):
        mytxt = mytext.encode('utf-8')

        self.cipher_suite  = Fernet(self.key)
        ciphered_text = self.cipher_suite.encrypt(mytext) 
        return ciphered_text
        
    def get_encrypttxt(self, mytext):   
        unciphered_text = (self.cipher_suite.decrypt(mytext))
        print("get_encrypt tct: ",unciphered_text)
        return unciphered_text
        
    def load_encrypttxt(self,myfile):   
        with open(myfile, 'rb') as file_object:
            for line in file_object:
                ciphered_text = line   
        print("in get_encrypt txt", ciphered_text)
        return  ciphered_text
        
    def test(self):
        self.key     = self.load_encryptkey(self.keyfilename)
        print("self.key: ",self.key)
        encrypttext  = self.load_encrypttxt(self.txtfilename)   
        print("after encrypttxt =", encrypttext)
        self.cipher_suite  = Fernet(self.key)
        uncrypttext = self.get_encrypttxt(encrypttext)
        return uncrypttext
#######################################################################
#crypt = Acctl("/home/pi/dev/gpio/ac/","FirstTest")

#spw = crypt.gen_encrypttxt("My_new_password_qqq777xxxxx")
#print("encrypted   spw : ",spw)

#spw2 = crypt.get_encrypttxt(spw)
#print("spw2 ",spw2)
#crypt.save_encrypttxt(crypt.txtfilename, spw)
#print("unencrypted spw : ",spw2)
########################################################################
########################################################################
crypt = Acctl("old","/home/pi/dev/gpio/ac/","FirstTest")
ans = crypt.test()
print("password: ",ans)
