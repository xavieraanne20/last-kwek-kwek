from __future__ import division
import pygame
import sys
import math
from pygame.locals import *
import random


 

class Bacteria(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bact2.png').convert_alpha()
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
        self.x = 1
        self.y = 1
        self.rect.center=(self.x,self.y)
        

    def draw(self, surface):

        speed = 5
        cursor_x, cursor_y = pygame.mouse.get_pos()
       # Vector from me to cursor
        dx = cursor_x - self.x
        dy = cursor_y - self.y

        # Unit vector in the same direction
        distance = math.sqrt(dx*dx + dy*dy)
        dx /= distance
        dy /= distance

        # speed-pixel vector in the same direction
        dx *= speed
        dy *= speed

        # And now we move:
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

    def kwek_get_size(self):

        kwek_size = self.rect.size
        return kwek_size[0]

    def is_collided_with(self, sprite):

        return self.rect.colliderect(sprite.rect)



pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
kwek = Kwekwek()
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
#bacterium.append(bact1)

Clock = pygame.time.Clock()



#print (kwek.kwek_position())

running = True



while running:
    screen.fill((255,255,255))
    bact1.draw(screen)
    bact2.draw(screen)
    bact3.draw(screen)
    bact4.draw(screen)
    bact5.draw(screen)
    bact6.draw(screen)
    bact7.draw(screen)
    bact8.draw(screen)
    bact9.draw(screen)
    bact10.draw(screen)


    kwek.draw(screen)

    kwek_size = kwek.kwek_get_size()
   


    for i in bacterium:
        if kwek.is_collided_with(bacterium[i]):
            kwek.grow(5)
            bacterium[i].x = random.randrange(0,screen_width-25)
            bacterium[i].y = random.randrange(0,screen_height-25)
 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    Clock.tick(40)