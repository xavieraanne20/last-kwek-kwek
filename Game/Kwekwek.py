from __future__ import division
import pygame
import sys
import math
from pygame.locals import *
import random


 

class Bacteria(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bactgood.png').convert_alpha()
        self.rect = self.image.get_rect();
        self.rect.move_ip(25,25)
        self.x = random.randrange(0,screen_width-25)
        self.y = random.randrange(0,screen_height-25)

 
    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))
        self.rect.center=(self.x,self.y)


class Badbacteria(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bactbad.png').convert_alpha()
        self.rect = self.image.get_rect();
        self.rect.move_ip(25,25)
        self.x = random.randrange(0,screen_width-25)
        self.y = random.randrange(0,screen_height-25)

 
    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))
        self.rect.center=(self.x,self.y)

class SpeedVitamin(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('speedvitamin.png').convert_alpha()
        self.rect = self.image.get_rect();
        self.rect.move_ip(25,25)
        self.x = random.randrange(0,screen_width-25)
        self.y = random.randrange(0,screen_height-25)

 
    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))
        self.rect.center=(self.x,self.y)

class GrowVitamin(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('growvitamin.png').convert_alpha()
        self.rect = self.image.get_rect();
        self.rect.move_ip(25,25)
        self.x = random.randrange(0,screen_width-25)
        self.y = random.randrange(0,screen_height-25)

 
    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))
        self.rect.center=(self.x,self.y)

