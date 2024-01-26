import pygame as pg
import random2 as rn
pg.init()


#color
c1=250
c2=250
c3=250

c1_c=1
c2_c=2
c3_c=3
color=(c1,c2,c3)
black=(0,0,0)
white=(255,255,255)

crashed=False
start=False
pause=False

#display
a=1000
b=800

d=pg.display.set_mode((a,b))


#display text
def text_objects(text, font):
    textsurface=font.render(text ,True ,white)
    return textsurface, textsurface.get_rect()

def message_display(text,h,k,size):
    largetext=pg.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect=text_objects(text, largetext)
    TextRect.center=(h,k)
    d.blit(TextSurf, TextRect)

#image load
img1=pg.image.load('plane3.png')
img2=pg.image.load('space.jpg')
img3=pg.image.load('alien.png')

#plane coordinates
x=450 
y=600

q=0
w=0

x1=100
y1=100

#groups

targets=[]
bullets=[]
bullet=0
bulletspeed=8

target=0
targetspeed=2

laserfuel=50
laserfuelcapacity=90

#continuity
i_space=0
i_left=0
i_right=0
i_up=0
i_down=0

b_break=0


#level
level=1
score=0

mode="bullet"
inputmode="keyboard"
health=4
gamespeed0=100
gamespeed=99



####### start screen ############

while start==False:
    d.fill(black)
    ######## rgb engine ####

    c1+=c1_c
    c2+=c2_c
    c3+=c3_c
    if c1>=255:
        c1_c=-1
        c1=255
    if c2>=255:
        c2_c=-2
        c2=255
    if c3>=255:
        c3_c=-3
        c3=255
    if c1<=100:
        c1_c=1
        c1=100
    if c2<=100:
        c2_c=2
        c2=100
    if c3<=100:
        c3_c=3
        c3=100
    color=(c1,c2,c3)

    pg.draw.polygon(d,color,((300,100),(700,100),(700,250),(300,250)),0)

    message_display("START",500,175,100)

    for event in pg.event.get():
        if event.type==pg.MOUSEBUTTONDOWN:
            m1=pg.mouse.get_pos()[0]
            m2=pg.mouse.get_pos()[1]

            if (m1 in range(300,700)) and (m2 in range(100,250)):
                start=True
        if event.type==pg.QUIT:
            start=True
            pg.quit()
            quit()

    pg.display.update()



######################################                main engine                   #######################################

