import random
import utils as ut

LDB = 300
UDB = 500
CARD = 257

def create_prime(digs):
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




    


class RSA:
    def __init__(self,id):
        self.id = id
        digs1 = random.randint(LDB,UDB)
        self.p1 = create_prime(digs1)
        digs2 = random.randint(LDB,UDB)
        self.p2 = create_prime(digs2)
        if self.p1 < self.p2:
            self.p1 , self.p2 = self.p2, self.p1
        self.lim = ut.expo_rapida(10,digs1 + digs2 - 1)
        self.n = self.p1*self.p2
        self.tot = (self.p1-1)*(self.p2-1)
        self.e = random.randint(2,self.tot-1)
        bezout = ut.euclides_extendido(self.tot,self.e)
        while bezout[2] > 1:
            self.e = random.randint(2,self.tot-1)
            bezout = ut.euclides_extendido(self.tot,self.e)
        self.d = bezout[1]
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
                if ascii_ind >= 1000:
                    print(ascii_ind)
                curr += (ascii_ind*pot)
                pot *= 1000
                i += 1
            cipher.append(curr)
        return cipher
        
    def cipherToHuman(self,cipher):
        s = ""
        while cipher > 0:
            ch = cipher%1000
            if ch > CARD:
                return
            s += chr(ch-1)
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

    #Usuario con clave pública (nA, eA) y privada (pA, qA, dA)
    #Firma a un usuario con clave pública (nB , eB) y privada (pB, qB, dB)
    #El mensaje M ∈ Z/<N^k>
        
    def firmar_con_privacidad(self,dest):
        menfirma = "Firmado"
        (nD,eD) = dest.public_key()
        nE, eE, dE = self.n, self.e, self.d
        lim = min(self.lim,dest.get_lim())
        #Enviar C
        c = list()
        m = self.humanToCipher(lim,menfirma)
        if nE < nD:
            for elem in m:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,dE,nE), eD, nD))
        else:
            for elem in m:
                c.append(ut.expo_rapida(ut.expo_rapida(elem,eD,nD), dE, nE))
        return c

    
    def verificar_firma(self,em,m):
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
        print(menfirma)
        if menfirma == "Firmado":
            print("Firma válida\n")
            return True
        print("Firma no válida\n")
        return False
        

    def send_message(self,dest,men):
        return [self.encrypt(dest,men),self.firmar_con_privacidad(dest)] 


    def rec_message(self,sen,cif):
        decr = self.decrypt(cif[0])
        self.verificar_firma(sen,cif[1])
        return decr


Alice = RSA("Alice")
Bob = RSA("Bob")
m1 = "Hola que tal"
m2 = "Muy bien"
m3 = "Códigos: ñóáéíóúa123421328910asfjkkljrijnij ijasirjijweqfdjasoirjqf184u312398jf"
m4 = "Ya han sido insertados"

en1 = Alice.send_message(Bob,m1)
dec1 = Bob.rec_message(Alice,en1)

en2 = Bob.send_message(Alice,m2)
dec2 = Alice.rec_message(Bob,en2)

en3 = Alice.send_message(Bob,m3)
dec3 = Bob.rec_message(Alice,en3)

en4 = Bob.send_message(Alice,m4)
dec4 = Alice.rec_message(Bob,en4)







            






