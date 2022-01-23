import time
import random
import rsa
from utils import expo_rapida as pow_ef
from utils import euclides_gcd as mcd

def rho_pollard(n): # Esta función aplica el algoritmo de rho pollard al número n para sacar un divisor suyo
    # Genearmos una sucesión pseudoaleatoria a partir de (x^2+c) mod n donde x y c son generados aleatoriamente 
    if n == 1:
        return n
    if n%2 == 0:
        return 2
    
    x = random.randint(0,n-1)
    y = x
    c = random.randint(1,n-1)

    gcd = 1

    time_ret = 10 # Para darle una condición de terminación al bucle le damos un tiempo límite de ejecución de 10 segundos
    time_start = time.time()
    time_end = time_start + time_ret
    while (gcd == 1 or gcd == n) and time.time() < time_end:
        # Nos quedamos en el bucle mientras el máximo común divisor encontrado sea o bien 1
        # o bien n (ya que en este caso necesitamos nuevos valores de x y c)

        if gcd == n: # Si gcd = n generamos nuevos valores para x y c
            x = random.randint(0,n-1)
            y = x
            c = random.randint(1,n-1)
        
        x = (pow_ef(x,2,n) + c)%n
        y = (pow_ef((pow_ef(y,2,n) + c)%n,2,n) + c)%n
        gcd = mcd(abs(x-y),n)
        print(x)
        print(y)
        print(gcd)

    if gcd == 1 or gcd == n:
        return
    return gcd


def ataque_rsa(): # Esta función es un ataque mediante el método de rho-pollard
    prueba = rsa.RSA()
    (n,e) = prueba.public_key()
    fact = rho_pollard(n)
    if fact is None:
        print("Ataque fallido. Clave fuerte")
    else: print("Ataque exitoso. Clave débil. Factor: {0}".format(fact))