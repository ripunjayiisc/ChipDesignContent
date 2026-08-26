import sys
from PIL import Image
names = sys.argv[1:-1]; out = sys.argv[-1]
W = 1450; outs = []
for n in names:
    im = Image.open(f'/home/user/ChipDesignContent/ChipDesignAssociate/Module2/build/topic4/img/{n}.png'); r = W/im.width
    outs.append(im.convert('RGB').resize((W, int(im.height*r))))
c = Image.new('RGB', (W, sum(o.height for o in outs)+8*len(outs)), '#DDDDDD'); y = 0
for o in outs: c.paste(o, (0, y)); y += o.height+8
c.save(f'/home/user/ChipDesignContent/ChipDesignAssociate/Module2/build/topic4/img/{out}.png'); print(out, c.size)
