from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parent
im=Image.new('RGB',(1024,1024),'#f5efdf'); d=ImageDraw.Draw(im)
NAVY='#142d40'; RED='#b84d37'; BLUE='#abc7cd'; GOLD='#dbb359'; INK='#263e4a'
fontdir='/usr/share/fonts/truetype/dejavu/'
def font(n,b=False,i=False): return ImageFont.truetype(fontdir+('DejaVuSansMono-Oblique.ttf' if i else 'DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'),n)
def txt(x,y,s,n=12,b=False,c=INK): d.text((x,y),s,font=font(n,b),fill=c)
def wrap(s,w,n,b=False):
    f=font(n,b); lines=[]; line=''
    for word in s.split():
        candidate=(line+' '+word).strip()
        if f.getlength(candidate)>w:
            assert line,word
            lines.append(line); line=word
        else: line=candidate
    if line: lines.append(line)
    assert all(f.getlength(z)<=w for z in lines)
    return lines

def block(x,y,s,w,n=12,b=False,c=INK,step=None):
    for line in wrap(s,w,n,b):
        txt(x,y,line,n,b,c); y+=step or n+3
    return y

# Art is painted first, entirely from geometric primitives; all labels follow.
d.rectangle((0,0,1024,73),fill=NAVY)
d.rectangle((20,84,1004,141),fill='#ead38b')
boxes=[(20,155,395,409),(408,155,598,278),(611,155,801,278),(814,155,1004,278),(408,290,598,409),(611,290,801,409)]
for box in boxes: d.rectangle(box,fill='#e5e4d7',outline='#bcc3b9')
# 1: coastline and cyclone
x,y=20,155
d.rectangle((x+1,y+1,x+374,y+109),fill=BLUE)
d.polygon([(20,155),(145,155),(135,179),(156,196),(126,214),(145,239),(119,264),(20,264)],fill='#9fae85')
for k in range(4):
    pts=[]
    for j in range(180):
        a=j*.035+k*math.pi/2; r=3+j*.23
        pts.append((244+math.cos(a)*r,208+math.sin(a)*r))
    d.line(pts,fill='#f7f3e8',width=6)
d.ellipse((237,201,251,215),fill=NAVY)
# 2: cathedral, embassy flagpoles
for xx in [430,464,498]:
    d.rectangle((xx,185,xx+22,213),fill=NAVY)
    d.polygon([(xx-3,185),(xx+11,167),(xx+25,185)],fill='#617e86')
    d.line((xx+11,161,xx+11,172),fill=NAVY,width=2)
d.rectangle((425,208,531,217),fill=NAVY)
for xx,col in [(551,RED),(578,'#c47a46')]:
    d.line((xx,168,xx,218),fill=NAVY,width=2)
    d.rectangle((xx,169,xx+14,179),fill=col)
    d.rectangle((xx,172,xx+14,176),fill='#f5efdf')
# 3 Capitol
for xx in range(638,779,18): d.rectangle((xx,191,xx+7,215),fill='#e9efe5')
d.rectangle((630,215,786,220),fill=NAVY)
d.rectangle((637,185,780,192),fill=NAVY)
d.pieslice((679,160,739,205),180,360,fill=NAVY)
d.rectangle((704,157,714,177),fill=NAVY)
d.line((709,153,709,161),fill=NAVY,width=2)
# 4 summit
for xx,colors in [(836,['#b84d37','#f5efdf','#b84d37']),(889,['#b84d37']),(942,['#f5efdf','#6889a3','#b84d37'])]:
    d.line((xx,164,xx,209),fill=NAVY,width=2)
    for k,c in enumerate(colors): d.rectangle((xx,165+k*8/len(colors)*3,xx+31,165+(k+1)*24/len(colors)),fill=c)
d.polygon([(838,202),(974,202),(988,218),(824,218)],fill=NAVY)
# 5 justice
cx=503
d.line((cx,300,cx,346),fill=NAVY,width=5); d.line((466,311,540,311),fill=NAVY,width=3)
for xx in [472,534]:
    d.line((xx,311,xx-12,333),fill=NAVY,width=2);d.line((xx,311,xx+12,333),fill=NAVY,width=2)
    d.pieslice((xx-14,324,xx+14,342),0,180,fill=RED)
