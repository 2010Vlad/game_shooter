from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((700, 500))


font.init()
font1 = font.Font(None, 70)
win = font1.render("Браво", True,(0,255,0 ))
lose = font1.render("Я не удивлен", True,(255,0,0))
font2 = font.Font(None, 40)
#text_score = font2.render("Счет:", True)
background = "background.jpg"

lost = 0

mixer.init()
mixer.music.load('sigma.mp3')
mixer.music.play()
# dmg_sound = mixer.Sound('trevoga.mp3')
# boom = mixer.Sound('vzryv.mp3')
# fire_sound = mixer.Sound('vestrel.mp3')


FPS = 60
game = True
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        global last_time
        global rel_time
        global num_fire
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
        if keys[K_SPACE]:
            if num_fire < 5 and rel_time == False: 
                num_fire += 1
                # fire_sound.play()
                self.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
    def fire(self):
       bullet = Bullet("pyli.png", self.rect.centerx, self.rect.top, 10, 20, 10)
       bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width-50)
            lost = lost + 1

class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
         
bullets = sprite.Group()
score = 0
goal = 100

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(background), (win_width, win_height))

background = GameSprite('background.jpg', 0,0,0,700,500)
pvo = Player('pvo.png', 600,400,5,70,80)
boss = Boss('bomba.png', randint(50, win_width-500), 5,10, 100,100)
enemys = sprite.Group()
for i in range(8):
    enemy = Enemy('bomba.png', randint(50, win_width-500),10,5,50,50)
    enemys.add(enemy)

finish = False
run = True
last_time = 0
num_fire = 0
rel_time = False
life = 3
boss_hp = 10
#start_game = timer()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    text_score = font2.render("Счет:"+str(score), True, (255,255,255))
    text_lose = font2.render('Потерь:'+str(lost), True,(255,255,255))
    text_life = font2.render("Жизни:"+str(life), True, (255, 100, 100))

    collide = sprite.groupcollide(enemys, bullets, True, True)
    if collide:
        # boom.play()
        pass
    for c in collide:
        score += 1
        enemy = Enemy("bomba.png", randint(50,win_width-50), 10, 5, 50, 50)
        enemys.add(enemy)

    if not finish:
        background.reset()
        window.blit(text_score, (10,30))
        window.blit(text_lose, (10,0))
        window.blit(text_life, (10,50))
        enemys.update()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                amon = font2.render("Reload", 1, (255, 0, 100))
                window.blit(amon,(260,460))
            else:
                num_fire =  0
                rel_time = False
        enemys.draw(window)
        bullets.draw(window)
        pvo.update()
        if score >= 1:
            boss.reset()
            boss.update()
        if score > 100:
            boss.reset()
        pvo.reset()
        bullets.update()
        #события
        if sprite.spritecollide(pvo, enemys, True) or lost >= 30:
            # dmg_sound.play()
            life -= 1
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        if life <= 0:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(boss, bullets, True):
            boss_hp -= 1
        if boss_hp <= 0:
            boss.kill
        display.update()
    time.delay(50)