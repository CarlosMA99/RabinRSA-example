import random


CHOSEN = set()



def expo_rapida(b,e,n=0):
    if e == 0:
        return 1
    if n > 0:    
        b %= n
    res = 1
    while e > 0:
        if e%2 == 1:
            res = (res*b)
            if n > 0:
                res %= n
        b = b*b
        if n > 0:
            b %= n
        e = e // 2
    return res


def euclides_gcd(a,b):
    if a < b:
        a, b = b, a
    if a == 0 or b == 0:
        return a
    rem = a%b
    while rem > 0:
        a,b,rem = b,rem,b%rem
    return b

def euclides_extendido(a,b):
    if a < b:
        a, b = b, a
    if a == 0 or b == 0:
        return a

    aux_a = a
    aux_b = b

    seq1 = [1,0]
    seq2 = [0,1]

    rem = a%b
    while rem > 0:
        q = a//b
        k = len(seq1)
        seq1.append(seq1[k-1]*q+seq1[k-2])
        seq2.append(seq2[k-1]*q+seq2[k-2])
        a,b,rem = b,rem,b%rem
    
    k = len(seq1)
    (p,q) = (seq1[k-1]*(-1)**(k-1),seq2[k-1]*(-1)**k)

    if aux_a*p+aux_b*q < 0:
        p, q = -p, -q
    
    return (p,q,b)


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
    while a in CHOSEN:
        a = random.randint(2,n-2)
    CHOSEN.add(a)
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
    CHOSEN.clear()
    for i in range(k):
        if not miller_rabin(n):
            return False
    return True
