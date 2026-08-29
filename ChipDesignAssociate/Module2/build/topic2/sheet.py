import sys
from PIL import Image
out = sys.argv[1]; names = sys.argv[2:]
W = 1180
sc = []
for n in names:
    im = Image.open("img/%s.png" % n)
    sc.append(im.resize((W, int(im.height * W / im.width)), Image.LANCZOS))
gap = 30
H = sum(i.height for i in sc) + gap * (len(sc) - 1)
o = Image.new("RGB", (W, H), "white"); y = 0
for i in sc:
    o.paste(i, (0, y)); y += i.height + gap
o.save(out); print(o.size)
