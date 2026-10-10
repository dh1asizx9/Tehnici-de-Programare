# Laborator: functii, metode si importuri pe web
# Student: Agheorghesi Paul-Florian SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import re
from typing import Any
import requests
from requests import Response, RequestException
import csv
from datetime import datetime, timezone
from urllib.parse import urlparse
import socket
import ssl
import json

def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

def fetch(url, timeout=10):
    return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)

def get_status(url: str) -> int:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
    return response.status_code

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

def check_paths(base_url: str, paths: list[str]) -> list[dict]:
    results = []
    for path in paths:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
            status = response.status_code
        except requests.RequestException:
            status = "Error"

        results.append({"path": url, "status": status, "checked_at": datetime.now(timezone.utc).isoformat()})

    return results

def get_redirect_chain(url: str) -> list[str]:
    if url.startswith("https://"):
        http_url = url.replace("https://", "http://", 1)
    else:
        http_url = url

    try:
        res = requests.get(http_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        chain = [r.url for r in res.history] + [res.url]
        return chain
    except RequestException:
        return [url]

def get_robots_disallowed(base_url: str) -> list[str]:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}: //{parsed.netloc}/robots.txt"
    disallowed = []
    try:
        res = requests.get(robots_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if line.strip().lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path and path not in disallowed:
                        disallowed.append(path)
    except RequestException:
        pass

    return disallowed

def count_links(html: str, base_url: str) -> tuple[int, int]:
    parsed_base = urlparse(base_url)
    base_netloc = parsed_base.netloc

    hrefs = re.findall(r'href=["\'](.*?)["\']', html, re.IGNORECASE)
    internal = 0
    external = 0

    for href in hrefs:
        if href.startswith("http://") or href.startswith("https://"):
            parsed_href = urlparse(href)
            if parsed_href.netloc == base_netloc:
                internal += 1
            else:
                external += 1
        elif ( href.startswith("/") and not href.startswith("//") and not href.startswith("#")):
            internal += 1

    return internal, external

def site_report(url: str) -> dict:
    parsed = urlparse(url)
    hostname = parsed.netloc or parsed.path

    try:
        response = fetch(url)
        status_code = response.status_code
        final_url = response.url
        title = get_title(response.text)
        ip_addr = resolve(hostname)
        redirects = get_redirect_chain(url)

        sec_h = security_headers(response)
        max_sec = 4
        sec_score = f"{len(sec_h)} / {max_sec}"

        days_left = cert_days_left(hostname)
        internal_l, external_l = count_links(response.text, url)
        disallowed_paths = get_robots_disallowed(url)

        report_data = {"url": final_url, "status_code": status_code, "title": title, "ip_address": ip_addr, "redirects": redirects, "security_score": sec_score, "cert_days_left": days_left, "internal_links": internal_l, "external_links": external_l, "disallowed_paths": disallowed_paths, "generated_at": datetime.now(timezone.utc).isoformat()}

        filename = "report.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return report_data

    except Exception as e:
        print(f"Eroare: {e}")
        return {}




if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

