from PIL import Image

# B5

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
bit_idx = 0

for p in px:
    r, g, b = p

    if bit_idx < len(biti):
        r = (r & ~1) | int(biti[bit_idx])
        bit_idx += 1

    if bit_idx < len(biti):
        g = (g & ~1) | int(biti[bit_idx])
        bit_idx +=1

    if bit_idx < len(biti):
        b = (b & ~1) | int(biti[bit_idx])
        bit_idx += 1

    px_nou.append((r,g,b))

px_nou.extend(px[len(px_nou):])

img.putdata(px_nou)
img.save("stego.png")
print("Mesaj ascuns")

# B5

px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r,g,b) in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

octeti = bytearray()
for i in range(0, len(biti), 8):
    octet = int(biti[i:i+8], 2)
    if octet == 0:
        break
    octeti.append(octet)

mesaj_extras = octeti.decode('utf-8', errors="ignore")
print("Mesajul extras: ", mesaj_extras)