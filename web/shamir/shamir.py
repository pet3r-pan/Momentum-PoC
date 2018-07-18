import sharing
import sys

sec = "asdf"
totalPieces = 6
minRecover = 2

try:
    sec = raw_input('Tell me a secret: ')
    totalPieces = int(raw_input('How many pieces should I slice your secret?'))
    minRecover = int(raw_input('Which is the minimum amount of pieces to recover you secret?'))
except ValueError:
    print "Something went wrong"



res = sharing.PlaintextToHexSecretSharer.split_secret(sec, minRecover, totalPieces)
print res

try:
    pieces = raw_input('Which pieces should I use to recover [ comma separated: ex: 1, 3, 4]? ')
except ValueError:
    print "Something went wrong"

pieceVet = pieces.split(',')
pieceVet = map(int, pieceVet)

recovVet = []
for i in range(1,totalPieces):
    if i in pieceVet:
        print(res[i])
        recovVet.append(res[i])


ret = sharing.PlaintextToHexSecretSharer.recover_secret(recovVet)
print ret

#sudo pip install utilitybelt
