import re
from PIL import Image
from PIL.ExifTags import TAGS

# B1
def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    else:
        return f"Error"

print("\n")
print(tip_real("probe/foto.jpg"))
print("\n")

# B2

date = open("probe/ascuns.png", "rb").read()

for strings in re.findall(rb"[ -~]{4,}", date):
    print(strings.decode('utf-8', errors='ignore')) # la rulare am gasit FLAG{ascuns_prin_carving}

print("\n")

# B3

exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

print("\n")

gps_info = exif.get(34853)
if gps_info:
    lat = gps_info.get(2)
    lat_ref = gps_info.get(1)
    lon = gps_info.get(4)
    lon_ref = gps_info.get(3)
    print("Latitudine: ", lat, lat_ref)
    print("Longitudine: ", lon, lon_ref)
else:
    print("Nu exista date GPS")

print("\n")

# B4

date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")

if i != 1:
    open("gasit.zip", "wb").write(date[i:])
    print("Arhiva extrasa de la octetul", i)
else:
    print("Nu s-a gasit nimic :c")

