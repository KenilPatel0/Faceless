import json, math, subprocess, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from longdata import SCENES
W,H,FPS=1920,1080,24
for _fp in ["fonts/InterDisplay-Bold.otf", os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"), "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"]:
    if os.path.exists(_fp): FB=_fp; break
else: FB="fonts/InterDisplay-Bold.otf"
@lru_cache(None)
def F(s): return ImageFont.truetype(FB,max(int(s),1))
WHITE=(255,255,255); DIM=(185,192,225); RED=(255,70,90); CY=(70,220,255); YEL=(255,205,70); GRN=(90,235,150); PUR=(150,110,255)
ACC={"G":GRN,"R":RED,"Y":YEL,"C":CY,"P":PUR}
bg=Image.new("RGB",(W,H)); d=ImageDraw.Draw(bg)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=tuple(int((8,12,28)[i]+((30,16,70)[i]-(8,12,28)[i])*t) for i in range(3)))
for x in range(0,W,90): d.line([(x,0),(x,H)],fill=(22,28,58))
for y in range(0,H,90): d.line([(0,y),(W,y)],fill=(22,28,58))
DUM=ImageDraw.Draw(Image.new("RGB",(4,4)))
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def T(dr,xy,s,f,fill,a="mm",st=0): dr.text(xy,s,font=f,fill=fill,anchor=a,stroke_width=st,stroke_fill=(0,0,0))
def fit(s,size,maxw):
    while size>34 and DUM.textlength(s,font=F(size))>maxw: size-=2
    return F(size)

def wrap(s,font,maxw):
    out=[];cur=""
    for w in s.split():
        t=(cur+" "+w).strip()
        if DUM.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur); cur=w
    return out+[cur]

def draw_list(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); acc=ACC[sc["accent"]]; bs=sc["beats"]
    T(dr,(120,180),sc["heading"],F(78),acc,"lm"); dr.rectangle([120,240,560,246],fill=acc)
    items=[]
    for k,b in enumerate(bs[:bi+1]):
        if b[1]:
            for l in (b[1] if isinstance(b[1],list) else [b[1]]): items.append((l,k))
    for i,(l,k) in enumerate(items):
        y=350+i*115; cur=(k==bi); off=int((1-ease(tb/0.3))*70) if cur else 0
        dr.ellipse([120+off,y-13,146+off,y+13],fill=acc)
        T(dr,(180+off,y),l,fit(l,62,1100),WHITE if cur else DIM,"lm")
    cx,cy=1480,450; r=int(170*(0.9+0.1*ease(tb/0.3))); p=sc["panel"]
    if p=="good":
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(20,70,55),outline=GRN,width=10)
        dr.line([(cx-80,cy+5),(cx-20,cy+65),(cx+85,cy-60)],fill=GRN,width=28,joint="curve")
    elif p=="bad":
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(80,20,35),outline=RED,width=10)
        dr.line([(cx-70,cy-70),(cx+70,cy+70)],fill=RED,width=28); dr.line([(cx-70,cy+70),(cx+70,cy-70)],fill=RED,width=28)
    elif p=="change":
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(80,60,10),outline=YEL,width=10); T(dr,(cx,cy-5),"!",F(240),YEL)
    else:
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(30,22,70),outline=acc,width=10); T(dr,(cx,cy-5),str(bi+1),F(230),acc)
        if sc.get("prefix"): T(dr,(cx,cy+r+70),f"{sc['prefix']} {bi+1}",F(64),WHITE)
    side=None
    for b in bs[:bi+1]:
        if b[2]: side=b[2]
    if side:
        for j,ln in enumerate(wrap(side,F(58),760)): T(dr,(cx,cy+r+70+j*72),ln,F(58),WHITE)

