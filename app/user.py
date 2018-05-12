import sys
import os
import requests
import random
import struct
import json

from Crypto.Cipher import AES

passSize = 32

server = "http://localhost:8080"

def fixPass(passwd):
    if(len(passwd)<passSize):
        passwd = passwd+'*'
        size = len(passwd)
        diff = passSize - size
        while(diff < passSize):
            passwd = passwd + '*'
            diff = len(passwd)
    return passwd

def unfixPass(passwd):
    remove = True
    while(remove):
        if(passwd[-1:] == '*'):
            passwd = passwd[:-1]
        else:
            remove = False
    return passwd

def enrol():
    usr = raw_input('Choose your username: ')
    passwd = raw_input('Choose your password: ')
    passwd = fixPass(passwd)
    keys = raw_input('Input all your keys: ')
    f = open("keys.txt", "w+")
    f.write(keys)
    f.close()
    encrypt_file(passwd, "keys.txt")


def login():
    usr = raw_input('Username: ')
    passwd = raw_input('Password: ')
    passwd = fixPass(passwd)
    url = server+"/login"
    data = '''{"user" : "''' + usr + '''", "passw" : "''' + passwd + '''"} '''
    resp = requests.post(url, data=data, headers={'content-type': 'application/json'})
    return "ok"

def saveSecret():
    url = server + "/save"
    resp = requests.post(url, headers={'content-type': 'application/json'})
    return "ok"

def recoverySecret():
    usr = raw_input('Username: ')
    pieces = raw_input('Which friends to retrieve the piece[comma separated: ex: 1, 3, 4]: ')
    tan = raw_input('Authenticator of each friend [comma separated]: ')
    url = server + "/retrieveMySecret"
    data = '''{"user" : "''' + usr + '''", "tan" : "''' + tan + '''", "pieces" : "''' + pieces + '''"} '''
    resp = requests.post(url, data=data, headers={'content-type': 'application/json'})
    cont = resp.content
    dict = json.loads(cont)
    passwd = unfixPass(dict['secret'])
    print ("Secret sucessfully recovered. Your Secret is:")
    print(passwd)
    return "ok"

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

#############################################################################
#############################################################################
######################          Main         ################################
#############################################################################
#############################################################################
def main():
    global server
    options = {
               1: enrol,
               2: login,
               3: saveSecret,
               4: recoverySecret
               }

    mode = -1
    while True:
        print("Choose your option [" + str(server) + "]")
        print("0 - Exit")
        print("1 - Enrol")
        print("2 - Login")
        print("3 - SaveSecret")
        print("4 - RecoverySecret")
        try:
            mode = int(raw_input('Input:'))
        except ValueError:
            print "Not a number"
        if (mode == 0):
            break
        options[mode]()


if __name__ == '__main__':

    if len(sys.argv[1:]) < 0:
        print ("Command Line usage:")
        print ("    python user.py TBD")
        quit()
    os.system("clear")
    main()
