#Affine decode test
import pickle as pk
from decimal import Decimal
import sys

global ENGD
inf = open("Dicts/ENGDICT","rb")
ENGD = pk.load(inf)
inf.close()

def ILG(message):
    global ENGD
    global dec
    global S

    match = 0
    dec = False

    WIM = message.split(" ")
    for i in WIM:
        if i.upper() in ENGD:
            match += 1
        else:
            pass
    certainty = match/len(WIM)
    certainty = certainty * 100
    nc = round(Decimal(certainty),2)
    #if S == False:
    #    print("likelyhood:",str(nc)+"%")
    #else:
    #    pass
    if certainty >=20:
        print("likelyhood:",str(nc)+"%")
        dec = True
    else:
        dec = False
    return dec

def CK(ka,kb,SCS):
    if ka < 0 or kb < 0 or kb > len(SCS) - 1:
        sys.exit('Key A must be greater than 0 and Key B must bebetween 0 and %s.' % (len(SCS) - 1))
    if gcd(ka, len(SCS)) != 1:
        sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA,len(SCS)))



SCS = 'abcdefghijklmnopqrstuvwxyz'
def start(SCS):
    print("ENTER TEXT HERE:")
    inp = str(input(">> "))
    print("===================================")
    hack(SCS,inp)

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def MOI(a, m):
    if gcd(a, m) != 1:
        return None  # No mod inverse if a & m aren't relatively prime.
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # Note that // is the integer division operator.
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def GK(k,SCS):
    keyA = k // len(SCS)
    keyB = k % len(SCS)
    return (keyA, keyB)

def decrypt(key,phrase,SCS):
    t  = ""
    KA, KB = GK(key,SCS)
    CK(KA,KB,SCS)
    MOIA = MOI(KA,len(SCS))
    for char in phrase:
        if char in SCS:
            SI = SCS.find(char)
            t+=SCS[(SI-KB)*MOIA%len(SCS)]
        else:
            t+=char
        
    
    return t

def hack(SCS,phrase):
    print(SCS)
    for i in range(len(SCS)**2):
        #print(range(len(SCS)**2))
        KA = GK(i,SCS)[0]
        KB = GK(i,SCS)[1]
        print(KA,KB)
        if gcd(KA,len(SCS)) != 1:
            continue
        d = decrypt(i,phrase,SCS)
        print("tried %s... (%s)" %(i,d[:40]))

        if ILG(d) == True:
            print("POSSIBLE KEY: %s"%(i))
            print(d)
            inp = str(input("[Y/N]?\n>> "))
            if inp.upper() == "Y":
                print(d)
                break

    inp = input(">> ")
                

start(SCS)
        
    
                
                
    
    
