import sys
import os
import requests
import json

server = "http://localhost:3001"

def login():
    usr = raw_input('Username: ')
    passwd = raw_input('Password: ')
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
    tan = raw_input('Authenticator: ')
    pieces = raw_input('Which friends to retrieve the piece[comma separated: ex: 1, 3, 4]: ')
    url = server + "/retrieveMySecret"
    data = '''{"user" : "''' + usr + '''", "tan" : "''' + tan + '''", "pieces" : "''' + pieces + '''"} '''
    resp = requests.post(url, data=data, headers={'content-type': 'application/json'})

    cont = resp.content
    dict = json.loads(cont)
    print ("Secret sucessfully recovered. Your Secret is:")
    print(dict['secret'])
    return "ok"

#############################################################################
#############################################################################
######################          Main         ################################
#############################################################################
#############################################################################
def main():
    global server
    options = {
               1: login,
               2: saveSecret,
               3: recoverySecret
               }

    mode = -1
    while True:
        print("Choose your option [" + str(server) + "]")
        print("0 - Exit")
        print("1 - Login")
        print("2 - SaveSecret")
        print("3 - RecoverySecret")
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
