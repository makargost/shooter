from pygame import *
from random import randint
import time as tf
# ! The main class of game
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
# * Class of player
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 960:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
# ? Class of Enemy
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > 768:
            self.rect.y = 0
            self.rect.x = randint(5, 960)
            lost += 1
# todo Class of Bullets
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()
class Button_PNG():
    def __init__(self, btn_image, x, y, w, h):
        self.image = transform.scale(image.load(btn_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        self.pressed = False
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
win = display.set_mode((1024, 768))
display.set_caption('Shooter')
background = transform.scale(image.load('1082.jpg'), (1024, 768))

player = Player('rocket.png', 512, 698, 65, 65, 5)
player.reset()

enemies = sprite.Group()
for i in range(5):
    enemy1 = Enemy('ufo.png', randint(5, 960), 50, 80, 45, randint(1, 3))
    enemies.add(enemy1)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid1 = Enemy('asteroid.png', randint(5, 960), 50, 80, 45, randint(3, 5))
    asteroids.add(asteroid1)
lost = 0
win_amount = 0
lives = 3

num_fire = 0
rel_time = False

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)
font3 = font.SysFont('Arial', 60)

text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
text_score = font1.render('Счет:' + str(win_amount), 1, (255, 255, 255))
text_lives = font3.render(str(lives), 1, (0, 255, 0))
text_pause = font1.render('Пауза (для старта нажмите S)', 1, (255, 0, 0))

btn_pause = Button_PNG('pause.png', 512, 10, 128//2, 128//2)

fps = 60
run = True
finish = False
clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.2)

full_fire = False
while run:
    
    if not finish:
        win.blit(background, (0, 0))

        player.reset()
        player.update()

        enemies.draw(win)
        enemies.update()

        bullets.draw(win)
        bullets.update()

        asteroids.draw(win)
        asteroids.update()

        btn_pause.reset()

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for collide in collides:
            win_amount += 1
            enemy1 = Enemy('ufo.png', randint(5, 960), 50, 80, 45, randint(1, 3))
            enemies.add(enemy1)
        if win_amount >= 10:
            text_win = font2.render('YOU WIN!', 1, (0, 255, 0))
            win.blit(text_win, (450, 768/2))
            mixer.music.stop()
            finish = True
        if lost >= 5:
            text_game_over = font2.render('GAME OVER!', 1, (255, 0, 0))
            win.blit(text_game_over, (450, 768/2))
            mixer.music.stop()
            finish = True
        for aster in sprite.spritecollide(player, asteroids, False):
            aster.kill()
            lives -= 1
            asteroid1 = Enemy('asteroid.png', randint(5, 960), 50, 80, 45, randint(3, 5))
            asteroids.add(asteroid1)
        for vrag in sprite.spritecollide(player, enemies, False):
            vrag.kill()
            lives -= 1
            enemy1 = Enemy('ufo.png', randint(5, 960), 50, 80, 45, randint(1, 3))
            enemies.add(enemy1)
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Счет:' + str(win_amount), 1, (255, 255, 255))
        text_reload = font1.render('Перезарядка!', 1, (255, 0, 0))
        text_lives = font3.render(str(lives), 1, (0, 255, 0))
        win.blit(text_lose, (0, 25))
        win.blit(text_score, (0, 0))
        win.blit(text_lives, (960, 25))
        if rel_time:
            now_time = tf.time()
            if (now_time-last_time) < 3:
                win.blit(text_reload, (512, 668))
            else:
                num_fire = 0
                rel_time = False
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                full_fire = True
            if e.key == K_p:
                win.blit(text_pause, (450, 768/2))
                finish = True
                mixer.music.stop()
            if e.key == K_s:
                finish = False
                mixer.music.play()
            if e.key == K_r:
                if finish:
                    for enemy in enemies:
                        enemy.kill()
                    for bullet in bullets:
                        bullet.kill()
                    for aster in asteroids:
                        aster.kill()
                    for i in range(5):
                        enemy1 = Enemy('ufo.png', randint(5, 960), 50, 80, 45, randint(1, 3))
                        enemies.add(enemy1)
                    for i in range(3):
                        asteroid1 = Enemy('asteroid.png', randint(5, 960), 50, 80, 45, randint(3, 5))
                        asteroids.add(asteroid1)
                    
                    finish = False
        if e.type == KEYUP:
            if e.key == K_SPACE:
                full_fire = False
        if finish != True or btn_pause.pressed != True:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_pause.collidepoint(x, y):
                    btn_pause.pressed = True
                    if finish != True:
                        mixer.music.pause()
                        finish = True
                        win.blit(text_pause, (450, 768/2))
                        btn_pause.pressed = False
                    elif finish:
                        mixer.music.unpause()
                        finish = False
    if full_fire:
        if num_fire < 5 and rel_time == False:
            fire_sound.play()
            player.fire()
            num_fire += 1
        if num_fire >= 5 and rel_time == False:
            rel_time = True
            last_time = tf.time()
    
    clock.tick(fps)
    display.update()