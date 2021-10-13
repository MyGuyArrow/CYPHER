#This program will decrypt messages from the CYPHER challenge and provide anaysis tools
import time
import pickle as pk
import os
import math as m #not needed yet...
from decimal import Decimal
import sys

global CSD # character set dictionary
global SCS # selected Character Set
global ENGD # English dictionary
global S # silent mode
global KEY # key found from shift

KEY = None

def cls():
    n = 150
    for i in range(n):
        print("")

def BACK(message):
    print(message)
    print("RETURNING")
    time.sleep(2)
    cls()
    start()
    return

#LANGUAGE DETECTION
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

def text(op):
    global SCS
    global ENGD
    global S
    global KEY

    print(" _________ _____.___.__________   ___ ___ _____________________\n \\_   ___ \\\\__  |   |\\______   \\ /   |   \\\\_   _____/\\______   \\ \n /    \\  \\/ /   |   | |     ___//    ~    \\|    __)_  |       _/ \n \\     \\____\\____   | |    |    \\    Y    /|        \\ |    |   \\ \n  \\______  // ______| |____|     \\___|_  //_______  / |____|_  / \n         \\/ \\/                         \\/         \\/         \\/ \n")
    print("=================================================================")
    try:
        if S == True:
            SM = "ON"
            print("Char Set:",SCS,"    SILENT MODE:",SM)
        else:
            SM = "OFF"
            print("Char Set:",SCS,"    SILENT MODE:",SM)
    except:
        if S == True:
            SM = "ON"
            print("Char Set: NONE      SILENT MODE:",SM)
        else:
            SM = "OFF"
            print("Char Set: NONE      SILENT MODE:",SM)
    
    if ENGD != None:
        if KEY == None:
            print("DICT: LOADED | KEY: NONE")
        else:
            print("DICT: LOADED | KEY:",KEY)
    else:
        if KEY == None:
            print("DICT: NONE   | KEY: NONE")
        else:
            print("DICT: NONE   | KEY:",KEY)

    if op == 1:
        print("=================================================================")
        print("> Ceaser")
        print("> Affine")
        print("> Analyse")
        print("> Settings")
        print("====================")
    else:
        pass

def start():
    text(1)
    inp = input(str(">> "))
    if inp == "1":
        ceaser()
        return

    elif inp == "2":
        affine()
        return

    elif inp == "4":
        settings()
        return
    elif inp == "3":
        anal()
        return

    elif inp.upper() == "END":
        quit()

    else:
        BACK("ERROR")
        return

def anal():
    global S

    cls()
    text(0)
    
    print("=================================================================")
    print("Enter Path to file:")
    p = str(input(">> "))
    inf = open(p,"r")
    code = inf.read()
    inf.close()
    print("FILE LOADED...")
    print("GENERALISING TEXT")
    code = code.upper()
    if S == False:
        print("=================================================================")
        print("GENERALISED CODE:")
        print("=================================================================")
        print(code)
        print("=================================================================")
    else:
        pass
    print("TRY C/A SHIFT? [Y/N]")
    inp = str(input(">> "))
    if inp.upper() == "Y":
        print("OK")
        print("TRYING CEASER")
        FSC(1,code)

    inp=input("DEBUG STOP")


def affine():
    cls()
    text(0)
    print("=================================================================")
    print("AFFINE OPTIONS")
    print("=================================================================")
    print("> Find key")
    print("> DeCYPHER")
    print("> Back")
    print("=================================================================")
    inp = input(str(">> "))
    if inp == "1":
        FAK()
    elif inp == "2":
        FDA()
    elif inp == "3":
        BACK("OK")
    else:
        affine()
    return

def CK(ka,kb,SCS):
    if ka < 0 or kb < 0 or kb > len(SCS) - 1:
        sys.exit('Key A must be greater than 0 and Key B must bebetween 0 and %s.' % (len(SCS) - 1))
    if gcd(ka, len(SCS)) != 1:
        sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA,len(SCS)))

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

