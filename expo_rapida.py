

def expo_rapida(b,e,n): # Función que calcula b^e mod n de manera eficiente. Si n=0 (por defecto) calcula b^e
    if e == 0:
        return 1
    b %= n
    res = 1
    while e > 0:
        if e%2 == 1:
            res = (res*b)%n
        b = (b*b)%n
        e //= 2
    return res