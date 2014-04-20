# 1 - Import library
import pygame
import sys
import time
import math
import random
from pygame.locals import *

clock = pygame.time.Clock() 
# 2 - Initialize the game
pygame.init()
pygame.mixer.init()

width, height = 640, 480
screen=pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]
acc = [0,0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640,100]]
healthvalue = 200
powerups = []
powertimer = 100

# 3 - Load images
player = pygame.image.load("resources/images/dude.png").convert_alpha()
grass = pygame.image.load("resources/images/grass.png").convert_alpha()
castle = pygame.image.load("resources/images/castle.png").convert_alpha()
arrow = pygame.image.load("resources/images/bullet.png").convert_alpha()
badguyimg1 = pygame.image.load("resources/images/badguy.png").convert_alpha()
badguyimg = badguyimg1
health = pygame.image.load("resources/images/health.png").convert_alpha()
healthbar = pygame.image.load("resources/images/healthbar.png").convert_alpha()
gameover = pygame.image.load("resources/images/gameover.png").convert_alpha()
youwin = pygame.image.load("resources/images/youwin.png").convert_alpha()
powerupimg = pygame.image.load("resources/images/powerup.png").convert_alpha()
buttonimg = pygame.image.load("resources/images/button.png").convert_alpha()


#3.1 - Load sounds
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
power_up_sound = pygame.mixer.Sound("resources/audio/power_up_sound.wav")
effect = pygame.mixer.Sound("resources/audio/effect.wav")
power_up_sound.set_volume(1)
hit.set_volume(0.25)
enemy.set_volume(0.25)
shoot.set_volume(0.25)
effect.set_volume(1)
pygame.mixer.music.load("resources/audio/pirate.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.75)



def screen_elements(back,castle):
    for x in range(width/back.get_width() + 1):
        for y in range(height/back.get_height() + 1):
            screen.blit(back,(x*100,y*100))
    screen.blit(castle , (0,30))
    screen.blit(castle , (0,135))
    screen.blit(castle , (0,240))
    screen.blit(castle , (0,345))    


def powerup_func(powertimer,badtimer1,power_up_sound,powerupimg):
    if powertimer <= 0 and badtimer1 > 10 :
        powertimer = 1000
        if powerups == []:
            power_up_sound.play()
            powerups.append([random.randint(100,500), random.randint(100,400)])
        
    
    for powerup in powerups:
        screen.blit(powerupimg, (powerup[0],powerup[1]))
    return powertimer

def player_func():
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    #playerrot.fill((255,255,255)) #(For understanding rotation)
    screen.blit(playerrot, playerpos1)
    return playerpos1

def draw_arrows(arrows,speed):
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*speed
        vely=math.sin(bullet[0])*speed
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    return arrows

def draw_badguys(badguys,badtimer,badtimer1,healthvalue,speed):
    
    if badtimer == 0: 
        badguys.append([640,random.randint(50,430)])
        badtimer = 100 - (badtimer1*2)
        if badtimer1 >= 40:
            badtimer1 = 40
        else:
            badtimer1 += 5
    index = 0 
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= speed
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        index += 1
    for badguy in badguys: screen.blit(badguyimg, badguy)
    return badtimer1 ,badtimer,healthvalue

def arrow_collision(badguys,arrows):
    index1 = 0
    for badguy in badguys:
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        index2 = 0
        for bullet in arrows:
            bulletrect = pygame.Rect(arrow.get_rect())
            bulletrect.left = bullet[1]
            bulletrect.top = bullet[2]
            if badrect.colliderect(bulletrect):
                enemy.play()
                acc[0] += 1
                arrows.pop(index2)
                badguys.pop(index1)
            index2 += 1
        index1 += 1
    return badguys , arrows

def draw_clock(time):
    font = pygame.font.Font("arial.ttf", 30)
    timetext = font.render(str((time-pygame.time.get_ticks())/60000)+":"+
    str((time-pygame.time.get_ticks())/1000%60).zfill(2), False, (0,0,0))
    timerect = timetext.get_rect()
    timerect.topright = [635,5]
    screen.blit(timetext, timerect)

def event_queue(arrows,keys,powerups,healthvalue):
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w:
                keys[0] = True
            if event.key == pygame.K_a:
                keys[1] = True
            if event.key == pygame.K_s:
                keys[2] = True
            if event.key == pygame.K_d:
                keys[3] = True
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w:
                keys[0] = False
            if event.key == pygame.K_a:
                keys[1] = False
            if event.key == pygame.K_s:
                keys[2] = False
            if event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            index3 = 0
            
            for powerup in powerups:
                powerect = powerupimg.get_rect()
                powerect.left = powerup[0]
                powerect.top = powerup[1]
                if powerect.collidepoint(pygame.mouse.get_pos()):
                    effect.play()
                    powerups.pop(index3)
                    healthvalue = 200
                    
                index3 += 1

            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-
                            (playerpos1[0]+26)),playerpos1[0],playerpos1[1]+16])
    return arrows,keys,healthvalue,powerups

