import re
import base64
from urllib.parse import unquote
import hashlib
import argparse
import json
import os

# A2
def ghici_strat(s):
    s = s.strip()
    pattern_url = re.search(r'%[0-9a-fA-F]{2}', s)
    pattern_hex = re.fullmatch(r'[0-9a-f]+', s)
    pattern_base64 = re.fullmatch(r'[A-Za-z0-9+/=]+', s)

    if pattern_url:
        return "url"
    elif len(s) % 2 == 0 and pattern_hex:
        return "hex"
    elif pattern_base64:
        return "base64"
    else:
        return "necunoscut"

print("\n")
print(ghici_strat("%2Fetc"))   
print(ghici_strat("48656c6c6f"))
print("\n")

# A3
def desfa(s):
    strat = ghici_strat(s)
    rezultat = None
    
    if strat == "url":
        rezultat = unquote(s).encode()
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "base64":
        rezultat = base64.b64decode(s)
    else:
        rezultat = s.encode("latin1", errors="ignore")

    return strat, rezultat

# A4
def citibil(b):
    return all(32 <= c < 127 for c in b)

val = "NTM1OTU3NTk="

for _ in range(8): 
    strat, b = desfa(val) 

    if citibil(b):
        print(f"Text gasit: {b.decode('utf-8', errors='ignore')}")
        break
    else:
        val = b.decode('utf-8', errors='ignore')
        

# A5
def ruleaza_xor(cale_bin="probe/xor.bin"):
    if not os.path.exists(cale_bin):
        print(f"Error {cale_bin} nu a fost gasit.")
        return
    date = open(cale_bin, "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print(f"Cheie gasita: {k}; Mesaj: {clar.decode('utf-8', errors='ignore')}")

print("\n")
ruleaza_xor()

# A6
def ruleaza_hash(cale_hashuri="probe/hashuri.txt", cale_wordlist="probe/wordlist.txt"):
    if not os.path.exists(cale_hashuri) or not os.path.exists(cale_wordlist):
        print("error")
        return
    
    tinta = open(cale_hashuri).readline().strip()
    for cuv in open(cale_wordlist, encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print(f"Hash gasit: {cuv}")
            break

print("\n")
ruleaza_hash()
print("\n")


# A7
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    
    a = p.parse_args()

    if a.intrare:
        if a.fisier:
            with open(a.intrare, "r", encoding="utf-8-sig") as f:
                val = f.read().strip()
        else:
            val = a.intrare

        strat_final = "necunoscut"
        rezultat_final = val.encode()

        for _ in range(8):
            strat, b = desfa(val)
            if strat == "necunoscut":
                break
            else:
                strat_final = strat
                rezultat_final = b
                val = b.decode("latin1", errors="ignore")

        os.makedirs("arsenal/forensics", exist_ok=True)
        output = {
            "strat": strat_final,
            "rezultat": rezultat_final.decode("utf-8", errors="ignore")
        }

        with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print(f"Salvat in arsenal/forensics/fisa.json; Strat final: {strat_final}")

print("\n")