import os
import sys
import random, struct
import json

import requests
from Crypto.Cipher import AES
from shamir.sharing import PlaintextToHexSecretSharer

from flask import Flask, request

app = Flask(__name__)

passwd = ""
friendSecret = ""
friendTan = str(random.randint(1000, 9000))

friend1Addr = "http://localhost:3002/"
friend2Addr = "http://localhost:3003/"
friend3Addr = "http://localhost:3004/"

@app.route('/login', methods=['POST'])
def login():
    print ("running login")
    global passwd
    content = request.get_json()
    user = content['user']
    passwd = content['passw']
    print("user:"+user+" pass:"+passwd)
    #encrypt_file("1234567890123456", "keys.txt")
    decrypt_file(passwd, "keys.txt.enc", "keys.txt")
    f = open("keys.txt","r")
    print f.read()
    return "ok"


@app.route('/save', methods=['POST'])
def doShammir():
    print passwd
    res = PlaintextToHexSecretSharer.split_secret(passwd, 2, 3)
    print res
    sendShamirPieces(res)
    return "ok"


@app.route('/setSecret', methods=['POST'])
def setSecret():
    content = request.get_json()
    global friendSecret
    global friendTan
    #friendTan = str(random.randint(1000, 9000))
    friendSecret = content['secret']
    print "received "+friendSecret
    print "My Authenticator code is:"+friendTan
    return "ok"''


@app.route('/getSecret', methods=['POST'])
def getSecret():
    content = request.get_json()
    global friendSecret
    global friendTan
    tan = content['tan']
    usr = content['user']
    print ("the user: "+usr+" is requesting his secret")
    if(tan == friendTan):
        # request.data['secret'] = friendSecret
        #return friendSecret
        strRet = '''{"secret" : "''' + friendSecret + '''"} '''
        return strRet
    else:
        print (tan)
        print (friendTan)
        print("Invalid Authenticator!!!!")
        return ''


@app.route('/retrieveMySecret', methods=['POST'])
def retrieveMySecret():
    content = request.get_json()
    global friendSecret
    tan = content['tan']
    tanVet = tan.split(',')
    usr = content['user']
    pieces = content['pieces']
    pieceVet = pieces.split(',')
    pieceVet = map(int, pieceVet)
    secretReceived = []
    try:
        for i in range(0, len(pieceVet)):
            secretReceived.append(getShamirPiece(tanVet[i].strip(), usr, pieceVet[i]).encode('utf8'))

        plainSecret = PlaintextToHexSecretSharer.recover_secret(secretReceived)
        strRet = '''{"secret" : "''' + plainSecret + '''"} '''
        return strRet
    except:
        return '''{"secret" : "Impossible  to retrieve"} '''


@app.route('/getAuthenticator', methods=['GET'])
def getAuthenticator():
    global friendTan
    print "Sending the authenticator code to UI: "+friendTan
    return friendTan
    

def getShamirPiece(tan, usr, friendId):
    friendId = friendId + 1
    url = "http://localhost:300" + str(friendId) + "/getSecret"
    data = '''{"user" : "''' + usr + '''", "tan" : "'''+tan+'''"} '''
    resp = requests.post(url, data=data, headers={'content-type':'application/json'})
    try:
        cont = resp.content
        dict = json.loads(cont)
        if (dict['secret']):
            return dict['secret']
        else:
            return ''
    except:
        return "failed"


def sendShamirPieces(pieceArray):
    url1 = friend1Addr + "setSecret"
    data1 = '''{"secret":"'''+pieceArray[0]+'''"}'''
    resp = requests.post(url1, data=data1, headers={'content-type':'application/json'})
    url2 = friend2Addr + "setSecret"
    data2 = '''{"secret":"'''+pieceArray[1]+'''"}'''
    resp = requests.post(url2, data=data2, headers={'content-type':'application/json'})
    url3 = friend3Addr + "setSecret"
    data3 = '''{"secret":"'''+pieceArray[2]+'''"}'''
    resp = requests.post(url3, data=data3, headers={'content-type':'application/json'})



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


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def main():
    p = sys.argv[1]
    startServer(int(p))


def startServer(porta=3001):
        app.run(host='0.0.0.0', port=porta, debug=True)


if __name__ == '__main__':
    if len(sys.argv[1:]) < 1:
        print ("Command Line usage:")
        print ("    python Momentun.py port")
        quit()
    os.system("clear")
    main()
