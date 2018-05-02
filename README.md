# Momentum-PoC

How to run the PoC:

Requirements- installation of pip and Flask if not done previously

Open 5 terminals. In this situation, our main user Satoshi has a secret, which has been defined through the Tenzorum UI (represented by Terminal 1) and executed in Momentum (represented by Terminal 2). ‘Pieces’ of Satoshi’s secret are received by 3 friends- Martin, Ralph and Bob- who are each running Momentum (in Terminal 3, 4 and 5 respectively). 

In other words-

a) Terminal 1 will be the user "interface" where all commands from Satoshi are sent to Tenzorum.
b) Terminal 2 will be the Tenzorum backend that runs on Satoshi’s computer (Momentum)
c) Terminal 3 is Martin’s, who is also running Momentum and will receive a piece of Satoshi’s secret.
d) Terminal 4 is Ralph’s, who like Martin is also running Momentum and will receive a piece of Satoshi’s secret.
e) Terminal 5 is Bob’s, again also running Momentum. He will receive a piece of Satoshi’s secret.

Instructions-

1.In terminal 2 run: python Momentum.py 3001
2.In terminal 3 run: python Momentum.py 3002
3.In terminal 4 run: python Momentum.py 3003
4.In terminal 5 run: python Momentum.py 3004
5.In terminal 1 run: python user.py

6.Inside Terminal 1-

	a) choose Option 1. Create your password to ‘login’- this is the ‘secret’ that will be stored.

	b) Choose Option 2. This will save the ‘secret’ using Shamir’s Secret Sharing. ‘Pieces’ of the secret will be encrypted and sent amongst Martin, Ralph and Bob. 

	c) To recover the secret, choose Option 3*. 

You choose any combination of 2 friends out of the 3- this is modular. For a large size n, you can choose k out of n friends. 

After that, you must input the authenticator codes from the 2 chosen friends, placed in parentheses.

This simulates the authentication process in a real-case scenario. After that, your password will be recovered and shown in Terminal 1.