def draw_hook(img,bi,tb):
    dr=ImageDraw.Draw(img)
    T(dr,(W/2,130),"Is Learning to Code Still Worth It",F(76),WHITE); T(dr,(W/2,218),"in the AI Era?",F(76),CY)
    def sl(k): return int((1-ease(tb/0.35))*120) if bi==k else 0
    if bi>=0:
        o=sl(0); dr.rounded_rectangle([200-o,320,1000-o,470],radius=40,fill=(90,25,45),outline=RED,width=6); T(dr,(600-o,395),"“Coding is dead”",F(64),WHITE)
    if bi>=1:
        o=sl(1); dr.rounded_rectangle([920+o,510,1720+o,660],radius=40,fill=(15,60,80),outline=CY,width=6); T(dr,(1320+o,585),"“Nothing has changed”",F(64),WHITE)
    if bi>=2:
        dr.rounded_rectangle([440,710,1480,820],radius=55,fill=(45,34,100),outline=PUR,width=6); T(dr,(960,765),"3 YEARS building apps + using AI daily",fit("3 YEARS building apps + using AI daily",50,960),WHITE)
    if bi>=3: T(dr,(W/2,885),"My honest take, and what I'd learn today",F(46),YEL)

def phone(dr,x,y):
    dr.rounded_rectangle([x,y,x+360,y+640],radius=50,fill=(14,18,40),outline=(120,130,180),width=6)
    T(dr,(x+180,y+90),"Welcome back",F(40),WHITE)
    dr.rounded_rectangle([x+35,y+150,x+325,y+215],radius=16,fill=(230,235,250),outline=RED,width=3); T(dr,(x+55,y+183),"kenil@mail",F(30),(60,60,90),"lm")
    T(dr,(x+35,y+240),"Enter a valid email",F(26),RED,"lm")
    dr.rounded_rectangle([x+35,y+280,x+325,y+345],radius=16,fill=(230,235,250)); T(dr,(x+55,y+313),"••••••••",F(30),(60,60,90),"lm")
    dr.rounded_rectangle([x+35,y+400,x+325,y+470],radius=35,fill=(60,120,255)); T(dr,(x+180,y+435),"Log in",F(38),WHITE)
    T(dr,(x+180,y+540),"Forgot password?",F(28),DIM)

def draw_example_a(img,bi,tb):
    dr=ImageDraw.Draw(img)
    T(dr,(120,180),"An example from my own work",F(72),CY,"lm"); dr.rectangle([120,240,560,246],fill=CY)
    T(dr,(120,310),"Feature: login screen with validation + API call",F(44),WHITE,"lm")
    phone(dr,1360+(int((1-ease(tb/0.4))*200) if bi==0 else 0),230)
    if bi>=1:
        g=ease(tb/0.9) if bi==1 else 1
        T(dr,(120,420),"BEFORE AI",F(46),RED,"lm"); dr.rounded_rectangle([120,460,120+max(30,int(900*g)),530],radius=18,fill=RED)
        if g>0.9: T(dr,(1040,495),"~3 hours",F(54),WHITE,"lm")
        T(dr,(120,575),"Layout • validation • errors • API • tests",F(38),DIM,"lm")
    if bi>=2:
        g=ease(tb/0.5) if bi==2 else 1
        T(dr,(120,665),"WITH AI",F(46),GRN,"lm"); dr.rounded_rectangle([120,705,120+max(30,int(100*g)),775],radius=18,fill=GRN)
        if g>0.9: T(dr,(260,740),"~20 minutes",F(54),WHITE,"lm")
        T(dr,(120,820),"Describe it  →  AI drafts  →  I review and fix",F(42),DIM,"lm")
    if bi>=3: T(dr,(120,900),"Time saved goes into real thinking",F(52),PUR,"lm")

def draw_example(img,bi,tb):
    if bi<4: return draw_example_a(img,bi,tb)
    dr=ImageDraw.Draw(img)
    T(dr,(120,180),"An example from my own work",F(72),CY,"lm"); dr.rectangle([120,240,560,246],fill=CY)
    phone(dr,1360,230); T(dr,(120,350),"What I still check",F(64),YEL,"lm")
    for i,l in enumerate(["Edge cases, like empty fields","Security and user data","I read every line"][:min(bi-3,3)]):
        y=470+i*120; off=int((1-ease(tb/0.3))*70) if i==bi-4 else 0
        dr.ellipse([120+off,y-13,146+off,y+13],fill=YEL); T(dr,(180+off,y),l,F(60),WHITE if i==bi-4 else DIM,"lm")
    if bi>=7: T(dr,(120,880),"Less typing. More judgment.",F(64),PUR,"lm")

