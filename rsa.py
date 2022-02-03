import random
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
    return num


def findkgram(em,rec):
    (n,e) = em.public_key()
    (n1,e1) = rec.public_key()
    inf = min(n,n1)
    i = 1
    while i*1000 < inf:
        i *= 1000
    return i




    


class RSA:
    def __init__(self,id):
        self.id = id
        pair1 = create_prime()
        pair2 = create_prime()
        if pair1 < pair2:
            pair1, pair2 = pair2, pair1
        self.p1 = pair1
        self.p2 = pair2
        self.n = self.p1*self.p2
        self.tot = ((self.p1-1)*(self.p2-1))//(ut.euclides_gcd(self.p1-1,self.p2-1))
        self.e = random.randint(2,self.tot-1)
        bezout = ut.euclides_extendido(self.tot,self.e)
        while bezout[2] > 1 or self.e == self.p1 or self.e == self.p2:
            self.e = random.randint(2,self.tot-1)
            bezout = ut.euclides_extendido(self.tot,self.e)
        self.d = bezout[1]%self.tot
        self.publica = (self.n,self.e)
        self.privada = (self.d,self.p1,self.p2)

    def get_id(self):
        return self.id

    def public_key(self):
        return self.publica

    
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
    
    def encrypt(self,dest,mes,kgram):
        (n,e) = dest.public_key()
        cipher = self.humanToCipher(kgram,mes)
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
        for i in range(len(texts)):
            for j in range(len(texts[0])):
                if texts[i][j][-1] == "&":
                    text += texts[i][j][:-1]
        return text

    def firmar_sin_privacidad(self,kgram):
        nE, dE = self.n, self.d
        mes = self.humanToCipher(kgram,self.id)
        c = list()
        for elem in mes:
            c.append(ut.expo_rapida(elem, dE, nE))
        return c
        
    def firmar_con_privacidad(self,dest,kgram):
        (nD,eD) = dest.public_key()
        nE, eE, dE = self.n, self.e, self.d
        mes = self.humanToCipher(kgram,self.id)
        c = list()
        if nE < nD:
            for elem in mes:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,dE,nE), eD, nD))
        else:
            for elem in mes:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,eD,nD), dE, nE))
        return c

    def verificar_firma_sin_privacidad(self,em,m,kgram):
        (nE, eE) = em.public_key()
        comp = self.humanToCipher(kgram,em.get_id())
        sign = list()
        for elem in m:
            sign.append(ut.expo_rapida(elem,eE,nE))
        if sign == comp:
            return True
        
        return False

    
    def verificar_firma_con_privacidad(self,em,m,kgram):
        (nE,eE) = em.public_key()
        nD, eD, dD = self.n, self.e, self.d
        comp = self.humanToCipher(kgram,em.get_id())
        sign = list()
        if nE < nD:
            for elem in m:
                sign.append(ut.expo_rapida(ut.expo_rapida(elem,dD,nD), eE, nE))
        else:
            for elem in m:
                sign.append(ut.expo_rapida(ut.expo_rapida(elem,eE,nE), dD, nD))
        if sign == comp:
            return True
        return False
        

    def send_message(self,dest,men,kgram,priv=True):
        encript_men = self.encrypt(dest,men,kgram)
        if priv:
            sign = self.firmar_con_privacidad(dest,kgram)
            print("Mensaje {0} a {1} de parte de {2} enviado con éxito. La firma se hará con privacidad".format(men,dest.get_id(),self.id))
        else:
            sign = self.firmar_sin_privacidad(kgram)
            print("Mensaje {0} a {1} de parte de {2} enviado con éxito. La firma se hará sin privacidad".format(men,dest.get_id(),self.id))
        return [encript_men,sign]


    def rec_message(self,sen,cif,kgram,priv=True):
        decr = self.decrypt(cif[0])
        if priv:
            ok = self.verificar_firma_con_privacidad(sen,cif[1],kgram)
            if ok:
                print("Mensaje {0} a {1} de parte de {2} recibido y firma validada con éxito".format(decr,self.id,sen.get_id()))
            else: 
                print("Recepción fallida. Firma no válida.")
        else:
            ok = self.verificar_firma_sin_privacidad(sen,cif[1],kgram)
            if ok:
                print("Mensaje {0} a {1} de parte de {2} recibido y firma validada con éxito".format(decr,self.id,sen.get_id()))
            else: print("Recepción fallida. Firma no válida.")

    def intercambiar_mensaje(self,dest,men,priv=True):
        kgram = findkgram(self,dest)
        encr = self.send_message(dest,men,kgram,priv)
        dest.rec_message(self,encr,kgram,priv)


