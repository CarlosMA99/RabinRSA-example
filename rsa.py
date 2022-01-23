import random
from re import L
import utils as ut

LDB = 300
UDB = 500
CARD = 256

def create_prime():
    digs = random.randint(LDB,UDB)
    impares = [1,3,7,9]
    pot = 10
    num = random.choice(impares)
    for i in range(digs-2):
        num += (random.randint(0,9))*pot
        pot *= 10
    num += (random.randint(1,9))*pot

    while num % 4 == 1 or not ut.es_primo_miller_rabin(num):
        digs = random.randint(LDB,UDB)
        pot = 10
        num = random.choice(impares)
        for i in range(digs-2):
            num += (random.randint(0,9))*pot
            pot *= 10
        num += (random.randint(1,9))*pot
    
    return (num,digs)




    


class RSA:
    def __init__(self):
        pair1 = create_prime()
        pair2 = create_prime()
        if pair1[0] < pair2[0]:
            pair1, pair2 = pair2, pair1
        self.p1 = pair1[0]
        self.p2 = pair2[0]
        self.n = self.p1*self.p2
        self.lim = ut.expo_rapida(10,pair1[1] + pair2[1] - 1)
        self.tot = (self.p1-1)*(self.p2-1)
        self.e = random.randint(2,self.tot-1)
        bezout = ut.euclides_extendido(self.tot,self.e)
        while bezout[2] > 1 and (self.e == self.p1 or self.e == self.p2):
            self.e = random.randint(2,self.tot-1)
            bezout = ut.euclides_extendido(self.tot,self.e)
        self.d = bezout[1]
        self.publica = (self.n,self.e)
        self.privada = (self.d,self.p1,self.p2)


    def public_key(self):
        return self.publica
    
    def get_lim(self):
        return self.lim

    
    def humanToCipher(self,lim,s):
        cipher = list()
        i = 0
        while i < len(s):
            curr = 0
            pot = 1
            while pot < lim//1000 and i < len(s):
                ascii_ind = ord(s[i])+1
                curr += (ascii_ind*pot)
                pot *= 1000
                i += 1
            curr += (ord('&')+1)*pot # & es un caracter de control para saber cuál es la cadena correcta cuando decodifiquemos
            cipher.append(curr)
        return cipher
        
    def cipherToHuman(self,cipher):
        s = ""
        while cipher > 0:
            ch = cipher%1000
            s += chr((ch-1)%CARD)
            cipher //= 1000
        return s
    
    def encrypt(self,dest,mes):
        (n,e) = dest.public_key()
        lim = dest.get_lim()
        cipher = self.humanToCipher(lim,mes)
        return [(ut.expo_rapida(x,2,n)) for x in cipher]
    
    def decrypt(self,cipher):
        texts = list()
        for n in cipher:
            sq_modp = ut.expo_rapida(n,(self.p1+1)//4,self.p1)
            sq_modq = ut.expo_rapida(n,(self.p2+1)//4,self.p2)
            (x1,y1,mcd) = ut.euclides_extendido(self.p1,self.p2)
            r1 = (self.p1*sq_modq*x1+self.p2*sq_modp*y1)%self.n
            r2 = self.n - r1
            r3 = (self.p1*sq_modq*x1-self.p2*sq_modp*y1)%self.n
            r4 = self.n - r3
            roots = [r1,r2,r3,r4]
            frag = list()
            for r in roots:
                frag.append(self.cipherToHuman(r))
            texts.append(frag)
            
        text = ""
        for i in range(len(texts[0])):
            for j in range(len(texts)):
                if texts[j][i][-1] == "&":
                    text += texts[j][i][:-1]

        return text
        
    def firmar_con_privacidad(self,dest,mes):
        (nD,eD) = dest.public_key()
        nE, eE, dE = self.n, self.e, self.d
        lim = min(self.lim,dest.get_lim())
        #Enviar la firma c
        c = list()
        m = self.humanToCipher(lim,mes)
        if nE < nD:
            for elem in m:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,dE,nE), eD, nD))
        else:
            for elem in m:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,eD,nD), dE, nE))
        return c

    def firmar_sin_privacidad(self,dest,mes):
        (nD,eD) = dest.public_key()
        nE, eE, dE = self.n, self.e, self.d
        lim = min(self.lim,dest.get_lim())
        #Enviar la firma c
        c = list()
        m = self.humanToCipher(lim,mes)
        for elem in m:
            c.append(ut.expo_rapida(elem, dE, nE))
        return c

    
    def verificar_firma(self,em,m,comp):
        (nE,eE) = em.public_key()
        nD, eD, dD = self.n, self.e, self.d
        men = list()
        if nE < nD:
            for elem in m:
                men.append(ut.expo_rapida(ut.expo_rapida(elem,dD,nD), eE, nE))
        else:
            for elem in m:
                men.append(ut.expo_rapida(ut.expo_rapida(elem,eE,nE), dD, nD))
        menfirma = ""
        for elem in men:
            menfirma += self.cipherToHuman(elem)
        if menfirma.__eq__(comp):
            print("Firma válida")
            return True
        print("Firma no válida")
        return False


    def verificar_firma_sin_privacidad(self,em,m,comp):
        (nE,eE) = em.public_key()
        nD, eD, dD = self.n, self.e, self.d
        men = list()
        for elem in m:
            men.append(ut.expo_rapida(ut.expo_rapida(elem,dD,nD), eE, nE))
        menfirma = ""
        for elem in men:
            menfirma += self.cipherToHuman(elem)
        if menfirma.__eq__(comp):
            print("Firma válida")
            return True
        print("Firma no válida")
        return False
        

    def send_message(self,dest,men):
        return [self.encrypt(dest,men),self.firmar_con_privacidad(dest,men)] 


    def rec_message(self,sen,cif):
        decr = self.decrypt(cif[0])
        self.verificar_firma(sen,cif[1],decr)
