import pygame
import tmx

class Player(pygame.sprite.Sprite):
	def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
		self.image = pygame.image.load('tiles/player.png')
		self.imageDefault = self.image.copy()
		self.rect = pygame.Rect(location, (64,64))
		self.orient = 'down' 
		self.holdTime = 0
		self.walking = False
		self.dx = 0
		self.step = 'rightFoot'
		
	def setSprite(self):
		# Resets the player sprite sheet to its default position 
		# and scrolls it to the necessary position for the current orientation
		self.image = self.imageDefault.copy()
		if self.orient == 'up':
			self.image.scroll(0, -64)
		elif self.orient == 'down':
			self.image.scroll(0, 0)
		elif self.orient == 'left':
			self.image.scroll(0, -128)
		elif self.orient == 'right':
			self.image.scroll(0, -192)
		
	def update(self, dt, game):
		key = pygame.key.get_pressed()
		# Setting orientation and sprite based on key input: 
		if key[pygame.K_UP]:
			if not self.walking:
				if self.orient != 'up':
					self.orient = 'up'
					self.setSprite()
				self.holdTime += dt
		elif key[pygame.K_DOWN]:
			if not self.walking:
				if self.orient != 'down':
					self.orient = 'down'
					self.setSprite()	
				self.holdTime += dt
		elif key[pygame.K_LEFT]:
			if not self.walking:
				if self.orient != 'left':
					self.orient = 'left'
					self.setSprite()
				self.holdTime += dt
		elif key[pygame.K_RIGHT]:
			if not self.walking:
				if self.orient != 'right':
					self.orient = 'right'
					self.setSprite()
				self.holdTime += dt
		else:
			self.holdTime = 0
			self.step = 'rightFoot'
		# Walking mode enabled if a button is held for 0.1 seconds
		if self.holdTime >= 100:
			self.walking = True
		# Walking at 8 pixels per frame in the direction the player is facing 
		if self.walking and self.dx < 64:
			if self.orient == 'up':
				self.rect.y -= 8
				self.dx += 8
			elif self.orient == 'down':
				self.rect.y += 8
				self.dx += 8
			elif self.orient == 'left':
				self.rect.x -= 8
				self.dx += 8
			elif self.orient == 'right':
				self.rect.x += 8
				self.dx += 8
			pygame.transform.flip(self.image, True, True)
		# Switch to the walking sprite after 32 pixels 
		if self.dx == 32:
			# Self.step keeps track of when to flip the sprite so that
			# the character appears to be taking steps with different feet.
			if (self.orient == 'up' or 
				self.orient == 'down') and self.step == 'leftFoot':
				self.image = pygame.transform.flip(self.image, True, False)
				self.step = 'rightFoot'
			else:
				self.image.scroll(-64, 0)
				self.step = 'leftFoot'
		# After traversing 64 pixels, the walking animation is done
		if self.dx == 64:
			self.walking = False
			self.setSprite()	
			self.dx = 0
		
		game.tilemap.set_focus(self.rect.x, self.rect.y)
		
class Game(object):
	def main(self, screen):
		clock = pygame.time.Clock()

		self.tilemap = tmx.load('palletTown.tmx', screen.get_size())
		self.sprites = tmx.SpriteLayer()
		start_cell = self.tilemap.layers['triggers'].find('playerStart')[0]
		self.player = Player((start_cell.px, start_cell.py), self.sprites)
		self.tilemap.layers.append(self.sprites)		
			
		while 1:
			dt = clock.tick(30)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return

			self.tilemap.update(dt, self)
			screen.fill((255,255,255))
			self.tilemap.draw(screen)
			pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	Game().main(screen)