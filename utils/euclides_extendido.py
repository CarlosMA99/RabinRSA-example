


def euclides_gcd(a,b):
    if a < b:
        a, b = b, a
    if a == 0 or b == 0:
        return a

    rem = a%b
    while rem > 0:
        a,b,rem = b,rem,b%rem
    return b


def euclides_extendido(a,b): # Función que calcula b^e mod n de manera eficiente. Si n=0 (por defecto) calcula b^e
    if a < b:
        a, b = b, a
    if a == 0 or b == 0:
        return a

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
    (p,q) = (seq1[k-1]*(-1)**k,seq2[k-1]*(-1)**(k+1))

    if p*a+q*b < 0:
        p, q = -p, -q
    
    return (p,q)

        

    
    