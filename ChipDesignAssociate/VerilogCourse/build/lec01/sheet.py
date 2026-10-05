"""sheet.py <out.png> <img names...> — stack rendered panels into one review sheet."""
import sys, os
from PIL import Image
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
out, names = sys.argv[1], sys.argv[2:]
ims = [Image.open(os.path.join(IMG, n + ".png")) for n in names]
W = 1100
sc = [im.resize((W, int(im.height * W / im.width))) for im in ims]
H = sum(i.height + 10 for i in sc)
sheet = Image.new("RGB", (W, H), "white")
y = 0
for i in sc:
    sheet.paste(i, (0, y)); y += i.height + 10
sheet.save(out)
print(out, sheet.size)
