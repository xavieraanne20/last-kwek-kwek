from __future__ import division
import pygame
import sys
import math
from pygame.locals import *
import random
import time


class Bacteria(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('bactgood.png').convert_alpha()
		self.rect = self.image.get_rect();
		self.rect.move_ip(25,25)
		self.x = random.randrange(0,screen_width-320)
		self.y = random.randrange(60,screen_height-25)

 
	def draw(self, surface):

		surface.blit(self.image, (self.x, self.y))
		self.rect.center=(self.x,self.y)


class Badbacteria(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('bactbad.png').convert_alpha()
		self.rect = self.image.get_rect();
		self.rect.move_ip(25,25)
		self.x = random.randrange(0,screen_width-320)
		self.y = random.randrange(60,screen_height-25)

 
	def draw(self, surface):

		surface.blit(self.image, (self.x, self.y))
		self.rect.center=(self.x,self.y)

class SpeedVitamin(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('speedvitamin.png').convert_alpha()
		self.rect = self.image.get_rect();
		self.rect.move_ip(25,25)
		self.x = random.randrange(0,screen_width-320)
		self.y = random.randrange(60,screen_height-25)

 
	def draw(self, surface):

		surface.blit(self.image, (self.x, self.y))
		self.rect.center=(self.x,self.y)

class GrowVitamin(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('growvitamin.png').convert_alpha()
		self.rect = self.image.get_rect();
		self.rect.move_ip(25,25)
		self.x = random.randrange(0,screen_width-320)
		self.y = random.randrange(60,screen_height-25)

 
	def draw(self, surface):

		surface.blit(self.image, (self.x, self.y))
		self.rect.center=(self.x,self.y)

class Kwekwek(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load('kwekwek.png'),(50,50))
		self.rect = self.image.get_rect();
		self.rect.move_ip(50,50)
		self.x = random.randrange(0,screen_width-320)
		self.y = random.randrange(60,screen_height-25)
		self.speed = 2
		self.rect.center=(self.x,self.y)
		self.bottom = self.rect.bottom
		self.top = self.rect.top
		

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
		if self.kwek_get_size != 0:
			if self.x >= screen_width-320:
				self.x = screen_width-320
			if self.y >= screen_height-20:
				self.y = screen_height-20
			if self.y <= 80:
				self.y = 80
		else:
			self.x = x
			self.y = y
		


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

	def die(self):

		self.speed = 0
		self.x = -500
		self.y = -500
		self.rect.size = [0,0]
		self.image = pygame.image.load('clear.png')
		

	def kwek_get_size(self):
		kwek_size = self.rect.size
		return kwek_size[0]

	def kwek_get_coordinates(self):
		coordinates = [self.x, self.y]
		return coordinates

	def is_collided_with(self, sprite):

		return self.rect.colliderect(sprite.rect)

	def collide_with_kwek(self, spriteGroup):
		if pygame.sprite.spritecollide(self, spriteGroup, True):
			self.kill()
		pygame.display.update()
	'''def dont_overlap_with(self, sprite):
		print (self.bottom)
	
		print (sprite.rect.top)
		print("")
		if self.bottom > sprite.rect.top:
		# Determine how many units the player's rect has gone below the ground.
			overlap = self.bottom- sprite.rect.top
			# Adjust the players sprite by that many units. The player then rests
			# exactly on top of the ground.
			self.bottom  -= overlap 
			# Move the sprite now so that following if statements are calculated based upon up-to-date information.
		if self.top < sprite.rect.bottom:
			overlap = sprite.rect.bottom 
			self.rect.top  += overlap 
		pygame.display.update()
		# Move the sprite now so that following if statements are calculated based upon up-to-date information.
	# And so on for left and right.'''

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load(image_file),(screen_width, screen_height))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location



def text_objects(text, font):
	textSurface = font.render(text, True, (255,255,255))
	return textSurface, textSurface.get_rect()

def image_button(x_position, y_position, button_width, button_height, mode):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	global number_of_players
	if mode == "play":
		if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
			button_image = pygame.transform.smoothscale(pygame.image.load('ready_hover.png'),(220,220))
			rect = button_image.get_rect()
			rect.x = x_position-10
			rect.y = y_position-60
			rect.inflate_ip(30,30) #button
			if click[0] == 1:
				game_timebound_mode()()
			'''for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					mouseClicked = True'''
					
					#number_of_players += 1
					#if number_of_players > 2:
						#if click[0] == 1:
							
		else:
			button_image = pygame.transform.scale(pygame.image.load('ready.png'),(button_width,button_height))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
		screen.blit(button_image, rect)
	elif mode == "exit":
		if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
			button_image = pygame.transform.smoothscale(pygame.image.load('exit.png'),(button_width+20,button_height+20))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
			rect.inflate_ip(20,20) #button
			if click[0] == 1:
				pygame.quit()
				sys.exit()
		else:
			button_image = pygame.transform.scale(pygame.image.load('exit.png'),(button_width,button_height))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
		screen.blit(button_image, rect)
	elif mode == "about":
		if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
			button_image = pygame.transform.smoothscale(pygame.image.load('about.png'),(button_width+20,button_height+20))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
			rect.inflate_ip(20,20) #button
			if click[0] == 1:
				game_instructions()
		else:
			button_image = pygame.transform.scale(pygame.image.load('about.png'),(button_width,button_height))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
		screen.blit(button_image, rect)
	elif mode == "back":
		if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
			button_image = pygame.transform.smoothscale(pygame.image.load('back.png'),(button_width+20,button_height+20))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
			rect.inflate_ip(20,20) #button
			if click[0] == 1:
				game_menu()
		else:
			button_image = pygame.transform.scale(pygame.image.load('back.png'),(button_width,button_height))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
		screen.blit(button_image, rect)
	elif mode == "new_game":
		if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
			button_image = pygame.transform.smoothscale(pygame.image.load('kwek_button.png'),(button_width+30,button_height+30))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
			rect.inflate_ip(20,20) #button
			if click[0] == 1:
				game_lobby()
		else:
			button_image = pygame.transform.scale(pygame.image.load('kwek_button.png'),(button_width,button_height))
			rect = button_image.get_rect()
			rect.x = x_position
			rect.y = y_position
		screen.blit(button_image, rect)
'''def button(message, x_position, y_position, button_width, button_height, inactive_color, active_color, mode = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x_position+button_width > mouse[0] > x_position and y_position+button_height > mouse[1] > y_position:
		pygame.draw.rect(screen, active_color, (x_position,y_position,button_width,button_height)) #button
		if click[0] == 1 and mode != None:
			if mode == "new_game":
				game_lobby()
			elif mode == "exit_game":
				pygame.quit()
				sys.exit()
			elif mode == "instructions":
				game_instructions()
			elif mode == "back":
				game_menu()
			elif mode == "play":
				game_timebound_mode()

	else:
		pygame.draw.rect(screen, inactive_color, (x_position,y_position,button_width,button_height)) #button
	smallText = pygame.font.Font("freesansbold.ttf",20)
	textSurf, textRect = text_objects(message, smallText)
	textRect.center = ( (x_position+(button_width/2)), (y_position+(button_height/2)) )
	screen.blit(textSurf, textRect)'''

pygame.init()
pygame.time.get_ticks()/1000
font = pygame.font.SysFont("Bungee", 50)
font2 = pygame.font.SysFont("Bungee", 20)

#creating the background
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
BackGround = Background('sauce.jpg', [0,0])

#creating colors
green = (0,200,0)
bright_green = (0,255,0)
blue = (0,0,200)
bright_blue = (0,0,255)
red = (200,0,0)
bright_red = (255,0,0)

#instanciation of objects in the game
kweks = Kwekwek()
kweks2 = Kwekwek()
kweks3 = Kwekwek()
kwek_group = pygame.sprite.Group()
kwek_group.add(kweks)
kwek_group.add(kweks2)
kwek_group.add(kweks3)
kweks = {
	'kwek' : kweks,
	'kwek2' : kweks2,
	'kwek3' : kweks3,
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



#function for the main game
def game_timebound_mode():
	
	Clock = pygame.time.Clock()
	game_start_timer = time.time()

	game_is_running = True

	while game_is_running:


		game_timer = time.time()
		time_elapsed = game_timer - game_start_timer
		game_time = 181-time_elapsed
		if int(game_time) == 0:
			kwek_sizes = []*0
			for k in kweks:
				kwek_sizes.append(kweks[k].kwek_get_size())
			print(kwek_sizes)
			biggest_size = max(kwek_sizes)
		

			print("PLAYER with size " + str(biggest_size) + " IS THE WINNER") 
			game_is_running = False
			game_menu()

		screen.fill([255, 255, 255])
		screen.blit(BackGround.image, BackGround.rect)
		pygame.draw.rect(screen, (255,255,255), (5,5,170,50), 0)
	
		pygame.draw.rect(screen, (255,255,255), (700,20,300,800), 5)

		s = pygame.Surface((290,740))  # the size of your rect
		s.set_alpha(128)                # alpha level
		s.fill((30,30,30))           # this fills the entire surface
		screen.blit(s, (705,60))  


		pygame.draw.rect(screen, (0,0,0), (0,0,screen_width,70), 0)

		clock_image = pygame.transform.smoothscale(pygame.image.load('clock.png'),(50,50))
		screen.blit(clock_image,(10,5))
		time_string = format(int(game_time))
				
		top_player_string = "Leaderboard"
		time_left_string = "TIME LEFT"

		
		text = font.render(time_string, True, (255,255,255))
		text2 = font2.render(time_left_string, True, (255,255,255))
		text3 = font.render(top_player_string, True, (255,255,255))
		

		screen.blit(text, (70, 15))
		screen.blit(text2,(5, 60))
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

		'''for ablock in kwek_group:
			kwek_group.remove(ablock)
			ablock.collide_with_kwek(kwek_group)
			kwek_group.add(ablock)'''

		for j in kweks:
			for i in kweks:
				if kweks[j].is_collided_with(kweks[i]):
					
					if kweks[j].kwek_get_size() > kweks[i].kwek_get_size():
	
						kweks[i].die()
						kwek_group.remove(kweks[i])
						kweks[j].grow(int(kweks[i].kwek_get_size()/2))
			
						
						
					elif kweks[j].kwek_get_size() < kweks[i].kwek_get_size():
		
						kweks[j].die()
						kwek_group.remove(kweks[j])
						kweks[i].grow(int(kweks[i].kwek_get_size()/2))
						
					
					elif kweks[j].kwek_get_size() == kweks[i].kwek_get_size() and kweks[i] != kweks[j]:
						kill = random.randrange(0,1)
						if kill == 0:
							kweks[j].die()
							kwek_group.remove(kweks[j])
							kweks[i].grow(int(kweks[i].kwek_get_size()/2))
						else:
							kweks[i].die()
							kwek_group.remove(kweks[i])
							kweks[j].grow(int(kweks[i].kwek_get_size()/2))
						
		
			for i in bacterium:
				if kweks[j].is_collided_with(bacterium[i]):
					kweks[j].grow(5)
					bacterium[i].x = random.randrange(0,screen_width-320)
					bacterium[i].y = random.randrange(60,screen_height-25)
			
			for i in badbacterium:
				if kweks[j].is_collided_with(badbacterium[i]):
					if kweks[j].kwek_get_size() <= 10:
					
						kweks[j].kill
						
							
					else:
						kweks[j].shrink(10)
						badbacterium[i].x = random.randrange(0,screen_width-320)
						badbacterium[i].y = random.randrange(60,screen_height-25)

			
			for i in speedvitamins:
				if kweks[j].is_collided_with(speedvitamins[i]):
					
					if random.randrange(0,2) == 0: #33% chance of having effect
					   
						print ("BOOST")
						speedvitamins[i].x = random.randrange(0,screen_width-320)
						speedvitamins[i].y = random.randrange(60,screen_height-25)
						kweks[j].speed += 1
					else:
						print ("NO BOOST")
						speedvitamins[i].x = random.randrange(0,screen_width-320)
						speedvitamins[i].y = random.randrange(60,screen_height-25)

			for i in growthvitamins:
				if kweks[j].is_collided_with(growthvitamins[i]):

					if random.randrange(0,2) == 0: #33% chance of having effect
					   
						print ("GROW")
						growthvitamins[i].x = random.randrange(0,screen_width-320)
						growthvitamins[i].y = random.randrange(60,screen_height-25)
						kweks[j].grow(10)
					else:
						print ("NO EFFECT")
						growthvitamins[i].x = random.randrange(0,screen_width-320)
						growthvitamins[i].y = random.randrange(60,screen_height-25)
		

		for key, value in kweks.items() :
			
			#print (str(max(value.kwek_get_size())) + key)
			print (key, value.kwek_get_size())
			if len(kwek_group) == 1:

				if value.kwek_get_size() != 0:

					print ("the winner is "+ str(key) + " with a score of " + str(value.kwek_get_size()))

			

		#print (kwek_group.sprites())
		#if len(kwek_group) == 1:
			#print (kwek_group)
		#print (kweks)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		Clock.tick(40)

def game_instructions():
	running = True

	while running:

		screen.fill([255, 255, 255])
		screen.blit(BackGround.image, BackGround.rect)
		instruction_image = pygame.transform.smoothscale(pygame.image.load('mechanics.png'),(750,750))
		screen.blit(instruction_image, (screen_width/2-375,70))


		title_image = pygame.transform.smoothscale(pygame.image.load('title.png'),(175,75))
		screen.blit(title_image, (800,20))
		


	
		image_button(10,10,170,70,"back")

		 
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

def game_lobby():
	running = True
	click = pygame.mouse.get_pressed()
	global number_of_players
	while running:

		screen.fill([255, 255, 255])
		screen.blit(BackGround.image, BackGround.rect)
	
		title_image = pygame.transform.smoothscale(pygame.image.load('title.png'),(466,198))
		screen.blit(title_image, (screen_width/2-233,70))
		

	
		image_button(screen_width/2-85, screen_height/2-60,170,70,"play")
		image_button(10,10,170,70,"back")
		image_button(10,720,170,70,"exit")    

		

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

#default game menu
def game_menu():
	running = True

	while running:

		screen.fill([255, 255, 255])
		screen.blit(BackGround.image, BackGround.rect)
		title_image = pygame.transform.smoothscale(pygame.image.load('title.png'),(699,297))
		screen.blit(title_image, (screen_width/2-350,60))
		

		image_button(screen_width/2-150, screen_height/2-60,300,300, "new_game")
		image_button(screen_width/2 - 170 - 100,650,170,70,"about")
		image_button(screen_width/2 + 100,650,170,70,"exit")    



		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

running = True

while running:
	game_menu()