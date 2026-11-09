# Laborator: functii, metode si importuri pe web
# Student: Agheorghesi Paul-Florian SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import requests
from requests import get
import requests as rq
import urllib.request
import time
# requests este un modul; pe cand urllib este un package
print(requests.__version__)
print(requests.get(BASE_URL))
time.sleep(1)

print("\n")

print(get(BASE_URL))
time.sleep(1)

print("\n")

# prin import requests aduce toate metodele, pe cand cu from requests import get aduce doar metoda
# daca se foloseste o majoritate din metode, un import complet ar fi ideal; dar daca se foloseste doar cateva din metode, cu from e suficient
print(rq.get(BASE_URL))

print("\n")

# un alias face mai usor de citit daca acronimele sunt usor de descrifat; dar poate sa puna piedici daca sunt folosite in mod abuziv
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},)
with urllib.request.urlopen(req) as test:
    proba = test.status
    response = test.read()
    output = response.decode("utf-8")
print("Status: ", proba)

print(output[:200])

print("\n")

# a trebuit sa creez un header cu user agent ca sa nu mai ma trezesc cu 403 :C   
print(dir(requests))

print("\n")

# requests, e un modul; __loader__, este o clasa; Request este o functie
help(requests.get)
time.sleep(1)

print("\n")

try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    print("Status: ", response.status_code)
    print(response.text[:200])
except requests.exceptions.Timeout:
    print("Timeout oops")
time.sleep(1)

print("\n")

timp_start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
timp_stop = time.perf_counter()

diferenta = timp_stop - timp_start

print("\n")

print(f"Masurat manual: {diferenta:.4f} secunde")
print(f"Cu .elapsed: {response.elapsed.total_seconds()} secunde")

print("\n")

try:
    import bs4
    print("Modulul este instalat")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")