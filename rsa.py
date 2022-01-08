import random
from utils.miller_rabin import es_primo_miller_rabin as mr_test
from utils.expo_rapida import expo_rapida as pow_ef
from utils.euclides_extendido import euclides_gcd as euclid_gcd
from utils.euclides_extendido import euclides_extendido as euclid_ext

LDB = 300
UDB = 500
CARD = 127

def create_prime(digs):
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
    def __init__(self,id):
        self.id = id
        digs1 = random.randint(LDB,UDB)
        self.p1 = create_prime(digs1)
        digs2 = random.randint(LDB,UDB)
        self.p2 = create_prime(digs2)
        self.lim = 10**(digs1 + digs2 - 2)
        self.n = self.p1*self.p2
        self.tot = (self.p1-1)*(self.p2-1)
        self.e = random.randint(2,self.tot-1)
        while euclid_gcd(self.e,self.tot) > 1:
            self.e = random.randint(2,self.tot-1)
        self.d = euclid_ext(self.e,self.tot)[0]
        self.publica = (self.n,self.e)
        self.privada = (self.d,self.p1,self.p2)


    def public_key(self):
        return self.publica
    
    def get_lim(self):
        return self.lim

    def get_id(self):
        return self.id

    
    def humanToCipher(self,lim,s):
        cipher = list()
        i = 0
        while i < len(s):
            curr = 0
            pot = 1
            while pot < lim and i < len(s):
                ascii_ind = ord(s[i])+1
                curr += (ascii_ind*pot)
                pot *= 1000
                i += 1
            cipher.append(curr)
        return cipher
        
    def cipherToHuman(self,cipher):
        s = ""
        while cipher > 0:
            ch = cipher%1000
            if ch > 128:
                return
            s += chr(ch-1)
            cipher //= 1000
        return s
    
    def encrypt(self,dest,mes):
        (n,e) = dest.public_key()
        lim = dest.get_lim()
        cipher = self.humanToCipher(lim,mes)
        print(cipher)
        return [(pow_ef(x,2,n)) for x in cipher]
    
    def decrypt(self,cipher):
        texts = list()
        for n in cipher:
            sq_modp = pow_ef(n,(self.p1+1)//4,self.p1)
            sq_modq = pow_ef(n,(self.p2+1)//4,self.p2)
            (x1,y1) = euclid_ext(self.p1,self.p2)
            r1 = (self.p1*sq_modq*x1+self.p2*sq_modp*y1)%self.n
            r2 = self.n - r1
            r3 = (self.p1*sq_modq*x1-self.p2*sq_modp*y1)%self.n
            r4 = self.n - r3
            roots = [r1,r2,r3,r4]

            frag = list()
            for r in roots:
                frag.append(self.cipherToHuman(r))
            texts.append(frag)
        
        print(texts)
        
        for i in range(len(texts[0])):
            text = ""
            j = 0
            exit = False
            while j < len(texts) and not exit:
                if texts[j][i] is None:
                    exit = True
                else:
                    text += texts[j][i]
                    j += 1
            if j == len(texts):
                return text

        return

    
    def send_message(self,dest,men):
        encr = self.encrypt(dest,men)
        print("Mensaje de {0} a {1}: Mensaje enviado: {2}".format(self.id,dest.get_id(),men))
        return encr


    def rec_message(self,sen,cif):
        decr = self.decrypt(cif)
        print("Mensaje de {0} a {1}: Mensaje recibido: {2}".format(sen.get_id(),self.id,decr))
        return decr



Alice = RSA("Alice")
Bob = RSA("Bob")
m1 = "Hola que tal"
m2 = "Muy bien"
m3 = "Codigos: a123421328910asfjkkljrijnij ijasirjijweqfdjasoirjqf184u312398jf"
m4 = "Ya han sido insertados"

en1 = Alice.send_message(Bob,m1)
Bob.rec_message(Alice,en1)

en2 = Bob.send_message(Alice,m2)
Alice.rec_message(Bob,en2)

en3 = Alice.send_message(Bob,m3)
Bob.rec_message(Alice,en3)

en4 = Bob.send_message(Alice,m4)
Alice.rec_message(Bob,en4)







            