class Kwekwek(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('kwekwek.png'),(50,50))
        self.rect = self.image.get_rect();
        self.rect.move_ip(50,50)
        self.x = random.randrange(0,screen_width-25)
        self.y = random.randrange(0,screen_height-25)
        self.speed = 2
        self.rect.center=(self.x,self.y)
        

    def draw(self, surface):

        
        cursor_x, cursor_y = pygame.mouse.get_pos()
        dx = cursor_x - self.x
        dy = cursor_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        dx /= distance
        dy /= distance
        dx *= self.speed
        dy *= self.speed
        self.x += dx
        self.y += dy

        if self.x >= screen_width-50:
            self.x = screen_width-50
        if self.y >= screen_height-50:
            self.y = screen_height-50

        self.rect.center=(self.x,self.y)
        surface.blit(self.image, (self.x-(self.rect.width/2), self.y-(self.rect.height)/2))
        pygame.display.update()


    def grow(self,  points):

        kwek_size2 = self.rect.size
        self.image = pygame.transform.scale(pygame.image.load('kwekwek.png'),(kwek_size2[0]+points,kwek_size2[0]+points))
        self.rect.size=(kwek_size2[0]+points,kwek_size2[0]+points)
        pygame.display.update()

    def shrink(self, points):

        kwek_size2 = self.rect.size
        self.image = pygame.transform.scale(pygame.image.load('kwekwek.png'),(kwek_size2[0]-points,kwek_size2[0]-points))
        self.rect.size=(kwek_size2[0]-points,kwek_size2[0]-points)
        pygame.display.update()


    def kwek_get_size(self):

        kwek_size = self.rect.size
        return kwek_size[0]

    def is_collided_with(self, sprite):

        return self.rect.colliderect(sprite.rect)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(image_file),(screen_width, screen_height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location



pygame.init()
pygame.time.get_ticks()/1000
font = pygame.font.SysFont("Ubuntu", 30)

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
BackGround = Background('sauce.jpg', [0,0])

kwek = Kwekwek()
kwek2 = Kwekwek()

kweks = {
    'kwek1' : kwek,
    'kwek2' : kwek2,
}


bact1 = Bacteria()
bact2 = Bacteria()
bact3 = Bacteria()
bact4 = Bacteria()
bact5 = Bacteria()
bact6 = Bacteria()
bact7 = Bacteria()
bact8 = Bacteria()
bact9 = Bacteria()
bact10 = Bacteria()


bacterium = {
    'bact1' : bact1,
    'bact2' : bact2,
    'bact3' : bact3,
    'bact4' : bact4,
    'bact5' : bact5,
    'bact6' : bact6,
    'bact7' : bact7,
    'bact8' : bact8,
    'bact9' : bact9,
    'bact10' : bact10,
}

badbact1 = Badbacteria()
badbact2 = Badbacteria()
badbact3 = Badbacteria()
badbact4 = Badbacteria()
badbact5 = Badbacteria()

badbacterium = {
    'badbact1' : badbact1,
    'badbact2' : badbact2,
    'badbact3' : badbact3,
    'badbact4' : badbact4,
    'badbact5' : badbact5,
}

speedvit1 = SpeedVitamin()
speedvit2 = SpeedVitamin()
speedvit3 = SpeedVitamin()
speedvit4 = SpeedVitamin()

speedvitamins = {
    'speedvit1': speedvit1,
    'speedvit2': speedvit2,
    'speedvit3': speedvit3,
    'speedvit4': speedvit4,
}

growvit1 = GrowVitamin()
growvit2 = GrowVitamin()
growvit3 = GrowVitamin()
growvit4 = GrowVitamin()

growthvitamins = {
    'growvit1' :growvit1,
    'growvit2' :growvit2,
    'growvit3': growvit3,
    'growvit4' :growvit4,

}

Clock = pygame.time.Clock()
running = True

while running:

    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.draw.rect(screen, (255,255,255), (5,5,170,50), 0)
    pygame.draw.rect(screen, (255,255,255), (675,575,300,200), 5)
    pygame.draw.rect(screen, (255,255,255), (675,20,300,200), 5)
    s = pygame.Surface((300,200))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((30,30,30))           # this fills the entire surface
    screen.blit(s, (675,20))  

    time_string = "Time: {} ".format(int(pygame.time.get_ticks()/1000))
    chat_string = "Chat box"
    top_player_string = "Leaderboard"
    
    text = font.render(time_string, True, (0,0,0))
    text2 = font.render(chat_string, True, (0,0,0))
    text3 = font.render(top_player_string, True, (255,255,255))

    screen.blit(text, (10, 15))
    screen.blit(text2, (695,595))
    screen.blit(text3, (735,25))
   
      

    for i in bacterium:
        bacterium[i].draw(screen)

    for i in badbacterium:
        badbacterium[i].draw(screen)

    for i in speedvitamins:
        speedvitamins[i].draw(screen)

    for i in growthvitamins:
        growthvitamins[i].draw(screen)

    for i in kweks:
        kweks[i].draw(screen)



    for j in kweks:
        for i in bacterium:
            if kweks[j].is_collided_with(bacterium[i]):
                kweks[j].grow(5)
                bacterium[i].x = random.randrange(0,screen_width-25)
                bacterium[i].y = random.randrange(0,screen_height-25)
        
        for i in badbacterium:
            if kweks[j].is_collided_with(badbacterium[i]):
                kweks[j].shrink(10)
                badbacterium[i].x = random.randrange(0,screen_width-25)
                badbacterium[i].y = random.randrange(0,screen_height-25)
        
        for i in speedvitamins:
            if kweks[j].is_collided_with(speedvitamins[i]):
                
                if random.randrange(0,3) % 2 == 0: #33% chance of having effect
                   
                    print ("BOOST")
                    speedvitamins[i].x = random.randrange(0,screen_width-25)
                    speedvitamins[i].y = random.randrange(0,screen_height-25)
                    kweks[j].speed += 1
                else:
                    print ("NO BOOST")
                    speedvitamins[i].x = random.randrange(0,screen_width-25)
                    speedvitamins[i].y = random.randrange(0,screen_height-25)

        for i in growthvitamins:
            if kweks[j].is_collided_with(growthvitamins[i]):

                if random.randrange(0,3) % 2 == 0: #33% chance of having effect
                   
                    print ("GROW")
                    growthvitamins[i].x = random.randrange(0,screen_width-25)
                    growthvitamins[i].y = random.randrange(0,screen_height-25)
                    kweks[j].grow(10)
                else:
                    print ("NO EFFECT")
                    growthvitamins[i].x = random.randrange(0,screen_width-25)
                    growthvitamins[i].y = random.randrange(0,screen_height-25)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    Clock.tick(40)