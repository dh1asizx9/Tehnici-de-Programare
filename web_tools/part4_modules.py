# Laborator: functii, metode si importuri pe web
# Student: Agheorghesi Paul-Florian SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

from part1_imports import *
from part2_methods import *
from part3_functions import *
from urllib.parse import urlparse 
from urllib.parse import urljoin
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
from datetime import datetime, timezone
import ssl

print("\n")
time.sleep(1)

def analyze_url(url: str) -> None:
    parsed = urlparse(url)

    print(f"Analiza url-ului: {url}")
    print(f" Scheme: {parsed.scheme}")
    print(f" Netloc: {parsed.netloc}")
    print(f" Path: {parsed.path}")
    print(f" Query: {parsed.query}")
    print(f" Fragment: {parsed.fragment}")

target = "https://cybercor.org/path?x=1#top"
analyze_url(target)

print("\n")
time.sleep(1)

def comp_links(base: str, relative_paths: list[str]) -> dict[str, str]:
    resolved_links = {}
    for path in relative_paths:
        resolved_links[path] = urljoin(base, path)

    return resolved_links

paths = ["/about", "contact.html", "../index.html"]
results = comp_links(BASE_URL, paths)

print(f"Url-ul de baza: {BASE_URL}")
print("Legaturi: ")
for relative, absolute in results.items():
    print(f" '{relative}' --> {absolute}")

print("\n")
time.sleep(1)

def extract_links(html: str) -> list[str]:
    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))

sample = """
    <html>
        <body>
            <a href="https://test.com/about"> About </a>
            <a href="hhtps://test.com/contact"> Contact </a>
            <a href="https://test.com/about"> About </a>
            <a href="https://test.com/index.html"> Test </a>
        </body>
    </html>
"""


unice = extract_links(sample)
print("Legaturi unice: ")
for link in unice:
    print(f" {link}")

print("\n")
time.sleep(1)

def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    intern = []
    extern = []

    parsed_base = urlparse(domain)
    base_netloc = parsed_base.netloc or parsed_base.path

    for link in links:
        absolute = urljoin(domain, link)
        parsed_link = urlparse(absolute)
        if parsed_link.netloc == base_netloc:
            intern.append(absolute)
        else:
            extern.append(absolute)

    return list(dict.fromkeys(intern)) , list(dict.fromkeys(extern))

sample_links = ["/about", "https://google.com/search", "blog/index.html", "https://github.com", "https://cybercor.org/contact"]
internal_links, external_links = split_links(sample_links, BASE_URL)

print(f"Domeniul de referinta: {BASE_URL}")
print("Legaturi interne: ")
for link in internal_links:
    print(f" {link}")

print("\n")
print("Legaturi externe: ")
for link in external_links:
    print(f" {link}")

print("\n")
time.sleep(1)

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src_value = dict(attrs).get("src")
            if src_value:
                self.images.append(src_value)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print("Imagini gasite in test: ", finder.images)

print("\n")

assert finder.images == ["/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp", ], "Parserul nu a gasit exact imaginile asteptate"

print("Testul a trecut!")

print("\n")
time.sleep(1)

try:
    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
    finder = ImageFinder()
    finder.feed(response.text)
    print(f"{len(finder.images)} imagini gasite pe {BASE_URL}")
    for src in finder.images:
        print(f" {src}")

    html_lower = response.text.lower()
    tag_count = html_lower.count("<img")
    print(f"Verificare Numar de aparitii '<img' in html: {tag_count}")

except requests.RequestException as e:
    print(f"Eroare: {e}")

print("\n")
time.sleep(1)

def page_fingerprint(url: str) -> str | None:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        return hashlib.sha256(response.content).hexdigest()
    except requests.RequestException:
        return None

hash1 = page_fingerprint(BASE_URL)
hash2 = page_fingerprint(BASE_URL)

print(f"Prima amprenta: {hash1}")
print("\n")
print(f"A doua amprenta: {hash2}")
print("\n")

if hash1 == hash1 and hash1 == hash2:
    print("Amprentele sunt identice")
else:
    print("Amprentele sunt diferite, amprenta s-a modificat intre cereri")
# amprentele pot fi diferite cand ceva se modifica pe site; un counter sau o valoare ce tine de SEO

print("\n")
time.sleep(1)

def json_save(url: str, filename: str ="headers.json") -> None:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        headers_dict = dict(response.headers)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(headers_dict, file, indent=2)
        print(f"Antetele au fost salvate in '{filename}'")

        print("\n")

        with open(filename, "r", encoding="utf-8") as file:
            loaded_headers = json.load(file)

        content_type = loaded_headers.get("Content-Type", "Nu exista")
        print(f"Antetul 'Content-Type' incarcat din json: {content_type}")
    except requests.RequestException as e:
        print(f"Erroare: {e}")
    except IOError as e:
        print(f"Erroare: {e}")

json_save(BASE_URL)

print("\n")
time.sleep(1)

def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

domain = "cybercor.org"
ip_address = resolve(domain)
print(f"Interogarea pentru {domain} este: {ip_address}")

print("\n")
time.sleep(1)

def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sock:
            cert = sock.getpeercert()
            not_after_str = cert["notAfter"]
            expiry_seconds = ssl.cert_time_to_seconds(not_after_str)
            current_seconds = datetime.now(timezone.utc).timestamp()
            seconds_left = expiry_seconds - current_seconds
            days_left = int(seconds_left // 86400)

    return days_left

try:
    remaining_days = cert_days_left(domain)
    print(f"Certificatul SSL pentru {domain} expira in {remaining_days} zile")
except Exception as e:
    print(f"Eroare: {e}")