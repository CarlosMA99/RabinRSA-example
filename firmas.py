from utils.expo_rapida import expo_rapida as pow_ef

#Usuario con clave pública (nA, eA) y privada (pA, qA, dA)
#Firma a un usuario con clave pública (nB , eB) y privada (pB, qB, dB)
#El mensaje M ∈ Z/<N^k>

def firma_digital_sin_privacidad():
    C = pow_ef(M,dA,nA)
    #Enviar C
    if (pow_ef(C,eA,nA) == M):
        #El mensaje se verifica
    
def firma_digital_con_privacidad():
    C = pow_ef(M,dA,nA)
    #Enviar C
    if (nA < nB):
        C = pow_ef(pow_ef(M,dA,nA)), eB, nB)
    else:
        C = pow_ef(pow_ef(M,eB,nB)), dA, nA)      
