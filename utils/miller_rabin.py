import random
import sys
sys.path.insert(0,"/Users/carlosmoran/Desktop/Práctica\ final\ CTC/utils")
from expo_rapida import expo_rapida

def descomponer_en_impar(prim):
    i = 0
    while prim%2 == 0:
        i += 1
        prim = prim // 2
    return (i,prim)


def miller_rabin(n):
    if n == 2 or n == 3:
        return True
    if n == 1 or n%2 == 0:
        return False

    a = random.randint(2,n-2)
    (pot,num) = descomponer_en_impar(n-1)

    res = expo_rapida(a,num,n)
    if res == 1 or res == n-1:
        return True
    
    for i in range(pot-1):
        res = (res*res)%n
        if res == 1:
            return False
        if res == n-1:
            return True
    return False


def es_primo_miller_rabin(n,k=10):
    for i in range(k):
        if not miller_rabin(n):
            return False
    return True