d.rectangle((480,346,526,351),fill=NAVY)
# 6 chart
d.line((629,301,629,348,783,348),fill=NAVY,width=2)
d.line([(638,342),(661,335),(683,339),(707,320),(730,325),(774,302)],fill=RED,width=5)
d.polygon([(774,302),(763,304),(773,315)],fill=RED)
# Map: deliberately explicit polygons and geographic dots, in local coordinates.
mx,my=814,290
d.rectangle((mx,my,1004,409),fill=BLUE)
polys=[[(10,19),(24,10),(51,12),(63,28),(48,41),(39,48),(26,39),(22,30)],[(42,48),(58,54),(62,67),(54,91),(44,76),(38,58)],[(82,27),(91,21),(100,27),(103,36),(91,40),(82,34)],[(85,42),(106,40),(113,54),(102,77),(91,67),(83,50)],[(101,23),(124,14),(157,23),(176,37),(158,46),(149,57),(132,49),(120,59),(112,43),(99,36)],[(149,72),(169,68),(178,81),(160,87),(148,80)]]
for p in polys: d.polygon([(mx+a,my+b) for a,b in p],fill='#a2ae89')
dots=[(121,49),(98,29),(43,32),(148,45),(86,36),(23,29)]
def inside(point,poly):
    x,y=point; yes=False
    for j in range(len(poly)):
        a,b=poly[j],poly[j-1]
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: yes=not yes
    return yes
for point,land in zip(dots,[4,2,0,4,2,0]): assert inside(point,polys[land]),(point,land)
# Overlay every label after scene construction.
txt(20,7,'FRIDAY 20 NOVEMBER 2026',19,True,'#f5efdf')
txt(20,29,'THE WORLD TODAY',36,True,'#f5efdf')
txt(799,21,'32 STORIES',18,True,'#ead38b');txt(799,44,'6 CONTINENTS',14,True,'#ead38b')
note="dear judge, today is world children's day, so i made you this little newspaper with my own hands. i read all the news and drew every picture myself. please take care of it. — a kid who read the news today"
ny=89
for line in wrap(note,650,13):
    d.text((32,ny),line,font=font(13,i=True),fill=NAVY); ny+=15
# lead
texty=270
txty=block(30,texty,'1  AKVAN MAKES LANDFALL',355,19,True)
txty=block(30,txty+3,'Severe cyclone crosses near Gopalpur around noon today: winds 90–100 km/h, gusting to 110.',355,13)
txty=block(30,txty+3,'300,000+ evacuated • 423 rescue teams • 69 trains cancelled. Red alerts: Odisha & north Andhra Pradesh.',355,12)
block(30,392,'IMD / Jagran Josh / Daily Jagran',355,10)
small=[
('2  KYIV: 98 DRONES','1 dead, 5 hurt; hits in 18 places. Austrian & Dutch embassies and St Volodymyr’s Cathedral damaged.','AFP / Euronews / Kyiv24'),
('3  IRAN WAR-POWERS VOTE','Senate rejects 51–48. Three Republicans for; one Democrat against. First test since midterms.','Reuters / Washington Post'),
('4  SHENZHEN SUMMIT','Four-point pledge: nuclear war “cannot be won and must never be fought.” No arms limits, Ukraine deal or timetable.','Wall Street Journal / Fast Company / AP'),
('5  ICJ: MYANMAR GENOCIDE','State responsible for Rohingya genocide in 2017; first state ruling under Genocide Convention.','Amnesty / UN / NPR'),
('6  ANTHROPIC’S RECORD IPO','$83/share; ~$1.5tn value, largest debut ever. ANT starts trading on Nasdaq.','Reuters / Financial Times / AP')]
for idx,(title,body,source) in enumerate(small):
    x,y,_,bottom=boxes[idx+1]; start=221 if idx<3 else 351
    z=block(x+7,start,title,176,10,True,step=11)
    z=block(x+7,z+1,body,176,8,step=9)
    block(x+7,bottom-10,source,176,7)
