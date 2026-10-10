# Laborator: functii, metode si importuri pe web
# Student: Agheorghesi Paul-Florian SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import web_tools
from web_tools import get_title, security_headers, fetch, check_paths, site_report
# daca am avea in main.py o functie cu aceeasi functionalitate, functia locala ar rula si nu cea din web_tools.
import time
import argparse
import csv

time.sleep(1)
print("\n")
print(web_tools.get_title(web_tools.fetch(BASE_URL).text))
print("\n")
# autotestul ruleaza doar in webtools deoarece blocul de cod este prezent in fisierul webtools 
# pe langa asta, conditionalul pus verifica daca __name__ este de format string "__name__" cand este rulat local
# cand webtools e importat, __name__ schimba valoarea din "__name__" in "web_tools"; astfel conditionalul devine fals

def main():
    parser = argparse.ArgumentParser(description=("Unealta modulara de analiza web pentru extragerea titlului si a antentelor de securitate"))
    parser.add_argument("url", type=str, help="URL-ul complet al paginii web care va fi analizata")

    args = parser.parse_args()
    target_url = args.url

    data = site_report(target_url)

    print(f"Se verifica {target_url}")
    print("\n")

    try:
        response = fetch(target_url)
        title = get_title(response.text)
        sec_headers = security_headers(response)

        print(f" Titlul: {title}")
        print("\n")
        print(f" Antetele de securitate: {list(sec_headers.keys())}")
        for key, value in sec_headers.items():
            print (f"   {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

    paths_test = ["/", "/about", "/contact", "/not-found"]

    report_data = check_paths(target_url, paths_test)

    filename = "report.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["path", "status", "checked_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

    print("\n")
    print(f"Raportul a fost salvat in '{filename}'")
    print("\n") 

    print(f"=== Raport site: {target_url} ===")
    print("\n")
    if data:
        print(f"Cod de stare:   {data.get('status_code')}")
        print(f"Titlu:  {data.get('title')}")
        print(f"Adresa IP:  {data.get('ip_address')}")
        print("Redirectionari   " f"{' -> '.join(data.get('redirects', [target_url]))}")
        print(f"Scor securitate:    {data.get('security_score')}")
        print(f"Certificat: {data.get('cert_days_left')} de zile ramase") 
        print("Legaturi:    " f"{data.get('internal_links')} interne, {data.get('external_links')}" " externe") 
        print(f"Cai interzise:  {'. '.join(data.get('disallowed_paths', []))}") 
        print("\n")
        print("Salvat in report.json")
        print("========================================\n") 

if __name__ == "__main__":
    main()

print("\n")
