import random
from utils.miller_rabin import es_primo_miller_rabin as mr_test
from utils.expo_rapida import expo_rapida as pow_ef
from utils.euclides_extendido import euclides_gcd as euclid_gcd
from utils.euclides_extendido import euclides_extendido as euclid_ext

LDB = 200
UDB = 500

def create_prime():
    digs = random.randint(LDB,UDB)
    impares = [1,3,7,9]
    pot = 10
    num = random.choice(impares)
    for i in range(digs-2):
        num += (random.randint(0,9))*pot
        pot *= 10
    num += (random.randint(1,9))*pot

    while num % 4 == 1 or not mr_test(num):
        digs = random.randint(LDB,UDB)
        pot = 10
        num = random.choice(impares)
        for i in range(digs-2):
            num += (random.randint(0,9))*pot
            pot *= 10
        num += (random.randint(1,9))*pot
    
    return num


    




class RSA:
    def __init__(self):
        self.p1 = create_prime()
        self.p2 = create_prime()
        self.n = self.p1*self.p2
        self.tot = (self.p1-1)*(self.p2-1)
        self.e = random.randint(2,self.tot-1)
        while euclid_gcd(self.e,self.tot) > 1 or self.e == self.p1 or self.e == self.p2:
            self.e = random.randint(2,self.tot-1)
        self.d = euclid_ext(self.e,self.tot)[0]
        self.publica = (self.n,self.e)
        self.privada = (self.d,self.p1,self.p2)



