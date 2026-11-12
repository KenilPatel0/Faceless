import json, math, subprocess, re, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
meta=json.load(open("meta4.json"))
for _fp in ["fonts/InterDisplay-Bold.otf", os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"), "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"]:
    if os.path.exists(_fp): FB=_fp; break
else: FB="fonts/InterDisplay-Bold.otf"
def F(s): return ImageFont.truetype(FB,s)
BG1,BG2=(8,12,28),(30,16,70)
WHITE=(255,255,255); RED=(255,70,90); CY=(70,220,255); YEL=(255,205,70); GRN=(90,235,150); PUR=(150,110,255)

bg=Image.new("RGB",(W,H)); d=ImageDraw.Draw(bg)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(BG1[i]+(BG2[i]-BG1[i])*t) for i in range(3)))
for x in range(0,W,90): d.line([(x,0),(x,H)],fill=(255,255,255,0) if False else (22,28,58))
for y in range(0,H,90): d.line([(0,y),(W,y)],fill=(22,28,58))

def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def pop(x): 
    x=max(0,min(1,x)); return 1+0.15*math.sin(x*math.pi) if x<1 else 1
def ctext(dr,xy,txt,font,fill,anchor="mm",stroke=0,sf=(0,0,0)):
    dr.text(xy,txt,font=font,fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=sf)
def alpha_layer(img,fn,a):
    if a>=0.99: fn(ImageDraw.Draw(img)); return
    if a<=0.01: return
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); fn(ImageDraw.Draw(lay))
    lay.putalpha(lay.getchannel("A").point(lambda v:int(v*a)))
    img.paste(lay,(0,0),lay)

def word_letters(dr,word,cx,cy,size,colors,t_in=None):
    f=F(size); ws=[dr.textlength(c,font=f) for c in word]; sp=size*0.06
    tot=sum(ws)+sp*(len(word)-1); x=cx-tot/2
    for i,c in enumerate(word):
        dr.text((x,cy),c,font=f,fill=colors[i],anchor="lm"); x+=ws[i]+sp
    return tot

# ---------- scenes ----------
def sc_hook(img,t,dur):
    s=ease(t/0.4); size=int(112*(0.5+0.5*s)*pop(t/0.6))
    word="STRAWBERRY"; cols=[WHITE]*10
    for i,c in enumerate(word):
        if c=="R" and t>2.2+0.35*[2,7,8].index(i): cols[i]=RED
    def f(dr):
        word_letters(dr,word,W/2,760,size,cols)
        if t>0.8:
            ctext(dr,(W/2,520),"HOW MANY R's?",F(78),CY)
        if t>2.8:
            q=ease((t-2.8)/0.4); ctext(dr,(W/2,1060),"?",F(int(420*q*(1+0.05*math.sin(t*8)))),RED)
    alpha_layer(img,f,ease(t/0.25))

def sc_intro(img,t,dur):
    s=ease(t/0.5); 
    def f(dr):
        r=int(150*s*pop(t/0.8))
        dr.ellipse([W/2-r,720-r,W/2+r,720+r],fill=PUR)
        dr.ellipse([W/2-r+18,720-r+18,W/2+r-18,720+r-18],fill=(20,14,50))
        ctext(dr,(W/2,720),"TXK",F(int(84*s)),WHITE)
        a=ease((t-0.4)/0.5)
        ctext(dr,(W/2,1000),"TechXKenil",F(130),WHITE)
        if t>1.0: ctext(dr,(W/2,1120),"AI  •  TECH  •  CODE",F(48),CY)
    f(ImageDraw.Draw(img)) if False else alpha_layer(img,f,ease(t/0.3))

