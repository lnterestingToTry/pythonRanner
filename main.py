import pygame
import random
#from os import path
import os

width = 1366
height = 768
fps = 30

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
game_surface = pygame.Surface((1366, 768))

pygame.display.set_caption("p")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
health_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
background = pygame.sprite.Group()

window_width = window.get_width()
window_height = window.get_height()

for_scale_coefficient = width / height

def fullscreen_with_ratio():
	game_surface_local = pygame.transform.scale(game_surface, (int(window_height * for_scale_coefficient), window_height))
	new_game_width = game_surface_local.get_width()
	window.blit(game_surface_local, ((window_width / 2) - (new_game_width) / 2, 0))

def draw_text(surf, text, size, x, y, color):
	font_name = pygame.font.match_font('arial')
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = (x, y)
	surf.blit(text_surface, text_rect)

class button_play(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((200, 200))
		#self.image.fill((0,255,0))
		self.image = button_start
		self.rect = self.image.get_rect()
		self.rect.centerx = width / 2
		self.rect.centery = height / 2
		self.controls_show1 = wsda_controls()
		self.controls_show2 = esc_controls()
		self.controls_show3 = x_controls()
		all_sprites.add(self)

	def update(self):
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_RETURN]:
			self.kill()
			self.controls_show1.kill()
			self.controls_show2.kill()
			self.controls_show3.kill()
			p.to_start_anim = True

class button_start_new_game(pygame.sprite.Sprite): #after gameover
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((200, 200))
		#self.image.fill((255,0,0))
		self.image = button_restart
		self.rect = self.image.get_rect()
		self.rect.centerx = width / 2
		self.rect.centery = height / 2
		self.controls_show1 = wsda_controls()
		self.controls_show2 = esc_controls()
		self.controls_show3 = x_controls()

		global hb_manager
		hb_manager.hp_1 = player_health(hb_manager.first_hp_pos[0], hb_manager.first_hp_pos[1])
		hb_manager.hp_2 = player_health(hb_manager.second_hp_pos[0], hb_manager.second_hp_pos[1])
		hb_manager.hp_3 = player_health(hb_manager.third_hp_pos[0], hb_manager.third_hp_pos[1])

		hb_manager.all_hp = [hb_manager.hp_1, hb_manager.hp_2, hb_manager.hp_3]

		all_sprites.add(self)

	def update(self):
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_RETURN]:
			self.kill()
			for i in all_sprites:
				i.kill()
			global p
			self.controls_show1.kill()
			self.controls_show2.kill()
			self.controls_show3.kill()
			g = ground()
			p = player()
			p.to_start_anim = True
			d_manager.timer_var = 0

class player(pygame.sprite.Sprite): #ballon
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((60, 100))
		#self.image.fill((0,0,255))
		self.image = player_image
		self.damage_anim_imgs = bp_damage_anim
		self.kill_anim_imgs = bp_kill_anim
		self.damage_anim = False
		self.kill_anim = False

		self.rect = self.image.get_rect()
		self.rect.centerx = width / 2
		self.rect.centery = height - 80

		self.to_start_anim = False

		self.frame = 0
		self.anim_timer_var = 0

		all_sprites.add(self)

	def update(self):
		if self.anim_timer_var > 2 and self.frame <= len(self.damage_anim_imgs) and self.damage_anim and self.kill_anim == False:
			self.image = self.damage_anim_imgs[self.frame]
			self.frame += 1
			self.anim_timer_var = 0
			if self.frame >= len(self.damage_anim_imgs):
				self.frame = 0
				self.damage_anim = False
		elif self.kill_anim == False:
			self.anim_timer_var += 1

		if self.anim_timer_var > 3 and self.frame <= len(self.kill_anim_imgs) and self.kill_anim == True:
			self.image = self.kill_anim_imgs[self.frame]
			self.frame += 1
			self.anim_timer_var = 0
			if self.frame >= len(self.kill_anim_imgs):
				self.frame = 0
				self.kill()
		else:
			self.anim_timer_var += 1


		keyboard = pygame.key.get_pressed()
		global game_started
		if game_started:
			if keyboard[pygame.K_a]:
				self.rect.x -= 3
			if keyboard[pygame.K_d]:
				self.rect.x += 3
			if keyboard[pygame.K_s]:
				self.rect.y += 1
			if keyboard[pygame.K_w]:
				self.rect.y -= 2

		if self.to_start_anim:
			self.rect.y -= 1
			if self.rect.top < 768 - 190:
				#global game_started
				game_started = True
				self.to_start_anim = False

		if self.rect.right >= 1366:
			self.rect.right = 1366
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= 768:
			self.rect.bottom = 768

