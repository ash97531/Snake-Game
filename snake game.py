import pygame as py
import random 
import os
import time
py.mixer.init()
py.init()

#colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#creating window
scrwidth = 900
scrheight = 600
gamewindow = py.display.set_mode((scrwidth, scrheight))

#creating title
py.display.set_caption('snake by ash')
py.display.update()
clock = py.time.Clock()
font = py.font.SysFont(None, 55)

def welcome():
    exitgame = False
    py.mixer.music.load(".\\welcome music.mp3")
    py.mixer.music.play(-1)
    while not exitgame:
        bgimg = py.image.load('.\\welcome.jpeg')
        bgimg = py.transform.scale(bgimg, (scrwidth, scrheight)).convert_alpha()
        gamewindow.blit(bgimg, (0, 0))
        txtscr('Welcome To Snakes', white, 260, 250)
        txtscr('Press Space Bar To Play', white, 232, 290)
        for event in py.event.get():
            if event.type == py.QUIT:
                exitgame = True

            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    py.mixer.music.load(".\\background2.mp3")
                    py.mixer.music.play(-1)
                    gameloop()
        
        py.display.update()        
        clock.tick(60)


def txtscr(text, color, x, y):
        scrtxt = font.render(text, True, color)
        gamewindow.blit(scrtxt, [x,y])

def plotsn(gamewindow, color, snlist, snsize):
        for x,y in snlist:
            py.draw.rect(gamewindow, color, [x, y, snsize, snsize])

def gameloop():
    #game variables
    exitgame = False
    gameover = False
    snx = 45
    sny = 55
    snsize = 30
    velox = 0
    veloy = 0
    initvelo = 5
    score = 0
    foodx = random.randint(20, scrwidth/2)
    foody = random.randint(20, scrheight/2)
    fps = 60
    snlist = []
    snlength = 1
    ini = time.time()
    c = 0

    #check if high score exist or not
    if (not os.path.exists('.\\highscore.txt')):
        with open('.\\highscore.txt', 'w') as f:
            f.write('0')

    with open('.\\highscore.txt', 'r') as f:
        highscore = f.read()

    #game loop
    while not exitgame:

        if gameover:
            with open('.\\highscore.txt', 'w') as f:
                f.write(str(highscore))
            gamewindow.fill(white)
            bgimg = py.image.load('.\\gameover.jpeg')
            bgimg = py.transform.scale(bgimg, (scrwidth, scrheight)).convert_alpha()
            gamewindow.blit(bgimg, (0, 0))
            txtscr('Press Enter To Continue', red, 225, 500)

            for event in py.event.get():
                if event.type == py.QUIT:
                    exitgame = True

                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        welcome()


        else:
            
            for event in py.event.get():
                
                if event.type == py.QUIT:
                    exitgame = True
                
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT:
                        velox = initvelo
                        veloy = 0

                    if event.key == py.K_LEFT:
                        velox = - initvelo
                        veloy = 0

                    if event.key == py.K_UP:
                        velox = 0
                        veloy = - initvelo

                    if event.key == py.K_DOWN:
                        velox = 0
                        veloy = initvelo

                    if event.key == py.K_q:
                        score = score + 50
                        snlength = snlength + 25
            
            snx = snx + velox
            sny = sny + veloy


            if abs(snx - foodx)<6 and abs(sny - foody)<6:
                score = score + 10
                foodx = random.randint(20, scrwidth/2)
                foody = random.randint(20, scrheight/2)
                snlength = snlength +5
                if score > int(highscore):
                    highscore = score

            bgimg = py.image.load('.\\back ground.jpeg')
            bgimg = py.transform.scale(bgimg, (scrwidth, scrheight)).convert_alpha()
            gamewindow.blit(bgimg, (0, 0))
            txtscr('Score : ' + str(score) + '   High Score :' + str(highscore), red, 5, 5)
            py.draw.rect(gamewindow, red, [foodx, foody, snsize, snsize]) 

            head = []
            head.append(snx)
            head.append(sny)
            snlist.append(head)

            if head in snlist[:-2]:
                gameover = True
                py.mixer.music.load(".\\explosion.mp3")
                py.mixer.music.play()

            if (snx > scrwidth) or (snx < 0) or (sny > scrheight) or (sny < 0) :
                gameover = True
                py.mixer.music.load(".\\explosion.mp3")
                py.mixer.music.play()

            if len(snlist) > snlength:
                del snlist[0]

            plotsn(gamewindow, black, snlist, snsize)     
        py.display.update()        
        clock.tick(fps)


    py.quit()
    quit()

welcome()