for i,(a,b) in enumerate(dots,1):
    d.ellipse((mx+a-4,my+b-4,mx+a+4,my+b+4),fill=RED)
    txt(mx+a-3,my+b-5,str(i),8,True,'white')
txt(821,386,'SIX STORIES / ONE WORLD',10,True)
headlines=[
('US intel: Iran still holds 2,500+ missiles after nine months of war','Wall Street Journal'),
('ADNOC tanker attacked in Strait of Hormuz; one crewman missing','press reports'),
('US and Venezuela agree to restore military cooperation','US Defence Secretary'),
("Brazil Senate passes Lula fiscal package; BofA sees path for capital to return",'Reuters'),
("Lula courts rare-earth investors; US share of Brazil trade down to 9.2%",'CounterPunch'),
('Lula in no hurry to name his next cabinet','Reuters'),
('Trump: Putin wants Ukraine war to end; Putin: no talks after Crimean Bridge strikes','Bloomberg'),
('Ukrainian attack on Crimean Bridge disrupts rail traffic','press reports'),
('Sudan: drone strafes South Kordofan gold mine, killing 10','Radio Dabanga'),
('LPG tanker sunk off Bulgaria was hit by projectiles, officials say','press reports'),
('Spain general strike: police clash with crowds','19 Nov'),
('French protests swell as unions join strikes','19 Nov'),
('Deutsche Bank handled $582m in Epstein-linked transactions, 2013–18','Financial Times • 19 Nov'),
('Somalia accuses UAE of secret military bases','19 Nov'),
('North Korea expanding uranium enrichment at Yongbyon, UN watchdog says','IAEA'),
('South Korea top court overturns ex-PM Han Duck-soo conviction in 2024 martial law case','press reports'),
('Japan PM Takaichi calls for continued dialogue with China','press reports'),
('Pakistan minister leads delegation to Delhi for SCO forum','press reports'),
('Modi meets Prince and Princess of Wales in Delhi','The Hindu'),
("Modi inaugurates FICCI centenary convention",'press reports'),
('Australia sanctions Israeli settlers: three people, four groups','Reuters'),
('India and Japan set to review defence ties','press reports'),
("Fire at ancestral home of Bangladesh’s Muhammad Yunus",'press reports'),
('Fiji declares nationwide disaster as El Niño drought reaches crisis; Tonga emergency too','Reuters'),
('India v NZ, 1st Test: Nicholls 113 not out; NZ 243/5 on day one in Wellington','press reports'),
('Sensex gains 1.21%; Nifty 1.14% on Thursday','press reports')]
assert len(headlines)==26
txt(20,422,'THE NEWS DESK',17,True);txt(695,426,'26 HEADLINES • SOURCES BELOW EACH',11,True)
for col,(lo,hi) in enumerate([(0,9),(9,18),(18,26)]):
    x=20+col*333; y=453
    if col: d.line((x-10,453,x-10,937),fill='#bac0b4')
    for j in range(lo,hi):
        title,src=headlines[j]
        y=block(x,y,title,310,12,True,step=15)
        y=block(x,y+2,src,310,10,c=RED,step=12)+9
    assert y<=945,(col,y)
d.rectangle((20,950,1004,1005),fill=NAVY)
txt(30,956,'MARKETS  |  Thu 19 Nov closes',12,True,'#ead38b')
txt(30,975,'S&P 500  7,175.83  −2.02%    •    FTSE 100  10,452.68  −0.93%    •    Brent  $92.27  +0.35%    •    Gold  $3,674.68  −1.36%',12,False,'#f5efdf')
txt(30,992,'Yahoo Finance / Armstrong Economics / Weekend Spread',8,False,'#f5efdf')
txt(20,1009,'20 NOV 2026  /  WORLD CHILDREN’S DAY EDITION',8,True)
im.save(ROOT/'entry.png',optimize=True)
print('PNG bytes:',(ROOT/'entry.png').stat().st_size)