def sc_tokens(img,t,dur):
    def f(dr):
        ctext(dr,(W/2,430),"YOU SEE",F(56),CY)
        word_letters(dr,"s t r a w b e r r y".replace(" ",""),W/2,540,110,[WHITE]*10)
        if t>1.5:
            ctext(dr,(W/2,860),"AI SEES",F(56),YEL)
            chunks=["str","aw","berry"]; cols=[PUR,(255,120,160),GRN]
            fnt=F(130); ws=[dr.textlength(c,font=fnt)+70 for c in chunks]; tot=sum(ws)+40*2; x=W/2-tot/2
            for i,c in enumerate(chunks):
                a=ease((t-1.8-0.45*i)/0.3)
                if a>0:
                    h=int(110*a)
                    dr.rounded_rectangle([x,1010-h,x+ws[i],1010+h],radius=34,fill=cols[i])
                    if a>0.8: ctext(dr,(x+ws[i]/2,1010),c,fnt,(15,15,30))
                x+=ws[i]+40
        if t>dur-1.7:
            ctext(dr,(W/2,1260),"3 chunks  ≠  10 letters",F(70),WHITE)
        ctext(dr,(W/2,300),"TOKENS",F(100),YEL) if t>0.5 else None
    alpha_layer(img,f,ease(t/0.25))

def strawberry_card(sz=540):
    c=Image.new("RGB",(sz,sz),(250,236,225)); d=ImageDraw.Draw(c)
    cx,cy=sz/2,sz*0.58
    d.polygon([(cx-190,cy-90),(cx+190,cy-90),(cx+120,cy+190),(cx,cy+240),(cx-120,cy+190)],fill=(230,40,60))
    d.ellipse([cx-190,cy-170,cx+190,cy-10],fill=(230,40,60))
    for (dx,dy) in [(-100,-30),(0,-60),(100,-30),(-60,50),(60,50),(0,120),(-110,100),(110,100),(0,10)]:
        d.ellipse([cx+dx-9,cy+dy-14,cx+dx+9,cy+dy+14],fill=(255,225,120))
    for ang in range(-60,61,30):
        a=math.radians(ang); d.polygon([(cx,cy-150),(cx+int(110*math.sin(a))-20,cy-150-int(90*math.cos(a))),(cx+int(110*math.sin(a))+20,cy-150-int(60*math.cos(a)))],fill=(50,170,90))
    return c
CARD=strawberry_card(); PC={}
def sc_pixels(img,t,dur):
    prog=ease((t-0.8)/(dur-2.0))
    lvl=max(10,int(270-prog*258)); 
    key=lvl
    if key not in PC: PC[key]=CARD.resize((lvl,lvl),Image.BILINEAR).resize((CARD.width,CARD.width),Image.NEAREST)
    card=PC[key]; zoom=1+0.45*prog
    sz=int(CARD.width*zoom*ease(t/0.4)) or 2
    c2=card.resize((sz,sz),Image.NEAREST)
    mask=Image.new("L",(sz,sz),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,sz-1,sz-1],radius=40,fill=255)
    px=int(W/2-sz/2); py=int(820-sz/2)
    img.paste(c2,(px,py),mask)
    dr=ImageDraw.Draw(img)
    dr.rounded_rectangle([px-6,py-6,px+sz+6,py+sz+6],radius=44,outline=WHITE,width=6)
    ctext(dr,(W/2,360),"THUMBNAIL",F(86),YEL)
    if t>dur*0.6: ctext(dr,(W/2,1320),"Count the pixels?",F(74),CY)

def sc_spell(img,t,dur):
    word="STRAWBERRY"; n=int((t-0.2)/((dur*0.55)/10))+1; n=max(0,min(10,n))
    def f(dr):
        ctext(dr,(W/2,430),"STEP BY STEP",F(76),CY)
        fnt=F(120); step=92; x0=W/2-step*4.5; cnt=0
        for i,c in enumerate(word):
            if i<n:
                isr=(c=="R"); 
                if isr: cnt+=1
                col=RED if isr else WHITE
                x=x0+i*step
                dr.text((x,780),c,font=fnt,fill=col,anchor="mm")
                if isr:
                    dr.ellipse([x-30,880,x+30,940],fill=RED); ctext(dr,(x,910),str(cnt),F(44),WHITE)
        if n>=10 and t>dur*0.62: ctext(dr,(W/2,1120),"3 R's",F(180),GRN)
    alpha_layer(img,f,ease(t/0.25))

def sc_lesson(img,t,dur):
    def f(dr):
        ctext(dr,(W/2,520),"THE LESSON",F(72),YEL)
        if t>0.6: ctext(dr,(W/2,760),"Looks easy to you",F(84),WHITE)
        if t>dur*0.42: ctext(dr,(W/2,920),"≠",F(150),RED)
        if t>dur*0.55: ctext(dr,(W/2,1100),"how AI sees text",F(92),CY)
    alpha_layer(img,f,ease(t/0.25))

