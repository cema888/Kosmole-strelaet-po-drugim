#Создай собственный Шутер!
from pygame import *
from random import *

font.init()
mixer.init()
sizeX = 700
sizeY = 500
window = display.set_mode((sizeX, sizeY))
kick = mixer.Sound("fire.ogg")
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.music.load("space.ogg")
mixer.music.play()
clock = time.Clock()
FPS = 60
game = True
finish = False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, ix, iy):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (ix, iy))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):

    def move(self, keys):
        dx, dy = 0, 0
        if keys[K_LEFT] or keys[K_a]:
            dx = -self.speed
        if keys[K_RIGHT] or keys[K_d]:
            dx = self.speed

        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(window.get_rect())
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 20, 25)
        bullets.add(bullet)
        kick.play()
skipEnemy = 0

class Enemy(GameSprite):
    def update(self):
        global skipEnemy
        if self.rect.y < 449:  
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 625)
            skipEnemy += 1
            self.speed = randint(1, 2)
bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
font2 = font.SysFont("Arial", 36)
font1 = font.SysFont("Arial", 52)
text_lose = font2.render("Пропущено: " + str(skipEnemy), 1, (255, 255, 255))
enemies = sprite.Group()
asteroides = sprite.Group()
enemy1 = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
enemy2 = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
enemy3 = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
enemy4 = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
enemy5 = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
asteroid = Enemy("asteroid.png", randint(75, 625), 0, 1.5, 75, 50)
asteroides.add(asteroid)
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)
player = Player("rocket.png", 300, 400, 5, 75, 100)
score = 0
lose = font1.render("ВЕЛИКИЙ lose", 1, (255, 0, 0))
win = font1.render("ВЕЛИКИЙ win", 1, (0, 255, 0))
while game:
    
    if finish != True:
        
        
        keys = key.get_pressed()
        window.blit(background, (0, 0))
        player.reset()
        player.move(keys)
        asteroid.update()
        asteroid.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose = font2.render("Пропущено: " + str(skipEnemy), 1, (255, 255, 255))
        text_kill = font2.render("Cчёт: " + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (0, 0))
        window.blit(text_kill, (0, 50))
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy("ufo.png", randint(75, 625), 0, randint(1, 2), 75, 50)
            enemies.add(enemy)
        if sprite.spritecollide(player, asteroides, False) or sprite.spritecollide(player, enemies, False) or skipEnemy >= 3:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    clock.tick(FPS)
    display.update()
