# Momentum-PoC

How to run the Poc:

1) opem 5 different terminals meaning:
	a) terminal 1: user "interface" where all commands will be send to tenzorum
	b) terminal 2: tenzorum backend running in users computer (Momentun)
	c) terminal 3: your Friend1 also running Momentun (and this guy will receive a piece of your secret)
	d) terminal 4: your Friend2 also running Momentun (and this guy will receive a piece of your secret)
	e) terminal 5: your Friend3 also running Momentun (and this guy will receive a piece of your secret)

2) in terminal 2 run: python Momentun.py 3001
3) in terminal 3 run: python Momentun.py 3002
4) in terminal 4 run: python Momentun.py 3003
5) in terminal 5 run: python Momentun.py 3004
6) in terminal 1 run: python user.py
7) terminal 1:
	a) choose option 1 to login use the password: 1234567890123456
	b) choose option 2 to save the secret using shamir and it will send the  secret among your frinds
	c) choose option 3 to recovery the scret (it doest mater the parameters, just the friends list, must be some like 1,2 or 1,3 or 2,3)
	
