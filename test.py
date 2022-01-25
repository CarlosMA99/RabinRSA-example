from rsa import RSA
import ataques

priv = False # esta variable determinará si queremos que la firma sea con privacidad o sin ella. False indica firma sin privacidad
Alice = RSA("Alice") # Creamos a Alice
Bob = RSA("Bob") # Creamos a Bob
m1 = "patata" # mensaje de ejemplo
m2 = "lorem ipsum dolor "*100 # Mensaje grande de ejemplo. Este texto es "lorem ipsum dolor" multiplicado 100 veces

Alice.intercambiar_mensaje(Bob,m1,priv) # Alice le envia a Bob el mensaje m1 y la firma sin privacidad
Bob.intercambiar_mensaje(Alice,m2,priv) # Bob le envia a Alice el mensaje m2 y la firma sin privacidad
priv = True
Alice.intercambiar_mensaje(Bob,m2,priv) # Alice le envia a Bob el mensaje m2 y la firma con privacidad
Bob.intercambiar_mensaje(Alice,m1,priv) # Bob le envia a Alice el mensaje m1 y la firma con privacidad

if ataques.rho_pollard(Alice.public_key()[0]): # Intentamos sacar la clave privada de Alice mediante el algoritmo de rho pollard. Tiene 10 seguundos para responder
    print("La clave de Alice ha sido descubierta")
elif ataques.rho_pollard(Bob.public_key()[0]): # Intentamos sacar la clave privada de Bob mediante el algoritmo de rho pollard. Tiene 10 seguundos para responder
    print("La clave de Bob ha sido descubierta")
else: print("Ninguna clave ha sido descubierta")
