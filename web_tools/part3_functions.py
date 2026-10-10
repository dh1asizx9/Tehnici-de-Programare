# Laborator: funcții, metode și importuri pe web
# Student: Agheorghesi Paul-Florian SI-266
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

from part1_imports import *
from part2_methods import *

def fetch(url, timeout=10):
    return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)

print("\n")
time.sleep(1)

response = fetch(BASE_URL)
print(f"Codul pentru {BASE_URL}: {response.status_code}")

print("\n")
time.sleep(1)

def get_status(url: str) -> int:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
    return response.status_code

paths = ["/", "/robots.txt", "/sitemap.xml"]

for path in paths:
    url_full = BASE_URL + path
    status = get_status(url_full)
    print(f"URL: {url_full} | Cod: {status}")
    time.sleep(1)

print("\n")
time.sleep(1)

respose_implicit = fetch(BASE_URL)
print(f"Cu valoare implicita - Status: {respose_implicit.status_code}")
time.sleep(1)
response_given = fetch(BASE_URL, timeout=3)
print(f"Cu valoare data - Status: {response_given.status_code}")

print("\n")
time.sleep(1)

def get_title(html):

    """
       Aceasta functie extrage si returneaza doar titlul. 
    
       Cauta tag-urile de titlu <title> si </title>, extrage textul dintre ele si elimina spatiile cu .strip().

       Argumente:
        get_title(var.text) 
    """

    start = "<title>"
    end = "</title>"

    start_index = html.find(start)
    end_index = html.find(end)

    if start_index != -1 and end_index != -1:
        start_index += len(start)
        return html[start_index:end_index].strip()

    return "Nu s-a gasit un titlu :C"

response = fetch(BASE_URL)
title = get_title(response.text)
print(f"Titlul este: {title}")

print("\n")
time.sleep(1)

help(get_title)

print("\n")
time.sleep(1)

# print(get_status(123))
# codul a rulat fara nici o problema, dar cand a ajuns la executie, s-a blocat si a aruncat o eroare

print("\n")
time.sleep(1)

def page_exists(url: str) -> bool:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return response.ok
    except requests.RequestException:
        return False

print("Url valid: ", page_exists(BASE_URL))
print("\n")
time.sleep(1)
print("Url invalid: ", page_exists("https://this-domain-does-not-exist.invalid"))
print("\n")

time.sleep(1)

def check_paths(base: str, paths: list[str]) -> dict:
    results = {}
    for path in paths:
        url_full = base + path
        results[path] = get_status(url_full)
    return results

lista_paths = ["/", "/robots.txt", "/sitemap.xml"]

returns = check_paths(BASE_URL, lista_paths)
print("Rezultatul: ")
print(returns)

print("\n")
time.sleep(1)

def get_header(url: str, name: str, default: str = "lipseste") -> str:
    try:
        response = requests.get(url, headers ={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return response.headers.get(name, default)
    except requests.RequestException:
        return default

header_server = get_header(BASE_URL, name="Server")
print(f"Antet Server: {header_server}")

custom_head = get_header(ECHO_URL, name="X-Custom-Header")
print(f"Antet Custom: {custom_head}")

print("\n")
time.sleep(1)

def security_headers(url: str) -> dict[str, bool]:
    check_headers = ["Strict-Transport Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    results = {}

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        for header in check_headers:
            results[header] = header in response.headers
    except requests.RequestException:
        for header in check_headers:
            results[header] = False

    return results

security_status = security_headers(BASE_URL)
print("Verificarea antetelor de securitate: ")
for header, present in security_status.items():
    print(f"{header}: {present}")

print("\n")
time.sleep(1)

def score_headers(results: dict[str, bool]) -> str:
    score = sum(1 for present in results.values() if present)
    total = len(results)
    return f"{score}/{total}"

scor_final = score_headers(security_headers(BASE_URL))
print(f"Scorul antetelor de securitate pentru {BASE_URL} este: {scor_final}")

print("\n")
time.sleep(1)

def fetch_robots(base: str) -> str | None:
    try:
        url = base.rstrip("/") + "/robots.txt"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: str | None) -> list[str]:
    if robots_text is None:
        return []

    disallowed = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                if path:
                    disallowed.append(path)

    return disallowed

robots_content = fetch_robots(BASE_URL)
restricted = disallowed_paths(robots_content)

print(f"Caile disallowed sunt: ")
print(restricted)

print("\n")

print("Test cu valoarea None: ", disallowed_paths(None))

print("\n")
time.sleep(1)

def response_times(*urls: str) -> dict[str, float | None]:
    results = {}

    for url in urls:
        timp_start = time.perf_counter()
        try:
            requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            timp_end = time.perf_counter()
            results[url] = round(timp_end - timp_start, 3)
        except requests.RequestException:
            results[url] = None

    return results

url_slow = ECHO_URL + "/delay/1"

timings = response_times(BASE_URL, url_slow)
print("Timpul de raspuns masurat: ")
for url, seconds in timings.items():
    print(f"{url}: {seconds} secunde")

print("\n")
time.sleep(1)

def log(message: str, **details) -> None:
    parts = [message]
    for key, value in details.items():
        parts.append(f"{key}={value}")

    print(" | ".join(parts))

log("Verificat", url=BASE_URL, status=200)