from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
import getpass
from easygui import passwordbox

#key=os.urandom(16)
key = b'Q\xc0\xe5;\x97\xfe\xd9\xd7\x86\xd8\xf9Z\xb8\xa8\xba\xf7'

def encrypt_file(file_name):
    with open (file_name, 'r') as fo:
        plaintext = fo.read()
        #convert to bytes
        s = plaintext.encode("latin-1")
        fo.close()
        os.remove(file_name)

        #padding
        message=s+ b"\0" * (AES.block_size - len(s) % AES.block_size)
        #ensure same plaintext into different cipher text
        iv= Random.new().read(AES.block_size)
        #cipher object is made
        cipher = AES.new(key, AES.MODE_CBC, iv)
        #message is encrypted and iv is added
        ciphertext = iv + cipher.encrypt(message)
        
        with open (file_name, 'wb+') as fo:
            fo.write(ciphertext)
            fo.close()



def decrypt_file(filename):
    with open (filename, 'rb') as fo:
            ciphertext = fo.read()
            fo.close()
            os.remove(filename)

            #iv is extracted
            iv=ciphertext[:AES.block_size]
            #cipher object is made
            cipher = AES.new(key, AES.MODE_CBC, iv)
            #plaintext is decrypted
            plaintext = cipher.decrypt(ciphertext[AES.block_size:])
            #message is extracted
            plaintext=plaintext.rstrip(b"\0")
            
            with open (filename, 'wb+') as fo:
                    fo.write(plaintext)

            

if os.path.isfile('data.txt'):
    while True:
        password = passwordbox("Enter Password:")
        decrypt_file("data.txt")
        p = ""
        with open ("data.txt","r") as f:
            p = f.readlines()
        if p[0] == password:
            encrypt_file("data.txt")
            break
        else:
            encrypt_file("data.txt")

    while True:
        
        try:
            choice = int(input(
                        '''
                            1. Encrypt file.\n
                            2. Decrypt file.\n
                            3. Exit\n\n
                            Enter your choice: '''
                            ))
            
            if choice==1:
                encrypt_file(str(input("Enter file name to encrypt: ")))
                print("Encrypted .  .  .  ")

            elif choice==2:
                decrypt_file(str(input("Enter file name to decrypt: ")))
                print("Dencrypted .  .  .  ")

            elif choice==3:
                exit()

            else:
                print("Please select a valid option!")

        except:
            print("Value Error!!")
        


else:
    while True:
        
        password = str(input("\nSetting up a few stuff. . .\n\nEnter password: "))
        repassword = str(input("Confirm password: "))
        if password == repassword:
            f = open ("data.txt","w+")
            f.write(password)
            f.close()
            encrypt_file("data.txt")
            print("\nPlease restart the program to complete the setup")
            break
        else:
            print("\nPassword Mismatched!")

        
        
