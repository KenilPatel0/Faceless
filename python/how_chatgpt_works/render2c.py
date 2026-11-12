import json, math, subprocess, os, sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from longdata2 import SCENES
W,H,FPS=1920,1080,24
for _fp in [
    os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf"),
    "fonts/InterDisplay-Bold.otf",
    os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"),
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
]:
    if os.path.exists(_fp): FB=_fp; break
else: FB=os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf")
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
    cx,cy=1560,450; r=int(170*(0.9+0.1*ease(tb/0.3))); p=sc["panel"]
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
        for j,ln in enumerate(wrap(side,F(58),520)): T(dr,(cx,cy+r+70+j*72),ln,F(58),WHITE)

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

def head(dr,s,acc):
    T(dr,(120,180),s,F(78),acc,"lm"); dr.rectangle([120,240,560,246],fill=acc)
def pill(dr,box,fill,out,txt,size,col=WHITE):
    dr.rounded_rectangle(box,radius=(box[3]-box[1])//2,fill=fill,outline=out,width=5); T(dr,((box[0]+box[2])/2,(box[1]+box[3])/2),txt,fit(txt,size,box[2]-box[0]-50),col)

def draw_hook2(img,sc,bi,tb):
    dr=ImageDraw.Draw(img)
    T(dr,(W/2,190),"How AI Chatbots",F(112),WHITE); T(dr,(W/2,320),"Actually Work",F(112),CY)
    pill(dr,(760,400,1160,490),(45,34,100),PUR,"(NO MATH)",50,YEL)
    if bi>=1:
        for i,(s,at) in enumerate([("Is it thinking?",2.3),("Searching the internet?",3.3),("Understanding you?",4.3)]):
            if bi>1 or tb>at:
                cx=360+i*600; pill(dr,(cx-290,580,cx+290,700),(40,30,90),CY,s,44)
    if bi>=2: T(dr,(W/2,810),"Simpler, and a bit weirder, than you'd expect",F(58),YEL)
    if bi>=3: T(dr,(W/2,910),"How it works  •  Why it makes things up  •  How to use it",F(46),WHITE)

def draw_auto(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"Idea 1: It's autocomplete",YEL)
    if bi<=1:
        x,y=260,300
        dr.rounded_rectangle([x,y,x+560,y+620],radius=50,fill=(14,18,40),outline=(120,130,180),width=6)
        T(dr,(x+40,y+70),"I'm on my",F(54),WHITE,"lm")
        for i,(w,hl) in enumerate([("way",1),("phone",0),("own",0)]):
            cx=x+105+i*175; dr.rounded_rectangle([cx-75,y+130,cx+75,y+190],radius=18,fill=(60,120,255) if hl else (40,46,80)); T(dr,(cx,y+160),w,F(36),WHITE)
        for r in range(3):
            for c in range(9 if r<2 else 7):
                kx=x+40+c*53+(26 if r==2 else 0); ky=y+260+r*95; dr.rounded_rectangle([kx,ky,kx+44,ky+70],radius=10,fill=(48,54,90))
        if bi>=1:
            T(dr,(1000,470),"A chatbot is this idea,",F(72),WHITE,"lm"); T(dr,(1000,570),"scaled up enormously",F(72),CY,"lm")
    elif bi==2:
        for i,(n,t,at) in enumerate([("1","Predict the next piece",0.6),("2","Add it to the text",4.0),("3","Repeat",7.0)]):
            if tb>at:
                cx=380+i*580; dr.rounded_rectangle([cx-250,420,cx+250,640],radius=36,fill=(30,22,70),outline=YEL,width=6)
                T(dr,(cx,490),n,F(80),YEL); T(dr,(cx,590),t,fit(t,44,460),WHITE)
                if i>0: T(dr,(cx-290,530),"→",F(90),CY)
    else:
        pcs=["The best way to learn is"," by"," building"," small"," projects","."]
        n=min(len(pcs),1+int(tb/0.8)) if bi==3 else len(pcs); f=F(76)
        tot=sum(DUM.textlength(p,font=f) for p in pcs[:n]); x=W/2-tot/2
        for i,p in enumerate(pcs[:n]):
            T(dr,(x,480),p,f,CY if (i==n-1 and bi==3 and n>1) else WHITE,"lm"); x+=DUM.textlength(p,font=f)
        T(dr,(W/2,700),"Predict  →  add  →  repeat" if bi==3 else "Each new piece depends on everything before it",F(60),YEL)

def draw_probs(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"How it picks the next piece",CY)
    T(dr,(W-120,190),"Illustrative numbers",F(34),DIM,"rm")
    if bi>=3:
        a=F(84); s1="The capital of France is "; w1=DUM.textlength(s1,font=a); w2=DUM.textlength("Paris",font=a); x=W/2-(w1+w2)/2
        T(dr,(x,340),s1,a,WHITE,"lm"); T(dr,(x+w1,340),"Paris",a,CY,"lm")
    else: T(dr,(W/2,340),"The capital of France is  ____",F(84),WHITE)
    g=ease(tb/1.4) if bi==0 else 1
    for i,(w,p) in enumerate([("Paris",.92),("the",.03),("a",.02),("Lyon",.01),("known",.01)]):
        y=470+i*92; bw=max(14,int(1000*p*g)); hl=(i==0 and bi>=1)
        T(dr,(560,y),w,F(54),WHITE if hl or bi==0 else DIM,"rm"); dr.rounded_rectangle([600,y-30,600+bw,y+30],radius=14,fill=GRN if i==0 else PUR)
        T(dr,(620+bw,y),f"{int(p*100)}%",F(46),WHITE,"lm")
    if bi==2: T(dr,(W/2,950),"Pick one, with a little randomness",F(52),YEL)
    if bi>=3: T(dr,(W/2,950),"Add it to the text, then repeat",F(52),YEL)

TOK=["Straw","berries","taste","un","believ","ably","good"]
TCOL=[PUR,(255,120,160),GRN,CY,YEL,(255,150,80),(120,180,255)]
def chips(toks,f,pad=34,gap=18):
    ws=[DUM.textlength(t,font=f)+2*pad for t in toks]; x=W/2-(sum(ws)+gap*(len(toks)-1))/2; o=[]
    for w in ws: o.append((x,x+w)); x+=w+gap
    return o
def draw_tok(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"Idea 2: Tokens",GRN)
    if bi<3:
        T(dr,(W/2,340),"Strawberries taste unbelievably good",F(58),DIM)
        f=F(60); L=chips(TOK,f); n=int((tb-0.8)/0.4)+1 if bi==0 else 7
        for i in range(max(0,min(7,n))):
            dr.rounded_rectangle([L[i][0],505,L[i][1],615],radius=30,fill=TCOL[i]); T(dr,((L[i][0]+L[i][1])/2,560),TOK[i],f,(15,15,30))
        if bi>=1:
            T(dr,((L[6][0]+L[6][1])/2,665),"1 token",F(36),WHITE); T(dr,((L[3][0]+L[5][1])/2,665),"3 tokens: a rare, long word",F(36),WHITE)
            T(dr,(W/2,770),"7 tokens",F(70),YEL)
        if bi>=2: T(dr,(W/2,870),"Example split only. Real tokenizers differ.",F(40),DIM)
    else:
        T(dr,(W/2,330),"YOU SEE",F(52),CY); T(dr,(W/2,430),"s  t  r  a  w  b  e  r  r  y",F(84),WHITE)
        T(dr,(W/2,560),"AI SEES",F(52),YEL); f=F(80); ch=["str","aw","berry"]; L=chips(ch,f,40)
        for i,c in enumerate(ch):
            dr.rounded_rectangle([L[i][0],620,L[i][1],760],radius=34,fill=[PUR,(255,120,160),GRN][i]); T(dr,((L[i][0]+L[i][1])/2,690),c,f,(15,15,30))
        T(dr,(W/2,850),"3 chunks  ≠  10 letters",F(64),WHITE)
        if bi>=4: T(dr,(W/2,930),"A model reads text differently than you do",F(48),YEL)

def draw_params(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"Idea 3: Billions of dials",PUR); col=GRN if bi==2 else PUR
    for i in range(40):
        cx=260+(i%10)*155; cy=340+(i//10)*135; dr.ellipse([cx-50,cy-50,cx+50,cy+50],fill=(24,20,60),outline=col,width=5)
        a=math.radians((i*47)%360+(0 if bi==2 else 70*math.sin(tb*2.2+i)))
        dr.line([(cx,cy),(cx+38*math.cos(a),cy+38*math.sin(a))],fill=WHITE,width=7)
    T(dr,(W/2,900),["Billions of numbers, called parameters","Training = tuning the dials","Fixed while you chat"][min(bi,2)],F(62),YEL if bi<2 else GRN)

def page(dr,x,y,n,dim=False):
    dr.rounded_rectangle([x,y,x+230,y+300],radius=18,fill=(110,118,150) if dim else (230,235,250))
    T(dr,(x+115,y+60),f"Page {n}",F(42),(40,40,60) if not dim else (60,60,80))
    for k in range(5): dr.rectangle([x+30,y+120+k*30,x+200-(k%2)*50,y+130+k*30],fill=(150,158,190))
def draw_desk(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"Idea 5: The context window",YEL)
    X=lambda i:210+i*254
    if bi==0:
        for i in range(4):
            if tb>0.8+0.9*i: page(dr,X(i),400,i+1)
        T(dr,(W/2,830),"Everything is sent again with each message",F(54),WHITE)
    else:
        dr.rounded_rectangle([180,340,1740,740],radius=30,outline=YEL,width=6); T(dr,(960,300),"THE DESK  (context window)",F(44),YEL)
        if bi==1:
            for i in range(6): page(dr,X(i),400,i+1)
            T(dr,(W/2,830),"Only so many pages fit",F(56),WHITE)
        elif bi==2:
            for i in range(6): page(dr,X(i),400,i+3)
            g=ease(tb/1.6)
            for j in range(2): page(dr,60+j*70,int(120+g*500),j+1,True)
            T(dr,(W/2,830),"Pages 1 and 2 fell off. The model can't see them.",F(52),RED)
        else:
            for i in range(6): page(dr,X(i),400,i+3)
            dr.rounded_rectangle([1330,130,1760,250],radius=12,fill=(255,225,110)); T(dr,(1545,190),"Memory: saved notes",F(40),(60,50,10))
            T(dr,(W/2,830),"Extra machinery on top. The desk is still the desk.",F(52),WHITE)

def draw_hallu(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"Why it makes things up",RED)
    if bi<=1:
        dr.rounded_rectangle([160,320,900,700],radius=36,fill=(50,20,40),outline=RED,width=6); T(dr,(530,430),"Looks up facts",F(60),WHITE); T(dr,(530,500),"in a database",F(60),WHITE)
        dr.line([(430,570),(630,660)],fill=RED,width=20); dr.line([(430,660),(630,570)],fill=RED,width=20)
        dr.rounded_rectangle([1020,320,1760,700],radius=36,fill=(15,55,45),outline=GRN,width=6); T(dr,(1390,430),"Predicts the most",F(60),WHITE); T(dr,(1390,500),"plausible text",F(60),WHITE)
        dr.line([(1290,620),(1350,670),(1480,560)],fill=GRN,width=20,joint="curve")
        if bi==1: T(dr,(W/2,830),"Plausible and true usually match",F(58),YEL)
    else:
        pill(dr,(1260,270,1760,340),(80,20,35),RED,"MADE-UP EXAMPLE",34)
        dr.rounded_rectangle([1000,370,1760,470],radius=30,fill=(60,120,255)); T(dr,(1380,420),"Give me a source for that claim.",F(36),WHITE)
        dr.rounded_rectangle([160,500,1360,800],radius=30,fill=(30,34,70),outline=(120,130,180),width=4)
        for k,l in enumerate(["According to the 2019 study “Patterns in Everyday","Data” by Dr. A. Morgan, published in the Journal of","Applied Statistics, the effect was clearly confirmed."]): T(dr,(200,550+k*80),l,F(40),WHITE,"lm")
        if bi>=3: pill(dr,(360,840,1560,930),(80,20,35),RED,"HALLUCINATION: fluent, confident, wrong",44)
        if bi>=4: T(dr,(W/2,960),"Better at saying “I'm not sure”, but it still happens",F(40),YEL)

NEW={"hook2":draw_hook2,"auto":draw_auto,"probs":draw_probs,"tok":draw_tok,"params":draw_params,"desk":draw_desk,"hallu":draw_hallu}

def draw_ex(img,sc,bi,tb):
    dr=ImageDraw.Draw(img); head(dr,"A better way to ask",GRN)
    f=F(42)
    dr.rounded_rectangle([160,320,900,760],radius=36,fill=(50,20,40),outline=RED,width=6); pill(dr,(260,280,800,360),(80,20,35),RED,"WEAK PROMPT",38)
    T(dr,(530,520),"Tell me about the report.",F(52),WHITE)
    if bi>=1:
        dr.rounded_rectangle([1020,320,1760,760],radius=36,fill=(15,55,45),outline=GRN,width=6); pill(dr,(1120,280,1660,360),(10,60,40),GRN,"BETTER PROMPT",38)
        for j,ln in enumerate(wrap("Here's the report text: [paste]. Using only this text, list the 3 main risks. If it isn't in the text, say so.",f,640)): T(dr,(1060,430+j*62),ln,f,WHITE,"lm")
    if bi>=2: T(dr,(W/2,860),"Grounded in your text, with permission to say “I don't know”",F(48),YEL)
    if bi>=3: T(dr,(W/2,940),"A few extra seconds, far fewer guesses",F(48),WHITE)
NEW["ex"]=draw_ex

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

tl=json.load(open(os.path.join(SCRIPT_DIR, "tl2.json")))
audio_path = os.path.join(SCRIPT_DIR, "audio2.wav")
out_mp4 = os.path.join(SCRIPT_DIR, "techxkenil_long2.mp4")

ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",audio_path,
 "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out_mp4],stdin=subprocess.PIPE)
start=0.0
for sc,bd in zip(SCENES,tl):
    end=start+sum(bd); f0,f1=round(start*FPS),round(end*FPS)
    cum=[0]; [cum.append(cum[-1]+x) for x in bd]
    caps=[captions(b[0],bd[i]) for i,b in enumerate(sc["beats"])]
    for f in range(f0,f1):
        t=min(max(f/FPS-start,0),cum[-1]-1e-6); bi=max(i for i in range(len(bd)) if cum[i]<=t); tb=t-cum[bi]
        img=bg.copy(); k=sc["kind"]
        if k not in("intro","outro"): T(ImageDraw.Draw(img),(70,55),"TechXKenil",F(36),(160,170,210),"lm")
        if k in NEW: NEW[k](img,sc,bi,tb)
        elif k=="list": draw_list(img,sc,bi,tb)
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
