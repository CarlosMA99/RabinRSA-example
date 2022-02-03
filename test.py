from rsa import RSA
import ataques

priv = False
Alice = RSA("Alice")
Bob = RSA("Bob")
m1 = "patata"
m2 = "lorem ipsum dolor "*100

Alice.intercambiar_mensaje(Bob,m1,priv)
Bob.intercambiar_mensaje(Alice,m2,priv)
Alice.intercambiar_mensaje(Bob,m2)
Bob.intercambiar_mensaje(Alice,m1)

if ataques.rho_pollard(Alice.public_key()[0]) is not None:
    print("Alice's key has been compromised")
elif ataques.rho_pollard(Bob.public_key()[0]) is not None:
    print("Bob's private key has been compromised")
else: print("Neither private key has been compromised")