def move_player(speed):
    if keys[0]: playerpos[1] -= speed
    elif keys[2]: playerpos[1] += speed
    if keys[1]: playerpos[0] -= speed
    elif keys[3]: playerpos[0] += speed


level2 = False
level1 = True
win = True 
while level1:
    badtimer -= 1
    powertimer -= 1
    
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen_elements(grass,castle)
    
    #6.1 - Power ups
    powertimer = powerup_func(powertimer,badtimer1,power_up_sound,powerupimg)

    # 6.2 - Set player position and rotation
    playerpos1 = player_func()

    # 6.3 - Draw arrows
    arrows = draw_arrows(arrows,20)
    # 6.4 - Draw Bad guys
    badtimer1,badtimer,healthvalue = draw_badguys(badguys,badtimer,badtimer1,healthvalue,8)

    #6.5 - Arrow Collision 
    badguys , arrows = arrow_collision(badguys,arrows)

    #6.6 - Draw Clock
    draw_clock(90000)

    #6.7 - Health Bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue-5): screen.blit(health, (health1+8,8))

    # 7 - update the screen
    pygame.display.flip()

    # 8 - loop through the events
    arrows,keys,healthvalue,powerups = event_queue(arrows,keys,powerups,healthvalue)
    
    #9- Move Player
    move_player(8)

    if pygame.time.get_ticks() > 90000:
        level1 = False
        win = True
    if healthvalue <= 0:
        level1 = False
        win = False
    if acc[1] != 0: accuracy = int(acc[0]*1.0/acc[1]*100)
    else: accuracy = 0

    clock.tick(35)

    
if win == False:
    font = pygame.font.Font("arial.ttf", 24)
    text = font.render("Accuracy: %s%%" % accuracy, True, (0,0,0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0,0))
    screen.blit(text, textrect)

else:
    font = pygame.font.Font("arial.ttf", 24)
    text = font.render("Accuracy: %s%%" % accuracy, True, (0,0,0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0,0))
    screen.blit(text, textrect)
    screen.blit(buttonimg,(250,300))

while not level2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonrect = buttonimg.get_rect()
            buttonrect.left = 250
            buttonrect.top = 300
            if buttonrect.collidepoint(pygame.mouse.get_pos()):
                level2 = True
    
    pygame.display.flip()
    # time.sleep(0.006)
    # time.sleep(0.006)

pygame.mixer.music.load("resources/audio/need_for_madness.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)
badtimer = 100
badtimer1 = 0
powertimer = 100
arrow = pygame.image.load("resources/images/bullet2.png").convert_alpha()
acc = [0,0]

time_passed= pygame.time.get_ticks()

while level2:
    badtimer -= 1
    powertimer -= 1
    
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen_elements(grass,castle)
    
    
    #6.1 - Power ups
    powertimer = powerup_func(powertimer,badtimer1,power_up_sound,powerupimg)

    # 6.2 - Set player position and rotation
    playerpos1 = player_func()

    # 6.3 - Draw arrows
    arrows = draw_arrows(arrows,30)
    # 6.4 - Draw Bad guys
    badtimer1,badtimer , healthvalue = draw_badguys(badguys,badtimer,badtimer1,healthvalue,15)

    #6.5 - Arrow Collision 
    badguys , arrows = arrow_collision(badguys,arrows)

    #6.6 - Draw Clock
    draw_clock(90000 + time_passed)

    #6.7 - Health Bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue-5): screen.blit(health, (health1+8,8))

    # 7 - update the screen
    pygame.display.flip()

    # 8 - loop through the events
    arrows,keys,healthvalue,powerups = event_queue(arrows,keys,powerups,healthvalue)
    
    #9- Move Player
    move_player(8)

    if pygame.time.get_ticks() > 90000:
        level2 = False
        win = True
    if healthvalue <= 0:
        level1 = False
        win = False
    if acc[1] != 0: accuracy = int(acc[0]*1.0/acc[1]*100)
    else: accuracy = 0

    clock.tick(35)    


if win == False:
    font = pygame.font.Font("arial.ttf", 24)
    text = font.render("Accuracy: %s%%" % accuracy, True, (0,0,0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0,0))
    screen.blit(text, textrect)

else:
    font = pygame.font.Font("arial.ttf", 24)
    text = font.render("Accuracy: %s%%" % accuracy, True, (0,0,0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0,0))
    screen.blit(text, textrect)

while not level2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonrect = buttonimg.get_rect()
            buttonrect.left = 250
            buttonrect.top = 300
            if buttonrect.collidepoint(pygame.mouse.get_pos()):
                level2 = True
    
    pygame.display.flip()