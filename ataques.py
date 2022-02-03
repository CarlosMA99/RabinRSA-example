import time
import random
import rsa
from utils import expo_rapida as pow_ef
from utils import euclides_gcd as mcd

def rho_pollard(n):
    if n == 1:
        return n
    if n%2 == 0:
        return 2
    
    x = random.randint(0,n-1)
    y = x
    c = random.randint(1,n-1)

    gcd = 1

    time_ret = 10
    time_start = time.time()
    time_end = time_start + time_ret
    while (gcd == 1 or gcd == n) and time.time() < time_end:

        if gcd == n:
            x = random.randint(0,n-1)
            y = x
            c = random.randint(1,n-1)
        
        x = (pow_ef(x,2,n) + c)%n
        y = (pow_ef((pow_ef(y,2,n) + c)%n,2,n) + c)%n
        gcd = mcd(abs(x-y),n)

    if gcd == 1 or gcd == n:
        return
    return gcd