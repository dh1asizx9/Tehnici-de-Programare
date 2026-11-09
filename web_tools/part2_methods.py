# Laborator: funcții, metode și importuri pe web
# Student: Agheorghesi Paul-Florian SI-266
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

from part1_imports import *
time.sleep(1)

print("\n")

response = requests.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code) # atribut
print(response.ok) # atribut
print(response.url) # atribut
print(response.encoding) # atribut

print("\n")

time.sleep(1)

try:

    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    print("Pagina principala s-a incarcat")

    invalid = BASE_URL + "/this-page-does-not-exist"
    bad_response = requests.get(invalid, timeout=TIMEOUT)
    bad_response.raise_for_status()

except requests.exceptions.HTTPError as e:
    print(f"A aparut o problema :C (eroare:{e})")

time.sleep(1)
print("\n")

response = requests.get(BASE_URL, timeout=TIMEOUT)
for Nume, valoare in response.headers.items():
    print(f"{Nume}: {valoare}")

time.sleep(1)
print("\n")

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Server: ", response.headers.get("Server", "lipseste"))
print("Content-Type: ", response.headers.get("Content-Type", "lipseste"))

print("\n")

print("content-type: ", response.headers.get("content-type", "lipseste"))
# afiseaza indiferent, dat fiind ca response.headers este case-insensitive

time.sleep(1)
print("\n")

response = requests.get(BASE_URL, timeout=TIMEOUT)
count = response.text.lower().count("cyber")
print(f"Cuvantul apare de {count} ori")
# ambele ofera operatii de transformare a textului si in acelasi timp, .lower() returneaza tot un string, astfel se poate inlantui mai multe metode care fac operatii pe stringuri

time.sleep(1)
print("\n")

titlu = response.text
start = "<title>"
end = "</title>"
start_index = titlu.find(start) + len(start)
end_index = titlu.find(end)
if titlu.find(start) != -1 and end_index != -1:
    titlu_clar = titlu[start_index:end_index].strip()
    print(f"Titlul: {titlu_clar}")
else:
    print("Nu s-a gasit titlul :C")

print("\n")

html = response.text
linii = html.splitlines()
print(f"Numarul total de linii: {len(linii)}")
linia_lunga = max(linii, key=len)
print(f"Lungimea celei mai lungi linii: {len(linia_lunga)} caractere")

print("\n")
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)
if response.url.startswith("https://"):
    print("Conexiune securitaza :D")
else:
    print("Conexiune nesecurizata :C")

print("\n")
time.sleep(1)

url_http = "http://cybercor.org"
response = requests.get(url_http, timeout=TIMEOUT)
print("Istoric: ")
for rasp in response.history:
    print(f"Status: {rasp.status_code} -> URL: {rasp.url}")
print(f"URL-ul final: {response.url}")

print("\n")
time.sleep(1)

response_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
response_get = requests.get(BASE_URL, timeout=TIMEOUT)

print(f"Lungime head: {len(response_head.content)}")
print(f"Lungime get: {len(response_get.content)}")
# HEAD solicita metadatele fara sa descarce continutul html al paginii, pe cand get face asta

print("\n")
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)
if response.cookies:
    for cookie in response.cookies:
        print(f"Nume cookie: {cookie.name} | Secure: {cookie.secure}")
else:
    print("Nu avem prajituri :C")

print("\n")
time.sleep(1)

session = requests.Session()
session.headers.update({"User-Agent": "WebLab - Agheorghesi Paul-Florian"})

response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)

print("Folosind response.text: ")
print(response.text)

print("\n")

print("Folosind response.json(): ")
print(response.json())
# .text este un atribut; pe cand .json() este o functie