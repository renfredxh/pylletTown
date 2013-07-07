import pygame
import tmx

class Player(pygame.sprite.Sprite):
	def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
		self.image = pygame.image.load('tiles/player.png')
		self.rect = pygame.Rect(location, (64,64))
		
	def update(self, dt, game):
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			self.rect.x -= 64
		if key[pygame.K_RIGHT]:
			self.rect.x += 64
		if key[pygame.K_UP]:
			self.rect.y -= 64
		if key[pygame.K_DOWN]:
			self.rect.y += 64
		
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

			self.tilemap.update(dt / 1000, self)
			screen.fill((255,255,255))
			self.tilemap.draw(screen)
			pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	Game().main(screen)