def draw_verdict(img,bi,tb):
    dr=ImageDraw.Draw(img)
    if bi>=2:
        T(dr,(W/2,170),"TO RECAP",F(64),CY)
        for i,l in enumerate(["Learn the fundamentals","Build real projects, explain every line","Use AI as a tutor, not a crutch"]):
            y=400+i*170; dr.ellipse([300,y-45,390,y+45],fill=(30,22,70),outline=GRN,width=6); T(dr,(345,y),str(i+1),F(56),GRN)
            T(dr,(430,y),l,fit(l,64,1200),WHITE,"lm")
        return
    T(dr,(W/2,150),"THE VERDICT",F(60),CY)
    T(dr,(W/2,430),"YES",F(int(380*(0.85+0.15*ease(tb/0.4)))),GRN)
    T(dr,(W/2,690),"if you learn to think and to build",F(66),WHITE)
    if bi>=1:
        T(dr,(W/2,810),"AI makes average code cheap.",F(68),WHITE); T(dr,(W/2,900),"Good judgment is still expensive.",F(68),YEL)

def draw_intro(img,tb):
    dr=ImageDraw.Draw(img); s=ease(tb/0.5); r=int(130*s)
    dr.ellipse([W/2-r,330-r,W/2+r,330+r],fill=PUR); r2=max(r-16,1); dr.ellipse([W/2-r2,330-r2,W/2+r2,330+r2],fill=(20,14,50))
    T(dr,(W/2,330),"TXK",F(int(74*s)),WHITE); T(dr,(W/2,600),"TechXKenil",F(150),WHITE)
    if tb>1.0: T(dr,(W/2,720),"AI  •  TECH  •  CODE",F(52),CY)

def draw_outro(img,tb):
    dr=ImageDraw.Draw(img); T(dr,(W/2,330),"TechXKenil",F(150),WHITE); T(dr,(W/2,440),"AI  •  TECH  •  CODE",F(52),CY)
    if tb>0.7:
        s=ease((tb-0.7)/0.4)*(1+0.04*math.sin(tb*7)); w,h=int(760*s),int(180*s)
        dr.rounded_rectangle([W/2-w/2,680-h/2,W/2+w/2,680+h/2],radius=h//2,fill=(255,30,50))
        if s>0.8: T(dr,(W/2,680),"SUBSCRIBE",F(96),WHITE)

CF=F(40)
def captions(text,dur):
    words=text.split(); chunks=[];cur=[]
    for w in words:
        t=" ".join(cur+[w])
        if cur and (DUM.textlength(t.upper(),font=CF)>1400 or len(cur)>=9): chunks.append(cur); cur=[w]
        else: cur.append(w)
    chunks.append(cur); tot=sum(len(w) for w in words); tw=dur-0.2; res=[]; t=0
    for ch in chunks:
        L=sum(len(w) for w in ch)/tot*tw; res.append((t,t+L," ".join(ch))); t+=L
    return res

tl=json.load(open("tl.json"))
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","audio_long.wav",
 "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","techxkenil_long5.mp4"],stdin=subprocess.PIPE)
start=0.0
for sc,bd in zip(SCENES,tl):
    end=start+sum(bd); f0,f1=round(start*FPS),round(end*FPS)
    cum=[0]; [cum.append(cum[-1]+x) for x in bd]
    caps=[captions(b[0],bd[i]) for i,b in enumerate(sc["beats"])]
    for f in range(f0,f1):
        t=min(max(f/FPS-start,0),cum[-1]-1e-6); bi=max(i for i in range(len(bd)) if cum[i]<=t); tb=t-cum[bi]
        img=bg.copy(); k=sc["kind"]
        if k not in("intro","outro"): T(ImageDraw.Draw(img),(70,55),"TechXKenil",F(36),(160,170,210),"lm")
        if k=="list": draw_list(img,sc,bi,tb)
        elif k=="hook": draw_hook(img,bi,tb)
        elif k=="example": draw_example(img,bi,tb)
        elif k=="verdict": draw_verdict(img,bi,tb)
        elif k=="intro": draw_intro(img,tb)
        else: draw_outro(img,tb)
        for a,b,s in caps[bi]:
            if a<=tb<b+0.05: T(ImageDraw.Draw(img),(W/2,1010),s.upper(),CF,WHITE,"mm",5); break
        ff.stdin.write(img.tobytes())
    start=end
ff.stdin.close(); ff.wait(); print("done")
