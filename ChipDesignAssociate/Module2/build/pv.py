import sys, glob
from PIL import Image
SP='/tmp/claude-0/-home-user/21001dbc-8f5e-5620-b4fb-6ca9041a22f9/scratchpad/pages'
a=int(sys.argv[1]); b=int(sys.argv[2]); out=sys.argv[3] if len(sys.argv)>3 else '/tmp/preview.png'
fs=[f'{SP}/p-{i:02d}.png' for i in range(a,b+1)]
ims=[Image.open(f).convert('RGB') for f in fs]
W=ims[0].width
c=Image.new('RGB',(W,sum(i.height+6 for i in ims)),'#999999');y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+6
c.save(out); print(out, c.size)
