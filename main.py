import pygame,random,time,thread,sys
import cv2
import numpy as np
from pygame.locals import *
from Box import *

pygame.init()
pygame.mixer.init()

#colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BRED=(200,0,0)
GREEN=(0,200,0)
BLUE=(0,0,255)
LGREEN=(0,255,0)
YELLOW=(255,255,0)
LBLUE=(0,255,255)

controllerThread=False
FPS=60
WIDTH=800
HEIGHT=600
collides=False
pause=False
gameover=False
levelNo=1
red=[]
green=[]
brick=[]
levelChange=1
msg='CENTER'

gameDisplay=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('BRICKS')
clock=pygame.time.Clock()
startSound=pygame.mixer.Sound('hit.wav')

def OpenCVcontroller():
    cap = cv2.VideoCapture(0)
    
    REQUIRED_AREA           =   2000
    DIRECTION_THICKNESS     =   200 
    WIDTH                   =   1280
    HEIGHT                  =   720

    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)
    print int(cap.get(4)),int(cap.get(3))

    show = np.ndarray((int(cap.get(4)), int(cap.get(3)), 3))                    #System dependency
    
    global msg  #Access global msg
    msg = 'CENTER'
    global UP, DOWN, RIGHT, LEFT
    global isCollision
    global controllerThread
    
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([150,255,255])

        # define range of green color in HSV
        lower_green = np.array([40,100,100])
        upper_green = np.array([80,255,255])
        
        # define range of orange color in HSV
        lower_orange = np.array([0,210,0])
        upper_orange = np.array([10,255,255])

        
        #mask = cv2.inRange(hsv, lower_orange, upper_orange)
        #mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        erosion = cv2.erode(mask.copy(), None, iterations = 2)
        dilation = cv2.dilate(erosion, None, iterations = 2)
        
        #Check OpenCV version(No backward compatibility between versions)
        #OpenCV version 2.*
        if cv2.__version__.startswith("2."):
            contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)       #OpenCV version dependency 
        #OpenCV version 3.*
        elif cv2.__version__.startswith("3."):
            _,contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     #OpenCV version dependency 
        
        #cv2.rectangle(show,(0,0),(int(cap.get(3)), int(cap.get(4))), AQUA, -1)
        msg = 'CENTER'

        if len(contours) > 0 :
            contour = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(contour)
            msg = 'CENTER'
            if w*h > REQUIRED_AREA:
                #cv2.rectangle(show, (x,y), (x+w,y+h), RED, 1)
                #cv2.line(show, (x,y), (WIDTH/2, HEIGHT/2), RED, 2)

                if x < (WIDTH - DIRECTION_THICKNESS)/2:
                    if y < (HEIGHT - DIRECTION_THICKNESS)/2:
                        msg = 'UP LEFT'
                    elif y > (HEIGHT + DIRECTION_THICKNESS)/2:
                        msg = 'DOWN LEFT'
                    else:
                        msg = 'LEFT'
                elif x > (WIDTH + DIRECTION_THICKNESS)/2:
                    if y < (HEIGHT - DIRECTION_THICKNESS)/2:
                        msg = 'UP RIGHT'
                    elif y > (HEIGHT + DIRECTION_THICKNESS)/2:
                        msg = 'DOWN RIGHT'
                    else:
                        msg = 'RIGHT'
                else:
                    if y < (HEIGHT - DIRECTION_THICKNESS)/2:
                        msg = 'UP'
                    elif y > (HEIGHT + DIRECTION_THICKNESS)/2:
                        msg = 'DOWN'

        if controllerThread == True:
            break
    cap.release()
    cv2.destroyAllWindows()


#function to unpause the game
def unpause():
	global pause
	pause=False

#function too quit the game
def quitgame():
	pygame.quit()
	quit()