def sc_outro(img,t,dur):
    def f(dr):
        ctext(dr,(W/2,520),"TechXKenil",F(140),WHITE)
        ctext(dr,(W/2,640),"AI  •  TECH  •  CODE",F(48),CY)
        if t>0.7:
            s=ease((t-0.7)/0.4)*(1+0.04*math.sin(t*7)); w,h=int(640*s),int(170*s)
            dr.rounded_rectangle([W/2-w/2,900-h/2,W/2+w/2,900+h/2],radius=h//2,fill=(255,30,50))
            if s>0.8: ctext(dr,(W/2,900),"SUBSCRIBE",F(88),WHITE)
    alpha_layer(img,f,ease(t/0.25))

def arrow(dr,p,q,col,w=10):
    dr.line([p,q],fill=col,width=w); a=math.atan2(q[1]-p[1],q[0]-p[0]); L=34
    dr.polygon([q,(q[0]-L*math.cos(a-0.45),q[1]-L*math.sin(a-0.45)),(q[0]-L*math.cos(a+0.45),q[1]-L*math.sin(a+0.45))],fill=col)
def card(dr,box,fill,out,title,sub,tc):
    dr.rounded_rectangle(box,radius=50,fill=fill,outline=out,width=8)
    cx=(box[0]+box[2])/2; cy=(box[1]+box[3])/2
    ctext(dr,(cx,cy-35),title,F(110),tc); ctext(dr,(cx,cy+70),sub,F(56),WHITE)
def sc_hook4(img,t,dur):
    dr=ImageDraw.Draw(img)
    ctext(dr,(540,330),"What's the difference?",F(72),WHITE)
    if t>0.3: card(dr,(140,450,940,800),(15,60,80),CY,"CHATBOT","answers",CY)
    if t>1.0: ctext(dr,(540,900),"vs",F(80),YEL)
    if t>1.4: card(dr,(140,1000,940,1350),(50,28,100),PUR,"AGENT","acts",(190,160,255))
def sc_chat4(img,t,dur):
    dr=ImageDraw.Draw(img)
    ctext(dr,(540,430),"CHATBOT",F(70),CY); dr.rounded_rectangle([140,500,940,760],radius=44,fill=(15,60,80),outline=CY,width=6); ctext(dr,(540,630),"Here's your answer.",F(64),WHITE)
    if t>dur*0.45:
        ctext(dr,(540,930),"AGENT",F(70),(190,160,255)); dr.rounded_rectangle([140,1000,940,1260],radius=44,fill=(50,28,100),outline=PUR,width=6); ctext(dr,(540,1130),"Does the task.",F(64),WHITE)
def sc_trip4(img,t,dur):
    dr=ImageDraw.Draw(img)
    dr.rounded_rectangle([420,330,960,440],radius=40,fill=(60,120,255)); ctext(dr,(690,385),"Plan my trip",F(54),WHITE)
    if t>dur*0.12:
        dr.rounded_rectangle([120,480,820,620],radius=40,fill=(40,46,80)); ctext(dr,(470,550),"Here's a 3-day plan…",F(54),WHITE); ctext(dr,(540,690),"CHATBOT: a plan",F(48),CY)
    if t>dur*0.42:
        ctext(dr,(540,850),"AGENT: does it",F(56),(190,160,255))
        for i,(s,at) in enumerate([("Searches flights",0.45),("Compares prices",0.65),("Fills in the form",0.85)]):
            if t>dur*at:
                y=980+i*140; dr.rounded_rectangle([130,y-55,950,y+55],radius=30,fill=(50,28,100),outline=PUR,width=5)
                dr.ellipse([160,y-32,224,y+32],fill=GRN); dr.line([(176,y),(190,y+14),(212,y-14)],fill=(10,30,20),width=8)
                ctext(dr,(260,y),s,F(54),WHITE,"lm")
def sc_loop4(img,t,dur):
    dr=ImageDraw.Draw(img)
    dr.rounded_rectangle([200,330,880,450],radius=40,fill=(40,46,80)); ctext(dr,(540,390),"Chatbot: one answer, done",F(46),(190,196,225))
    nodes=[("Think",(540,740)),("Act",(820,1180)),("Observe",(260,1180))]; act=int(t*1.3)%3
    for i in range(3):
        p=nodes[i][1]; q=nodes[(i+1)%3][1]; dx,dy=q[0]-p[0],q[1]-p[1]; d=math.hypot(dx,dy); u=(dx/d,dy/d)
        arrow(dr,(p[0]+u[0]*135,p[1]+u[1]*135),(q[0]-u[0]*135,q[1]-u[1]*135),YEL if i==act else (110,116,150))
    for i,(n,c) in enumerate(nodes):
        on=(i==act); dr.ellipse([c[0]-115,c[1]-115,c[0]+115,c[1]+115],fill=PUR if on else (30,26,70),outline=WHITE if on else PUR,width=8); ctext(dr,c,n,F(54),WHITE)
    ctext(dr,(540,1010),"REPEAT",F(48),YEL)
    if t>dur*0.45:
        for i,s in enumerate(["Search","Browser","Code"]):
            cx=230+i*310; dr.rounded_rectangle([cx-125,1380,cx+125,1450],radius=35,fill=(15,60,80),outline=CY,width=4); ctext(dr,(cx,1415),s,F(44),CY)
def sc_same4(img,t,dur):
    dr=ImageDraw.Draw(img)
    for y,lab,col,fill,at in [(450,"CHATBOT",CY,(15,60,80),0.05),(850,"AGENT",(190,160,255),(50,28,100),0.3)]:
        if t>dur*at:
            dr.rounded_rectangle([140,y,940,y+300],radius=44,fill=fill,outline=col,width=7); ctext(dr,(540,y+70),lab,F(64),col)
            dr.rounded_rectangle([300,y+130,780,y+240],radius=30,fill=(30,26,70),outline=WHITE,width=4); ctext(dr,(540,y+185),"SAME MODEL",F(52),WHITE)
    if t>dur*0.55: ctext(dr,(540,1250),"+ LOOP  + TOOLS",F(84),YEL)
def sc_guard4(img,t,dur):
    dr=ImageDraw.Draw(img)
    ctext(dr,(540,360),"POWERFUL",F(100),GRN)
    if t>dur*0.3:
        dr.polygon([(540,500),(790,590),(765,900),(540,1120),(315,900),(290,590)],fill=(18,64,60),outline=GRN)
        dr.line([(430,820),(510,900),(660,720)],fill=GRN,width=30,joint="curve"); ctext(dr,(540,1230),"GUARDRAILS",F(88),WHITE)
    if t>dur*0.62: ctext(dr,(540,1350),"Real actions. Real mistakes.",F(54),RED)
SC={"intro":sc_intro,"outro":sc_outro,"hook4":sc_hook4,"chat4":sc_chat4,"trip4":sc_trip4,"loop4":sc_loop4,"same4":sc_same4,"guard4":sc_guard4}

def captions(text,dur):
    words=text.split(); chunks=[words[i:i+4] for i in range(0,len(words),4)]
    tot=sum(len(w) for w in words); tw=dur-0.25; res=[]; t=0
    for ch in chunks:
        L=sum(len(w) for w in ch)/tot*tw; res.append((t,t+L," ".join(ch))); t+=L
    return res
CAPF=F(66)
def draw_caption(img,t,caps):
    for a,b,s in caps:
        if a<=t<b+0.05:
            dr=ImageDraw.Draw(img); ctext(dr,(W/2,1560),s.upper(),CAPF,WHITE,stroke=8); return

ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","audio4.wav",
  "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","techxkenil_short4.mp4"],stdin=subprocess.PIPE)
for m in meta:
    n=int(round(m["dur"]*FPS)); caps=captions(m["text"],m["dur"])
    for i in range(n):
        t=i/FPS; img=bg.copy().convert("RGB")
        if m["name"] not in("intro","outro"):
            ctext(ImageDraw.Draw(img),(W/2,150),"TechXKenil",F(52),(160,170,210))
        SC[m["name"]](img,t,m["dur"]); draw_caption(img,t,caps)
        ff.stdin.write(img.tobytes())
ff.stdin.close(); ff.wait(); print("done")