class enemy1(pygame.sprite.Sprite): #bird
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((40, 24))
		#self.image.fill((255,0,0))
		self.image = enemy_1_right

		self.frame = 0
		self.anim_timer_var = 0

		self.rect = self.image.get_rect()
		self.rect.centerx = random.choice([1366 + 60, 0 - 60])
		self.rect.centery = random.randint(p.rect.top -  100, p.rect.bottom + 10)
		if self.rect.centerx == 1366 + 60:
			self.speedx = random.randint(-6, -3)
		if self.rect.centerx == 0 - 60:
			self.speedx = random.randint(3, 6)

		if self.rect.centery > p.rect.centery:
			self.speedy = random.randint(-2, 0)
		if self.rect.centery < p.rect.centery:
			self.speedy = random.randint(0, 2)
		if self.rect.centery == p.rect.centery:
			self.speedy = 0

		if self.speedx > 0:
			self.image = enemy_1_right
			self.anim_imgs = enemy_1_anim_right
		else:
			self.image = enemy_1_left
			self.anim_imgs = enemy_1_anim_left

		e_manager.enemy_list.append(self)
		all_sprites.add(self)

	def update(self):
		if self.anim_timer_var > 3 and self.frame <= len(self.anim_imgs):
			self.image = self.anim_imgs[self.frame]
			self.frame += 1
			self.anim_timer_var = 0
			if self.frame >= len(self.anim_imgs):
				self.frame = 0
		else:
			self.anim_timer_var += 1

		self.rect.x += self.speedx 
		self.rect.y += self.speedy
		if self.rect.left > 1366 + 100:
			self.kill()
			e_manager.enemy_list.remove(self)
		if self.rect.right < 0 - 100:
			self.kill()
			e_manager.enemy_list.remove(self)

		collide_with_p = self.rect.colliderect(p)
		global game_started
		if collide_with_p == True and game_started:
			self.kill()
			e_manager.enemy_list.remove(self)
			if len(hb_manager.all_hp) > 0:
				hb_manager.all_hp.remove(hb_manager.all_hp[len(hb_manager.all_hp) - 1])

class enemy2(pygame.sprite.Sprite): #bird
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_2
		self.anim = enemy_2_anim
		self.rect = self.image.get_rect()
		self.rect.centerx = random.choice([p.rect.centerx - 200, p.rect.centerx + 200])
		self.rect.centery = -200
		self.speedx = random.randint(-1,1)

		self.speedy = random.randint(9, 14)

		self.anim_timer_var = 0
		self.frame = 0

		e_manager.enemy_list.append(self)
		all_sprites.add(self)

	def update(self):
		if self.anim_timer_var > 12 and self.frame < len(self.anim) and self.rect.bottom > 0:
			self.image = self.anim[self.frame]
			self.frame += 1
			self.anim_timer_var = 0
		elif self.frame <= len(self.anim) and self.rect.bottom > 0:
			self.anim_timer_var += 1

		self.rect.x += self.speedx 
		self.rect.y += self.speedy
		if self.rect.left > 1366 + 100:
			self.kill()
			e_manager.enemy_list.remove(self)
		if self.rect.right < 0 - 100:
			self.kill()
			e_manager.enemy_list.remove(self)
		if self.rect.top > 768:
			self.kill()
			e_manager.enemy_list.remove(self)

		collide_with_p = self.rect.colliderect(p)
		global game_started
		if collide_with_p == True and game_started:
			self.kill()
			e_manager.enemy_list.remove(self)
			if len(hb_manager.all_hp) > 0:
				hb_manager.all_hp.remove(hb_manager.all_hp[len(hb_manager.all_hp) - 1])

