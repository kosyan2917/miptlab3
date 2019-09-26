from graph import *
#Анимация

dx = 0
dy = 0
def KeyPressed(event):
    global dx,dy
    dx=0
    dy=0
    if event.keycode== VK_UP:
        dx=0
        dy=-5
    elif event.keycode==VK_DOWN:
        dx=0
        dy=5
    elif event.keycode==VK_RIGHT:
        dx=5
        dy=0
    elif event.keycode==VK_LEFT:
        dx=-5
        dy=0
def update():
    global dx,dy
    for obj in animal:
        moveObjectBy(obj,dx,dy)



def ellipse (x,y,x1,y1,a):
    el = []
    for i in range(int(min(x1,x)) - int(a), int(max(x1,x)) + int(a), ++1):
        for j in range(int(min(y1,y)) - int(a), int(max(y1,y)) + int(a), ++1):
            if ((x-i)**2 + (y-j)**2)**0.5 + ((x1-i) ** 2 + (y1-j) **2) **0.5 <= a:
               el.append(point(i,j))
    return el
def ellipse1 (x,y,a,b,x1,y1): #функция для элипсов, наклоненных в правую сторону
    return ellipse(131*a+x1+x, 33*b+y1+y, 121*a+x1+x, 56*b+y1+y, ((131*a-121*a) **2 + (56*b-33*b) **2) **0.5 + 0.5)
def ellipse2 (x,y,a,b,x1,y1): #Функция для элипсов, наклоненных в левую сторону
    return ellipse(321*a+x1+x, 20*b+y1+y, 331*a+x1+x, 43*b+y1+y, ((321*a-331*a) **2 + (43*b-20*b) **2) **0.5 + 0.5)
def plant (a,x,b,y):
    brushColor(0, 102, 53)
    penColor(0, 102, 53)
    penSize(2)
    #Далее ветки
    polyline([(119*a+x,27*b+y),(152*a+x,30*b+y),(174*a+x,37*b+y),(199*a+x,49*b+y),(213*a+x, 58*b+y),(229*a+x,71*b+y)])
    polyline([(274*a+x,57*b+y),(286*a+x,41*b+y),(304*a+x,26*b+y),(326*a+x,14*b+y),(342*a+x,7*b+y),(362*a+x,4*b+y),(376*a+x,2*b+y)])
    polyline([(270*a+x,113*b+y),(274*a+x,103*b+y),(280*a+x,96*b+y),(287*a+x,88*b+y),(297*a+x,80*b+y),(305*a+x,76*b+y),(314*a+x,76*b+y),(321*a+x,75*b+y),(329*a+x,78*b+y),(333*a+x,79*b+y)])
    polyline([(170*a+x,105*b+y),(178*a+x,102*b+y),(187*a+x,100*b+y),(194*a+x,100*b+y),(203*a+x,102*b+y),(210*a+x,105*b+y),(220*a+x,110*b+y),(228*a+x,117*b+y),(234*a+x,123*b+y),(245*a+x,139*b+y)])
    #Далее ствол
    polygon([(254*a+x,53*b+y),(269*a+x,4*b+y),(275*a+x,7*b+y),(260*a+x,56*b+y)])
    polygon([(244*a+x,94*b+y),(256*a+x,60*b+y),(266*a+x,64*b+y),(254*a+x,98*b+y)])
    rectangle(247*a+x,105*b+y,263*a+x,165*b+y)
    rectangle(247*a+x,225*b+y,263*a+x,173*b+y)
    #Далее листья накл. вправо
    ellipse1(0,-3*b,a,b,x,y)
    ellipse1(11*a,-2*b,a,b,x,y)
    ellipse1(21*a, 0,a,b,x,y)
    ellipse1(33*a,5*b,a,b,x,y)
    ellipse1(51*a,11*b,a,b,x,y)
    ellipse1(50*a,71*b,a,b,x,y)
    ellipse1(65*a,71*b,a,b,x,y)
    ellipse1(81*a,78*b,a,b,x,y)
    #Далее листья накл. влево
    ellipse2(0,0, a, b,x,y)
    ellipse2(15*a,-10*b,a,b,x,y)
    ellipse2(24*a,-13*b,a,b,x,y)
    ellipse2(34*a,-15*b,a,b,x,y)
    ellipse2(44*a,-16*b,a,b,x,y)
    ellipse2(1*a,56*b,a,b,x,y)
    ellipse2(-13*a,56*b,a,b,x,y)
    ellipse2(-26*a,64*b,a,b,x,y)