def hack(SCS,phrase,mode):
    global S
    global KEY
    if mode == 0:
        print("================================================================")
    else:
        pass
    for i in range(len(SCS)**2):
        #print(range(len(SCS)**2))
        KA = GK(i,SCS)[0]
        KB = GK(i,SCS)[1]
        #print(KA,KB)
        if gcd(KA,len(SCS)) != 1:
            continue
        d = decrypt(i,phrase,SCS)
        if S == False:
            print("tried %s... (%s)" %(i,d[:40]))
        else:
            pass

        if ILG(d) == True:
            print("POSSIBLE KEY: %s"%(i))
            print(d)
            inp = str(input("[Y/N]?\n>> "))
            if inp.upper() == "Y":
                print("KEY SAVED")
                KEY = i
                break

#find affine key
def FAK():
    global SCS
    global S
    print("=================================================================")
    print("Enter Phrase Below:")
    phrase = input(str(">> "))
    hack(SCS,phrase,0)
    inp = input(str("DONE"))
    BACK("TAKING YOU BACK")

#find Deciphered Affine (with key)
def FDA():
    global SCS
    global KEY
    print("=================================================================")
    if KEY == None:
        k = input("Enter Key:\n>> ")
        try:
            K = int(k)
        except:
            print("Not an Integer...")
            BACK("Dummy")
            return
        print("Accepted value")
    else:
        print("SAVED KEY:",KEY,"USED")
    print("Enter Path to File:")
    p = input(">> ")
    inf = open(p,"r")
    code = inf.read()
    print("GENERALISE CASE? [Y/N]")
    inp = str(input(">> "))
    if inp.upper() == "Y":
        code.upper()
    else:
        pass
    inf.close()
    print("DECODING:")
    print("=================================================================")
    print(code)
    print("=================================================================\n")
    translated = decrypt(KEY,code,SCS)
    print("DECODED:")
    print("=================================================================")
    print(translated)
    print("=================================================================")
    inp = input("DONE")
    print("SAVING CODE AS: DECYPHERED.txt")
    with open("DECYPHERED.txt", "w") as f:
        c = 0
        for i in translated:
            if c == 40:
                f.write("\n")
                c = 0
                return
            else:
                f.write(i)
    inp = input("DONE\n")
    BACK("TAKING YOU BACK")

def ceaser():
    cls()
    text(0)
    print("=================================================================")
    print("CEASER OPTIONS")
    print("=================================================================")
    print("> Find shift")
    print("> DeCYPHER")
    print("> Back")
    print("=================================================================")
    inp = input(str(">> "))
    if inp == "1":
        FCS(0,None)
    elif inp == "2":
        FDC()
    elif inp == "3":
        BACK("OK")
    else:
        ceaser()


# find decrypted ceaser
def FDC():
    global SCS
    global KEY
    cls()
    text(0)
    print("=================================================================")
    print("Enter Shift by:")
    if KEY == None:
        shift = input(">> ")
        try:
            S = int(shift)
        except:
            print("THATS NOT A NUMBER >:(")
            BACK("TAKING YOU BACK")
            return
        print("Accepted Value")
    else:
        print("SAVED KEY:",KEY,"USED")
        S = KEY
    
    print("\nEnter path to .txt:")
    p = input(str(">> "))

    inf = open(p,"r")
    code = inf.read()
    inf.close()
    print("GENERALISE CASE? [Y/N]")
    inp = str(input(">> "))
    if inp.upper() == "Y":
        code.upper()
    else:
        pass
    print("DECODING:")
    print("=================================================================")
    print(code)
    print("=================================================================")

    translated = ""
    for char in code:
        if char in SCS:
            num = SCS.find(char)
            num -= S
            if num < 0:
                num += len(SCS)
            else:
                pass
            translated += SCS[num]
        else:
            translated += char
    print("=================================================================")
    print("DECRYPTED CODE IS:")
    print("=================================================================")
    print(translated)
    print("=================================================================")
    inp = input("DONE")
    print("=================================================================")
    print("SAVING CODE AS: DECYPHERED.txt")
    with open("DECYPHERED.txt", "w") as f:
        c = 0
        for i in translated:
            if c == 40:
                f.write("\n")
                c = 0
                return
            else:
                f.write(i)
    inp = input("DONE\n")
    BACK("TAKING YOU BACK")