#function called when p is pressed to paue the game
def paused():
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = textObjects("Paused", largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue",150,450,100,50,GREEN,LGREEN,unpause)
        button("Quit",550,450,100,50,RED,BRED,quitgame)

        pygame.display.update()
        clock.tick(15)  

#display the score of the player on the top left corner
def writeScore(count):
	font=pygame.font.SysFont(None,25)
	text=font.render("SCORE: "+str(count),True,black)
	gameDisplay.blit(text,(0,0))

#utility function for buttons drawing and then the action on clicking 
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
    	if click[0]==1 and action!=None:
            #if action=='gameLoop':
            #   thread.start_new_thread(OpenCVcontroller,())
    		action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

#first function called i.e. the introductory page
def gameIntro():
	#intro = True
    intro=True
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = textObjects("BRICKS", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("START!!!",150,450,100,50,LGREEN,GREEN,gameLoop)
        button("QUIT!!!",550,450,100,50,BRED,RED,quit)            
     #   pygame.draw.rect(gameDisplay, red,(550,450,100,50))

        pygame.display.update()
        clock.tick(50)


#function in case of collision of brick with red blocks
def crash():
    startSound.stop()
    messageDisplay('--HIT--')
    hitSound=pygame.mixer.Sound('hit.wav')
    hitSound.play(0)
    time.sleep(5)
    hitSound.stop()
    gameLoop()

#utility function to display message and return the rectangular grid of the message for position etc 
def textObjects(text,font):
	TextSurface=font.render(text,True,BLACK)
	return TextSurface,TextSurface.get_rect()

#function to display messages
def messageDisplay(text):
	largeText=pygame.font.Font('freesansbold.ttf',115)
	TextSurf,TextRect=textObjects(text,largeText)
	TextRect.center=((WIDTH/2),(HEIGHT/2))
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()
	time.sleep(2)
	gameLoop()

#utility function to congratulate and end the game on the completion of all the levels
def youWin():
    largeText = pygame.font.SysFont("comicsansms",100)
    TextSurf, TextRect = textObjects("CONGRATS", largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    gameDisplay.fill(LBLUE)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    clock.tick(50)
    time.sleep(2)
    quitgame()      


#utility function that checks for collision between the brick and red/green block
def doesCollide(first,second):
    tx=first[0]
    ty=first[1]
    tw=first[2]
    th=first[3]

    px=second[0]
    py=second[1]
    pw=second[2]
    ph=second[3]

    if(tx>=px and tx<=px+pw):
        if(ty>=py and ty<=py+ph):
            return 1
    if(tx+tw>=px and tx+tw<=px+pw):
        if(ty+th>=py and ty+th<=py+ph):
            return 1
    return 0

#main loop
def gameLoop():
    
    #startSound.play(-1) 
    global levelNo
    global pause
    global red
    red=[]
    #while True:
    notCompleteLevel=True
    gameDisplay.fill(LBLUE)
    if(levelNo==1):
        red.append(Box(100,0,30,400,0,0))
        red.append(Box(300,0,30,400,0,0))
        red.append(Box(500,0,30,400,0,0))
        red.append(Box(200,200,30,400,1,0))
        red.append(Box(400,200,30,400,1,0))
        red.append(Box(600,200,30,400,1,0))
        green=[750,300,50,50,0,0]
        brick=[0,0,30,30,0,0]
        # for b in red:
        #     pygame.draw.rect(gameDisplay,RED,(b.x,b.y,b.width,b.height))
        #     print(b.x)
    elif(levelNo==2):
        red.append(Box(100,0,30,400,0,5))
        red.append(Box(300,0,30,400,0,5))
        red.append(Box(500,0,30,400,0,5))
        red.append(Box(200,200,30,400,1,5))
        red.append(Box(400,200,30,400,1,5))
        red.append(Box(600,200,30,400,1,5))
        green=[750,300,50,50,0,0]
        brick=[0,0,30,30,0,0]
    elif(levelNo==3):
        red.append(Box(100,0,30,400,0,5))
        red.append(Box(300,0,30,400,0,5))
        red.append(Box(500,0,30,400,0,5))
        red.append(Box(200,200,30,400,1,5))
        red.append(Box(400,200,30,400,1,5))
        red.append(Box(600,200,30,400,1,5))
        green=[750,300,50,50,0,0]
        brick=[0,0,30,30,0,0]
    elif(levelNo==4):
        red.append(Box(100,0,30,400,0,5))
        red.append(Box(300,0,30,400,0,5))
        red.append(Box(500,0,30,400,0,5))
        red.append(Box(200,200,30,400,1,5))
        red.append(Box(400,200,30,400,1,5))
        red.append(Box(600,200,30,400,1,5))
        green=[750,300,50,50,0,0]
        brick=[0,0,30,30,0,0]
    elif(levelNo==5):
        red.append(Box(100,0,30,400,0,5))
        red.append(Box(300,0,30,400,0,5))
        red.append(Box(500,0,30,400,0,5))
        red.append(Box(200,200,30,400,1,5))
        red.append(Box(400,200,30,400,1,5))
        red.append(Box(600,200,30,400,1,5))
        green=[750,300,50,50,0,0]
        brick=[0,0,30,30,0,0]

    

    xChange=0
    yChange=0

    while notCompleteLevel:
        gameDisplay.fill(LBLUE)
        for b in red:
            if(b.direction==0):
                #moving down
                b.y=b.y+b.speed
                if(b.y+b.height>HEIGHT):
                    b.direction=1
            else:
                #moving down
                b.y-=b.speed
                if(b.y<0):
                    b.direction=0
            pygame.draw.rect(gameDisplay,RED,(b.x,b.y,b.width,b.height))
        pygame.draw.rect(gameDisplay,BLACK,(brick[0],brick[1],brick[2],brick[3]))
        pygame.draw.rect(gameDisplay,GREEN,(green[0],green[1],green[2],green[3]))

        
                
        for b in red:
            if(doesCollide((brick[0],brick[1],brick[2],brick[3]),(b.x,b.y,b.width,b.height))):
                crash()
        if(doesCollide((brick[0],brick[1],brick[2],brick[3]),(green[0],green[1],green[2],green[3]))):
            levelNo+=1
            notCompleteLevel=False
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        xChange=-5
                    elif event.key==pygame.K_RIGHT:
                        xChange=5
                    elif event.key==273:
                        yChange=-5
                    elif event.key==274:
                        yChange=5
                    if event.key==pygame.K_p:
                        pause=True
                        paused()
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT:
                        xChange=0
                    elif event.key==pygame.K_RIGHT:
                        xChange=0
                    elif event.key==273:
                        yChange=0
                    elif event.key==274:
                        yChange=0
        

        if msg == 'UP':
#        pygame.draw.rect(DISPLAYSURF, AQUA, (startX, startY, BOXWIDTH, BOXHEIGHT))
            yChange  -= 5
            #    pygame.draw.rect(DISPLAYSURF, MAROON, (startX, startY, BOXWIDTH, BOXHEIGHT))
             #   UP  =   True
            #   DOWN
        if msg == 'DOWN':
              #  pygame.draw.rect(DISPLAYSURF, AQUA, (startX, startY, BOXWIDTH, BOXHEIGHT))
            yChange  += 5
               # pygame.draw.rect(DISPLAYSURF, MAROON, (startX, startY, BOXWIDTH, BOXHEIGHT))
                #DOWN    =   True
            #   RIGHT
        if msg == 'RIGHT':
         #       pygame.draw.rect(DISPLAYSURF, AQUA, (startX, startY, BOXWIDTH, BOXHEIGHT))
            xChange  += 5
          #      pygame.draw.rect(DISPLAYSURF, MAROON, (startX, startY, BOXWIDTH, BOXHEIGHT))
           #     RIGHT   =   True
            #   LEFT
        if msg == 'LEFT':
            xChange-=5
#                pygame.draw.rect(DISPLAYSURF, AQUA, (startX, startY, BOXWIDTH, BOXHEIGHT))
            # -=5
 #               pygame.draw.rect(DISPLAYSURF, MAROON, (startX, startY, BOXWIDTH, BOXHEIGHT))
  #              LEFT    =   True

        if(0<brick[0]+xChange<WIDTH):
            brick[0]+=xChange
        if(0<brick[1]+yChange<HEIGHT):
            brick[1]+=yChange

        pygame.display.flip()
        clock.tick(50)    
    #levelNo=levelNo+1
    if(levelNo==5):
        youWin()
    

    gameLoop()


thread.start_new_thread(OpenCVcontroller,())
gameIntro()
pygame.quit()
quit()