def panda (r=1,x=0,y=0):
    pand =[]
    brushColor("white")
    penColor("White")
    pand.append(polygon([(318/r+x,122/r+y),(328/r+x,125/r+y),(339/r+x,133/r+y),(358/r+x,171/r+y),(358/r+x,196/r+y),(356/r+x,200/r+y),(332/r+x,220/r+y),(301/r+x,220/r+y),(285/r+x,209/r+y),(281/r+x,201/r+y),(280/r+x,195/r+y),(278/r+x,157/r+y),(304/r+x,128/r+y),(316/r+x,122/r+y),(318/r+x,122/r+y)]))
    points = ellipse(402/r+x,184/r+y,296/r+x,184/r+y,130/r)
    for i in points:
        pand.append(i)
    brushColor("black")
    penColor("black")
    pand.append(polygon([(276/r+x,158/r+y),(271/r+x,154/r+y),(270/r+x,148/r+y),(272/r+x,138/r+y),(278/r+x,130/r+y),(291/r+x,121/r+y),(300/r+x,123/r+y),(304/r+x,127/r+y),(303/r+x,131/r+y),(276/r+x,158/r+y)]))
    pand.append(polygon([(340/r+x,133/r+y),(346/r+x,131/r+y),(353/r+x,133/r+y),(361/r+x,142/r+y),(363/r+x,146/r+y),(364/r+x,149/r+y),(364/r+x,225/r+y),(358/r+x,266/r+y),(335/r+x,288/r+y),(327/r+x,290/r+y),(312/r+x,286/r+y),(304/r+x,277/r+y),(304/r+x,269/r+y),(312/r+x,258/r+y),(322/r+x,249/r+y),(336/r+x,214/r+y),(351/r+x,206/r+y),(359/r+x,198/r+y),(359/r+x,169/r+y),(354/r+x,172/r+y),(350/r+x,168/r+y),(340/r+x,133/r+y)]))
    points = ellipse(318/r+x,192/r+y,318/r+x,192/r+y,25/r)
    for i in points:
        pand.append(i)
    pand.append(polygon([(286/r+x,173/r+y),(291/r+x,175/r+y),(293/r+x,178/r+y),(294/r+x,185/r+y),(292/r+x,194/r+y),(290/r+x,197/r+y),(286/r+x,197/r+y),(282/r+x,196/r+y),(279/r+x,192/r+y),(278/r+x,187/r+y),(278/r+x,183/r+y),(281/r+x,175/r+y),(286/r+x,173/r+y)]))
    pand.append(polygon([(278/r+x,191/r+y),(272/r+x,230/r+y),(274/r+x,244/r+y),(276/r+x,256/r+y),(299/r+x,271/r+y),(319/r+x,243/r+y),(318/r+x,220/r+y),(300/r+x,221/r+y),(299/r+x,219/r+y),(301/r+x,216/r+y),(301/r+x,213/r+y),(297/r+x,209/r+y),(291/r+x,208/r+y),(285/r+x,209/r+y),(281/r+x,202/r+y),(278/r+x,191/r+y)]))
    pand.append(polygon([(404/r+x,187/r+y),(409/r+x,191/r+y),(411/r+x,201/r+y),(411/r+x,219/r+y),(407/r+x,239/r+y),(398/r+x,256/r+y),(379/r+x,275/r+y),(368/r+x,273/r+y),(353/r+x,263/r+y),(362/r+x,235/r+y),(382/r+x,206/r+y),(397/r+x,190/r+y),(404/r+x,187/r+y)]))
    return pand
brushColor(255, 175, 128) #Фон
rectangle(0,0, 500, 333)
global animal
animal = panda()
panda(4,150,200)
plant (1,0,1,0)
plant(0.322,89.7,0.707,71)
plant(0.35, 0,0.707, 60)
plant(0.35,350, 1, 0)
print(type(animal))
for obj in animal:
    print(type(obj))

onTimer(update,50)
onKey(KeyPressed)
run()
