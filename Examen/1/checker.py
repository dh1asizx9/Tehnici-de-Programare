import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""

    if "https://" in host and "/" in path: 
        return host + path
    elif "https://" in host:
        return host + "/" + path
    elif "/" in path:
        return "https://" + host + path
    else:
        return "https://" + host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""

    if "https://" in url:
        return True
    else:
        return False

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    return print(f"Status: {r.status_code}\n", f"Content-Type: {r.headers['Content-Type']}")


def check_site(*url):
    """Returnează un dicționar cu: status, content_type, length, server."""

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)

    return print(dict(r.status_code, r.headers["Content-Type"])) #r.headers["Content-Length"], r.headers["Content-Server"]))

def scan_sites(list):
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""

    for i in list:
        r = requests.get(list, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if r.status_code == 200:
            print(f"Site-uri cu status 200: {r}")
        else:
            print(f"Site-uri esuate: {i}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