#find ceaser shift   
def FCS(mode,phrase):
    cls()
    text(0)
    
    global SCS
    global S
    global KEY
    comp = False
    PT = []
    if mode ==0:
        print("================================================================")
        print("Enter Phrase Below:")
        phrase = input(str(">> "))
        print()
        return
    else:
        pass
    
    for key in range(len(SCS)):
        translated = ""
        for symbol in phrase:
            if symbol in SCS:
                num = SCS.find(symbol)
                num -= key
                if num < 0:
                    num += len(SCS)
                else:
                    pass
                translated += SCS[num]
                
            else:
                translated += symbol
        if S == False:
            if ILG(translated) == True:
                print("POSSIBLE KEY:",key,"Text:",translated)
                PT.append((key,translated))
                KEY = key
                print("SAVED KEY")
                comp = True
            else:
                print("TRIED KEY:",key)
                print()
        else:
            if ILG(translated) == True:
                print("POSSIBLE KEY:",key,translated)
                PT.append((key,translated))
                KEY = key
                print("SAVED KEY")
                comp = True
            else:
                pass
    
    inp = input("DONE")
    if mode == 0:
        BACK("TAKING YOU BACK")
        return
    else:
        return comp


def settings():
    global SCS
    global CSD
    global ENGD
    global S
    global KEY

    cls()
    text(0)
    print("==================")
    print("OPTIONS")
    print("==================")
    print("> Add Char Set")
    print("> Choose Char Set")
    print("> Add Dict - NOT SUPPORTED YET")
    print("> View Dict")
    print("> Silent Mode")
    print("> Clear Saved KEY")
    print("> Back")
    print("==================")
    inp = input(">> ")
    if inp == "1":
        cls()
        print("ENTER NEW CHARSET Name:")
        NSN = input(str(">> ")) # new set name
        print()
        print("ENTER NEW CHARSET:")
        NS = input(str(">> "))
        cls()
        print("ADDING NEW CHARSET")
        CSD[NSN]=NS
        out = open("CHARSET", "wb")
        pk.dump(CSD, out)
        out.close()
        BACK("DONE")
        return


    elif inp == "2":
        cls()
        text(0)
        print("=================================================================")
        print("AVAILABLE SETS")
        print("=================================================================")
        for key,value in CSD.items():
            print("NAME : {}, SET : {}".format(key, value))
        print("============================")
        print("Select Char Set (ENTER NAME)")
        print("============================")
        name = input(str(">> "))
        if name == "B" or name == "b":
            print("OK")
            settings()
            return
        else:
            try:
                SCS = CSD.get(name)
                print("new set is:",SCS)
                BACK("DONE")
                return
            except:
                BACK("ERROR")
                return
        return

    elif inp == "3":
        pass

    elif inp == "4":
        for i in ENGD.keys():
            print(i)
            
        inp = input(str(""))
        BACK("DONE")

    elif inp == "5":
        if S == False:
            S = True
        else:
            S = False
        cls()
        settings()

    elif inp == "6":
        KEY = None
        settings()

    elif inp == "7":
        BACK("OK")
    else:
        BACK("ERROR")
    return

def init():
    global SCS
    global CSD
    global ENGD
    global S
    S = False
    dict = {"CAPS":"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "lower":"abcdefghijklmnopqrstuvwxyz"}
    try:
        inf = open("Charsets/CHARSET", "rb")
        CSD = pk.load(inf)
        print("INITIALISING CHARSET")
        inf.close()

    except FileNotFoundError:
        print("CHARSETS NOT FOUND, CREATING CHARSETS")
        out = open("Charsets/CHARSET", "wb")
        pk.dump(dict, out)
        print("DONE")
        out.close()
    inf = open("Charsets/CHARSET", "rb")
    CSD = pk.load(inf)
    print("LOADING DEFAULT CHARSET")
    SCS = CSD.get("CAPS")
    print("DONE")
    inf.close()


    try:
        inf = open("Dicts/ENGDICT","rb")
        dict = pk.load(inf)
        print("INITIALISING ENGLISH DICT")
        inf.close()
        ENGD = dict
        print("DONE")


    except FileNotFoundError:
        print("ENG DICT NOT FOUND, CREATING DICT")
        ENGD = {}
        inf = open("ENGDICT.txt","r")
        dict = inf.read().split("\n")
        for word in dict:
            ENGD[word]=None
        out = open("Dicts/ENGDICT","wb")
        pk.dump(ENGD,out)
        inf.close()
        print("DONE")

    #print(ENGD)
    print("DONE INITIALISING")
    BACK("OK")

init()