class enemy_manager():
	def __init__(self):
		self.enemy_list = []

		self.timer_to_spawn_new_enemy_var = 0

	def update(self):
		global game_started
		if game_started:
			if len(self.enemy_list) < 4 and self.timer_to_spawn_new_enemy_var > 100:
				self.timer_to_spawn_new_enemy_var = 0
				en = random.choice([enemy1, enemy2])()
			else:
				self.timer_to_spawn_new_enemy_var += 1

class let(pygame.sprite.Sprite): #cloud
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((random.randint(100, 300), random.randint(50,70)))
		#self.image.fill((255,255,255))
		self.width = random.randint(100, 300)
		self.height = random.randint(50,70)
		self.image = random.choice([let1, let2, let2]).copy()
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(150, 1366 - 150)
		self.rect.bottom = 0
		#l_manager.let_list.appen(self)
		all_sprites.add(self)

		spawn_collide = pygame.sprite.spritecollide(self, all_sprites, False)
		for i in spawn_collide:
			if type(i) == let and i != self:
				self.kill()

	def update(self):
		self.rect.y += 2
		if self.rect.top > 768:
			self.kill()

		collide_with_p = self.rect.colliderect(p)
		global game_started
		if collide_with_p == True and game_started:
			self.kill()
			if len(hb_manager.all_hp) > 0:
				hb_manager.all_hp.remove(hb_manager.all_hp[len(hb_manager.all_hp) - 1])

class let_baloon(pygame.sprite.Sprite): #ballon_enemy
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((60, 100))
		#self.image.fill((255,255,255))
		self.image = random.choice([let_ballon1, let_ballon2, let_ballon3])
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(150, 1366 - 150)
		self.rect.bottom = 0
		self.speedy = random.randint(0, 3)
		#l_manager.let_list.appen(self)
		all_sprites.add(self)

		spawn_collide = pygame.sprite.spritecollide(self, all_sprites, False)
		for i in spawn_collide:
			if type(i) == let and i != self:
				self.kill()

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > 768:
			self.kill()

		collide_with_p = self.rect.colliderect(p)
		global game_started
		if collide_with_p == True and game_started:
			self.kill()
			if len(hb_manager.all_hp) > 0:
				hb_manager.all_hp.remove(hb_manager.all_hp[len(hb_manager.all_hp) - 1])

