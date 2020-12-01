#!/usr/bin/env python3
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
        self.option = option.upper()
        if   self.option == "NEW":
            self.key = self.set_encryptkey()
        elif self.option == "OLD":
            self.key = self.load_encryptkey(self.keyfilename)
        
        self.cipher_suite  = Fernet(self.key)    
        
    def bld_filenames(self, path, stem):
        keyfile = path + stem + "_key.bin"
        txtfile = path + stem + "_txt.bin"
        return keyfile, txtfile
        
    def set_encryptkey(self):
        key = Fernet.generate_key()  
        self.save_encryptkey(key, self.keyfilename)
        return key
          
    def load_encryptkey(self,myfile):
        with open(myfile, 'rb') as file_object:
            for line in file_object:
                key = line

        return key     
             
    def save_encryptkey(self,encrypykey, myfile):
        with open(myfile , 'wb') as file_object:  
            file_object.write(encrypykey)   
            
    def save_encrypttxt(self,encrypttxt,myfile):    
        with open(myfile , 'wb') as file_object:  
            file_object.write(encrypttxt) 
        
    def en_crypttxt(self,mytext):
        mytext = bytes(mytext,'utf-8')
        ciphered_text = self.cipher_suite.encrypt(mytext) 
        return ciphered_text
        
    def de_crypttxt(self, mytext):   
        cipher_suite  = Fernet(self.key)
        unciphered_text = (self.cipher_suite.decrypt(mytext))
        return unciphered_text
        
    def read_txt2encrypt(self):
        print("########################################")
        txt = input("Enter text to encrypt here: ")
        print("Text: ", txt)
        cipherred_text = self.en_crypttxt(txt)
        self.save_encrypttxt(cipherred_text,self.txtfilename)
        
        return cipherred_text
        
    def load_encrypttxt(self,myfile): 
        if self.option == "NEW":
           ciphered_text = self.read_txt2encrypt()
        else:
            with open(myfile, 'rb') as file_object:
                for line in file_object:
                    ciphered_text = line  
                    
        return  ciphered_text
        
    def test(self):
        self.key     = self.load_encryptkey(self.keyfilename)
        print("self.key   = "+str(self.key)+"\n")

        encrypttext  = self.load_encrypttxt(self.txtfilename)   
        print("encrypttxt = "+str(encrypttext)+"\n")
    
        uncrypttext = self.de_crypttxt(encrypttext)
        return uncrypttext
#######################################################################
#######################################################################
if __name__ == "__main__":
    crypt = Acctl("old","/home/pi/dev/gpio/ac/","FourthTest")
    ans   = crypt.test()
    print("From File: "+crypt.txtfilename+"\nUnencrypted text is: "+str(ans))