while crashed==False:
    
    d.blit(img2,(0,0))
    d.blit(img1,(x,y))
    pg.draw.polygon(d,black,((a-100,0),(a,0),(a,b),(a-100,b)),0)
    target=0
    bullet=0


    #### menu ####

    pg.draw.polygon(d,color,((a-90,50),(a-10,50),(a-10,130),(a-90,130)),3)
    pg.draw.polygon(d,color,((a-70,55),(a-65,55),(a-65,125),(a-70,125)),0)
    pg.draw.polygon(d,color,((a-30,55),(a-35,55),(a-35,125),(a-30,125)),0)

    message_display("Laser Fuel",a-50,150,15)
    pg.draw.polygon(d,color,((a-95,160),(a-95+int(laserfuel),160),(a-95+int(laserfuel),170),(a-95,170)),0)
    pg.draw.polygon(d,white,((a-95,160),(a-5,160),(a-5,170),(a-95,170)),1)

    

    


    #### level engine ####

    level=int(score/(10))
    l_str="Level "+str(level)
    
    message_display(l_str,a-50,30,25)
    
    health=4+int(level/5)
    
    health_decrease=int(60/health)
    targetspeed=2+int(level/4)
    gamespeed=99-level

    ############bullet engine#############

    
    nb=len(bullets)

    
    while nb>bullet:
        
        bullets[bullet][1]-=bulletspeed
        b1=bullets[bullet][0]
        b2=bullets[bullet][1]
        pg.draw.circle(d,white,(b1,b2),4)
        
        if b2<0:
            bullets.remove(bullets[bullet])
            bullet-=1

        bullet+=1
        nb=len(bullets)


    if i_space==1 and mode=="laser" and laserfuel>0:
        pg.draw.polygon(d,color,((x+47,0),(x+53,0),(x+53,y),(x+47,y)),0)
        laserfuel-=0.3



    ##############enemy engine###########

    #display enemy
        
    ne=len(targets)

    while ne>target:
        
        targets[target][1]+=1
        t1=targets[target][0]
        t2=targets[target][1]
        t3=targets[target][2]
        t4=targets[target][3]
        t5=targets[target][4]

        
        
        if t3==1:

            if t4==0:
                targets[target][0]-=1
            elif t4==1:
                targets[target][0]+=1

                
            if t1+160>=a:
                targets[target][3]=0
                
                
            elif t1<=0:
                targets[target][3]=1

            

        d.blit(img3,(t1,t2))
        pg.draw.polygon(d,(255,0,0),((t1,t2),(60+t1,t2),(60+t1,t2+8),(t1,t2+8)))
        pg.draw.polygon(d,(0,255,0),((t1,t2),(t5*health_decrease+t1,t2),(t5*health_decrease+t1,t2+8),(t1,t2+8)))
        
        
        if t2>b:
            targets.remove(targets[target])
            
        target+=1
        ne=len(targets)

    pg.display.update()


    #generate enemy

    ne=len(targets)

    gamespeed0+=1
    

    if ne<9+level and gamespeed0>gamespeed:

        
        t1=rn.randint(0,a-160)
        t2=0
        t3=rn.randint(0,1)
        t4=rn.randint(0,1)
        t5=health
        gamespeed0=0

        targets.append([t1,t2,t3,t4,t5])
        ne=len(targets)


    ########### crash engine #####

    ne=len(targets)
    target=0

    while ne>target and crashed==False:

        if (targets[target][0] in range(x-30,x+80)) and (targets[target][1] in range(y-30,y+80)):
            crashed=True
            pg.draw.circle(d,(255,255,0),(targets[target][0]+45,targets[target][1]+45),30)
            message_display("CRASHED",a/2,b/2,150)
            pg.display.update()

        target+=1
            
            

        
    
    
    ##########   kill engine   #####

    
    ne=len(targets)
    target=0
    
    while ne>target:
        
        if mode=="laser":
            if (targets[target][0] in range(x-12,x+54)) and (targets[target][1] in range(0,y+5)) and i_space==1:
                targets.remove(targets[target])
                score+=1
                target-=1
                if laserfuel<laserfuelcapacity:
                    laserfuel+=3

        ne=len(targets)
        target+=1

    if mode=="bullet":
            
        bullet=0
        target=0
        ne=len(targets)
        nb=len(bullets)
        
        while target<ne:
                
            bullet=0
                
            while bullet<nb and target<ne:
                    
                if target<ne:
                    if (bullets[bullet][0] in range(targets[target][0],targets[target][0]+60)) and (bullets[bullet][1] in range(targets[target][1]+10,targets[target][1]+50)):
                        bullets.remove(bullets[bullet])
                        targets[target][4]-=1
                        if targets[target][4]==0:
                            targets.remove(targets[target])
                            score+=1
                            if laserfuel<laserfuelcapacity:
                                laserfuel+=5
                        bullet-=1

                bullet+=1
                nb=len(bullets)
                ne=len(targets)

            target+=1

        


       


    
    ########processing input##########

    ######continuity engine#######

    
    if i_space==1 and mode=="bullet":
        b_break+=1
        if b_break>=4:
            point=[x+50,y]
            bullets.append(point)
            b_break=0
        
    if i_left==1:
        q=-5
    if i_right==1:
        q=5
    if i_up==1:
        w=-5
    if i_down==1:
        w=5

    x+=q
    y+=w


    #input
        
    for event in pg.event.get():

        if event.type==pg.QUIT:
            crashed=True


        if inputmode=="keyboard":
        
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_LEFT:
                    q=-5
                    i_left=1

                if event.key==pg.K_RIGHT:
                    q=5
                    i_right=1

                if event.key==pg.K_UP:
                    w=-5
                    i_up=1

                if event.key==pg.K_DOWN:
                    w=5
                    i_down=1


        if inputmode=="keyboard" or inputmode=="mouse":

            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    i_space=1


                if event.key==pg.K_KP_ENTER:
                    if mode=="bullet":
                        mode="laser"
                    elif mode=="laser":
                        mode="bullet"


                if event.key==pg.K_LSHIFT:
                
                    if inputmode=="keyboard":
                        inputmode="mouse"
                    
                    elif inputmode=="mouse":
                        inputmode="keyboard"
                    mess=inputmode+" mode"
                    message_display(mess,a/2,b/2,100)
                    

            
            if event.type==pg.KEYUP:
                if event.key==pg.K_LEFT:
                    q=0
                    i_left=0
                elif event.key==pg.K_RIGHT:
                    q=0
                    i_right=0
                elif event.key==pg.K_UP:
                    w=0
                    i_up=0
                elif event.key==pg.K_DOWN:
                    w=0
                    i_down=0
                elif event.key==pg.K_SPACE:
                    i_space=0
                    b_break=0


        if inputmode=="mouse":

            m=pg.mouse.get_pos()

            x=m[0]
            y=m[1]

        
            


        x=x+q
        y=y+w

        if x>(a-100-x1) or x<0:
            if x>(a-100-x1):
                x=a-x1-100
            if x<0:
                x=0
        if y>(b-y1) or y<0:
            if y>(b-y1):
                y=b-y1
            if y<0:
                y=0


    x+=q
    y+=w

    if x>(a-100-x1) or x<0:
        if x>(a-100-x1):
            x=a-x1-100
        if x<0:
            x=0
    if y>(b-y1) or y<0:
        if y>(b-y1):
            y=b-y1
        if y<0:
            y=0
    

    ################################################################################

    

    pg.display.update()

    ######## rgb engine ####

    c1+=c1_c
    c2+=c2_c
    c3+=c3_c
    if c1>=255:
        c1_c=-1
        c1=255
    if c2>=255:
        c2_c=-2
        c2=255
    if c3>=255:
        c3_c=-3
        c3=255
    if c1<=100:
        c1_c=1
        c1=100
    if c2<=100:
        c2_c=2
        c2=100
    if c3<=100:
        c3_c=3
        c3=100
    color=(c1,c2,c3)


    ################# pause #####


pg.quit()
quit()



        

        