class wind(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((1366, 200))
		#self.image.fill((255,255,255))
		#self.image.set_alpha(100)
		self.image = wind_anim_left[0]
		self.rect = self.image.get_rect()
		self.rect.bottom = 0
		self.speedx = random.randint(-2, 2)

		all_sprites.add(self)

		spawn_collide = pygame.sprite.spritecollide(self, all_sprites, False)
		for i in spawn_collide:
			if type(i) == wind and i != self:
				self.kill()

		if self.speedx == 0:
			self.kill()

		if self.speedx < 0:
			self.anim = wind_anim_left

		if self.speedx > 0:
			self.anim = wind_anim_right

		self.anim_timer_var = 0
		self.frame = 0


	def update(self):
		self.rect.y += 2
		if self.rect.top > 768:
			self.kill()

		if self.anim_timer_var > 3 and self.frame <= len(self.anim):
			self.image = self.anim[self.frame]
			self.frame += 1
			self.anim_timer_var = 0
			if self.frame >= len(self.anim):
				self.frame = 0
		else:
			self.anim_timer_var += 1


		collide_with_p = self.rect.colliderect(p)
		global game_started
		if collide_with_p == True and game_started:
			p.rect.x += self.speedx



class let_manager():
	def __init__(self):
		#self.let_list = []

		self.timer_to_let_spawn_var = 0

		self.timer_var = 100

	def update(self):
		global game_started
		if game_started:
			if self.timer_to_let_spawn_var >= self.timer_var:
				self.timer_var = random.randint(100, 200)
				randnum = random.randint(1, 3)
				for i in range(randnum):

					if d_manager.timer_var < 100:
						l = let_baloon()

					if d_manager.timer_var > 100:
						l = let()

					randnum3 = random.randint(0,100)
					if d_manager.timer_var > 100:
						if randnum3 < 35:
							l = let_baloon()


					randnum2 = random.randint(0,100)
					if randnum2 < 6:
						w = wind()

				self.timer_to_let_spawn_var = 0
			else:
				self.timer_to_let_spawn_var += 1

class difficulty_manager():
	def __init__(self):
		self.timer_var = 0

	def update(self):
		global game_started
		if game_started and game_paused == False:
			self.timer_var += 0.1
		draw_text(game_surface, "score: {}".format(str(int(self.timer_var))), 30, 1366 / 2, 20, (182,199,216))

class player_health(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((50,50))
		#self.image.fill((200,0,0))
		self.image = health

		self.anim_imgs = health_anim
		self.anim = False
		self.frame = 0
		self.anim_framerate_var = 0

		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.in_list = True

		health_sprites.add(self)

	def update(self):
		self.in_list = False
		for i in hb_manager.all_hp:
			if i == self:
				self.in_list = True

		if self.in_list == False:
			self.anim = True

		if self.anim == True:
			if self.anim_framerate_var > 3 and self.frame <= len(self.anim_imgs):
				self.image = self.anim_imgs[self.frame]
				self.frame += 1
				self.anim_framerate_var = 0
			else:
				self.anim_framerate_var += 1

			if self.frame >= len(self.anim_imgs):
				self.kill()

class health_bar_manager(pygame.sprite.Sprite):
	def __init__(self):
		self.first_hp_pos = [1366 / 2 - 100, 80]
		self.second_hp_pos = [1366 / 2, 80]
		self.third_hp_pos = [1366 / 2 + 100, 80]

		self.hp_1 = player_health(self.first_hp_pos[0], self.first_hp_pos[1])
		self.hp_2 = player_health(self.second_hp_pos[0], self.second_hp_pos[1])
		self.hp_3 = player_health(self.third_hp_pos[0], self.third_hp_pos[1])

		self.all_hp = [self.hp_1, self.hp_2, self.hp_3]

		self.last_health_num = 3

	def update(self):

		difference = self.last_health_num - len(self.all_hp)
		if difference > 0:
			p.damage_anim = True
			ballon_hit_sound.play()

		self.last_health_num = len(self.all_hp)

		if len(self.all_hp) == 0:
			p.kill_anim = True
			global game_started
			game_started = False
			b_start_new_game = button_start_new_game()

class pause_switcher():
	def __init__(self):
		self.switch = False
		self.after_press_timer = 0

	def update(self):
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_ESCAPE] and self.after_press_timer <= 0 and game_started:
			self.after_press_timer = 20
			self.switch = True
		if self.after_press_timer > 0:
			self.after_press_timer -= 1

		global game_paused
		if game_paused:
			draw_text(game_surface, "PAUSE", 100, 1366 / 2, 768 - 100, (154,188,221))
			draw_text(game_surface, "press 'x' to left the game", 40, 1366 / 2, 768 - 200, (154,188,221))


		if self.switch == True:
			self.switch = False
			if game_paused == True:
				game_paused = False
			elif game_paused == False:
				game_paused = True

class ground(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = ground_image
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 768 - 200

		self.timer_var = 0
		self.down = False

		all_sprites.add(self)

	def update(self):
		if self.timer_var > 300:
			self.down = True
		else:
			self.timer_var += 1

		global game_started
		if game_started and self.down:

			self.rect.y += 1
			if self.rect.top >= 768:
				self.kill()

class wsda_controls(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = wsda_controls_image
		self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = 300
		all_sprites.add(self)

class esc_controls(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = esc_controls_image
		self.rect = self.image.get_rect()
		self.rect.x = 1366 - 100 - self.rect.width
		self.rect.y = 300
		all_sprites.add(self)

class x_controls(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = left_the_game_controls
		self.rect = self.image.get_rect()
		self.rect.centerx = 1366 / 2
		self.rect.y = 30
		all_sprites.add(self)

class backg(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = background_image
		self.rect = self.image.get_rect()
		background.add(self)

this_directory = os.path.join(os.path.dirname(__file__))

"""class game_graphics():
	def __init__(self):
		self.background = pygame.image.load(os.path.join(this_directory, "sprites\\background.png")).convert_alpha()
		self.let_ballon1 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy1.png")).convert_alpha()
		self.let_ballon2 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy2.png")).convert_alpha()
		self.let_ballon3 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy3.png")).convert_alpha()
		self.player = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_player.png")).convert_alpha()
		self.bp_damage_anim = []
		for i in range(1, 7):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\bp_damage_anim{}.png".format(i))).convert_alpha()
			#print(i)
			self.bp_damage_anim.append(image)
		self.bp_kill_anim = []
		for i in range(1, 4):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\bp_kill_anim{}.png".format(i))).convert_alpha()
			#print(i)
			self.bp_kill_anim.append(image)

		self.enemy_1_left = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_left.png")).convert_alpha()
		self.enemy_1_anim_left = []
		for i in range(1, 6):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_anim{}_left.png".format(i))).convert_alpha()
			#print(i)
			self.enemy_1_anim_left.append(image)

		self.enemy_1_right = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_right.png")).convert_alpha()
		self.enemy_1_anim_right = []
		for i in range(1, 6):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_anim{}_right.png".format(i))).convert_alpha()
			#print(i)
			self.enemy_1_anim_right.append(image)

		self.enemy_2_anim = []
		self.enemy_2 = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_2.png")).convert_alpha()
		for i in range(1, 4):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_2_anim{}.png".format(i))).convert_alpha()
			#print(i)
			self.enemy_2_anim.append(image)

		self.health = pygame.image.load(os.path.join(this_directory, "sprites\\health.png")).convert_alpha()
		self.health_anim = []
		for i in range(1, 4):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\health_anim{}.png".format(i))).convert_alpha()
			#print(i)
			self.health_anim.append(image)

		self.ground = pygame.image.load(os.path.join(this_directory, "sprites\\ground.png")).convert_alpha()

		self.let1 = pygame.image.load(os.path.join(this_directory, "sprites\\let1.png")).convert_alpha()
		self.let2 = pygame.image.load(os.path.join(this_directory, "sprites\\let2.png")).convert_alpha()
		self.let3 = pygame.image.load(os.path.join(this_directory, "sprites\\let3.png")).convert_alpha()

		self.wsda_controls = pygame.image.load(os.path.join(this_directory, "sprites\\controls_show.png")).convert_alpha()
		self.esc_controls = pygame.image.load(os.path.join(this_directory, "sprites\\pause_show.png")).convert_alpha()
		self.left_the_game_controls = pygame.image.load(os.path.join(this_directory, "sprites\\left_the_game.png")).convert_alpha()

		self.button_start = pygame.image.load(os.path.join(this_directory, "sprites\\button_start.png")).convert_alpha()
		self.button_restart = pygame.image.load(os.path.join(this_directory, "sprites\\button_restart.png")).convert_alpha()

		self.wind_anim_left = []
		for i in range(1, 7):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\wind_anim{}_left.png".format(i))).convert_alpha()
			#print(i)
			self.wind_anim_left.append(image)

		self.wind_anim_right = []
		for i in range(1, 7):
			image = pygame.image.load(os.path.join(this_directory, "sprites\\wind_anim{}_right.png".format(i))).convert_alpha()
			#print(i)
			self.wind_anim_right.append(image)"""

"""class game_sounds():
	def __init__(self):
		self.ballon_hit = pygame.mixer.Sound(os.path.join(this_directory, "sounds\\ballon_hit.wav"))
		self.comp_1 = pygame.mixer.music.load(os.path.join(this_directory, "sounds\\comp_1.mp3"))"""



background_image = pygame.image.load(os.path.join(this_directory, "sprites\\background.png")).convert_alpha()
let_ballon1 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy1.png")).convert_alpha()
let_ballon2 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy2.png")).convert_alpha()
let_ballon3 = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_enemy3.png")).convert_alpha()
player_image = pygame.image.load(os.path.join(this_directory, "sprites\\ballon_player.png")).convert_alpha()

bp_damage_anim = []
for i in range(1, 7):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\bp_damage_anim{}.png".format(i))).convert_alpha()
	bp_damage_anim.append(image)

bp_kill_anim = []
for i in range(1, 4):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\bp_kill_anim{}.png".format(i))).convert_alpha()
	bp_kill_anim.append(image)

enemy_1_left = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_left.png")).convert_alpha()
enemy_1_anim_left = []
for i in range(1, 6):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_anim{}_left.png".format(i))).convert_alpha()
	enemy_1_anim_left.append(image)

enemy_1_right = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_right.png")).convert_alpha()
enemy_1_anim_right = []
for i in range(1, 6):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_1_anim{}_right.png".format(i))).convert_alpha()
	enemy_1_anim_right.append(image)

enemy_2_anim = []
enemy_2 = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_2.png")).convert_alpha()
for i in range(1, 4):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\enemy_2_anim{}.png".format(i))).convert_alpha()
	enemy_2_anim.append(image)

health = pygame.image.load(os.path.join(this_directory, "sprites\\health.png")).convert_alpha()
health_anim = []
for i in range(1, 4):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\health_anim{}.png".format(i))).convert_alpha()
	health_anim.append(image)

ground_image = pygame.image.load(os.path.join(this_directory, "sprites\\ground.png")).convert_alpha()

let1 = pygame.image.load(os.path.join(this_directory, "sprites\\let1.png")).convert_alpha()
let2 = pygame.image.load(os.path.join(this_directory, "sprites\\let2.png")).convert_alpha()
let3 = pygame.image.load(os.path.join(this_directory, "sprites\\let3.png")).convert_alpha()

wsda_controls_image = pygame.image.load(os.path.join(this_directory, "sprites\\controls_show.png")).convert_alpha()
esc_controls_image = pygame.image.load(os.path.join(this_directory, "sprites\\pause_show.png")).convert_alpha()
left_the_game_controls = pygame.image.load(os.path.join(this_directory, "sprites\\left_the_game.png")).convert_alpha()

button_start = pygame.image.load(os.path.join(this_directory, "sprites\\button_start.png")).convert_alpha()
button_restart = pygame.image.load(os.path.join(this_directory, "sprites\\button_restart.png")).convert_alpha()

wind_anim_left = []
for i in range(1, 7):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\wind_anim{}_left.png".format(i))).convert_alpha()
	wind_anim_left.append(image)

wind_anim_right = []
for i in range(1, 7):
	image = pygame.image.load(os.path.join(this_directory, "sprites\\wind_anim{}_right.png".format(i))).convert_alpha()
	wind_anim_right.append(image)

ballon_hit_sound = pygame.mixer.Sound(os.path.join(this_directory, "sounds\\ballon_hit.wav"))
comp_1 = pygame.mixer.music.load(os.path.join(this_directory, "sounds\\comp_1.wav"))

#gs = game_sounds()
#gg = game_graphics()

game_paused = False
game_started = False
running = True

g = ground()
bg = backg()

l_manager = let_manager()
e_manager = enemy_manager()
d_manager = difficulty_manager()
hb_manager = health_bar_manager()

ps_manager = pause_switcher()

p = player()

b_play = button_play()

pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops= -1)

pygame.mouse.set_visible(False)

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				running = False
		
	#window.blit(gg.background, (0,0))
	#window.fill((0,0,0))

	background.draw(game_surface)

	menu_sprites.update()
	menu_sprites.draw(game_surface)

	if game_paused == False:
		all_sprites.update()

		e_manager.update()
		l_manager.update()
		hb_manager.update()

	all_sprites.draw(game_surface)

	d_manager.update()
	ps_manager.update()

	health_sprites.update()
	if game_started:
		health_sprites.draw(game_surface)

	real_fps = int(clock.get_fps())
	draw_text(game_surface, str(real_fps), 20, 20, 20, (255,255,255))
	#draw_text(game_surface, str(all_sprites), 15, 1300, 20, (255,255,255))
	
	fullscreen_with_ratio()

	pygame.display.flip()

	clock.tick(fps)