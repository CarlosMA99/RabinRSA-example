#Usuario con clave pública (nA, eA) y privada (pA, qA, dA)
#Firma a un usuario con clave pública (nB , eB) y privada (pB, qB, dB)
#El mensaje M ∈ Z/<N^k>

def firma_digital_sin_privacidad():
    C = expo_rapida(M,dA,nA)
    #Enviar C
    if (expo_rapida(C,eA,nA) == M)
    
def firma_digital_con_privacidad():
    C = expo_rapida(M,dA,nA)
    #Enviar C
    if (nA < nB):
        C = expo_rapida(expo_rapida(M,dA,nA)), eB, nB)
    else:
        C = expo_rapida(expo_rapida(M,eB,nB)), dA, nA)      
