#Создай собственный Шутер!

from pygame import *
from random import randint
from time import  time  as timer

#создаю  окно игры
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
  


clock = time.Clock()
FPS = 80
lost = 0
score = 0
max_lost = 100
max_score = 20
life = 3

# Перезарядка йоу 
rel_time = False  
num_fire = 0

font.init()
font1 = font.SysFont('Arial', 32)
# lose = font1.render('Проиграл!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 65)
win = font2.render('Выйграл!', True, (153, 0, 204))
lose = font2.render('Проиграл!', True, (102, 255, 255))

# text = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y , player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(("bullet.png"), self.rect.centerx, self.rect.top, -15, 20, 20 )
        bullets.add(bullet)
       
       

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    



class Enemy1(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.x = randint(5, 800)
            self.rect.y = 0
            lost += 1
        
        


bullets = sprite.Group()


player = Player(("rocket.png"), 300, 400 , 3, 70, 80)

monsters = sprite.Group()
for i in range(1, 9):
    enemy_test = Enemy1(('ufo.png'), randint(0, 800), 0, randint(1, 3), 60, 60) 
    monsters.add(enemy_test)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy1(('asteroid.png'), randint(0,800), 0, randint(1, 2), 70, 70)
    asteroids.add(asteroid)


back_y = 0
finish = False
game = True
while game:




   
    

  

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
            
                if num_fire < 15  and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()

                if num_fire >= 15 and rel_time == False:
                    last_timer = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, back_y))
        window.blit(background, (0, back_y - 500))


        back_y += 0.25
        if back_y == 500:
            back_y = 0

        if rel_time == True:
            now_timer = timer()

            if now_timer - last_timer < 2:
                reload =  font2.render('Перезарядка', 1 ,(220, 220, 0))
                window.blit(reload, (390, 430))
            else:
                rel_time = False
                num_fire = 0
 
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font1.render('Количество жизней:'  +str(life), 1, life_color)
        window.blit(text_life, (500-10, 20))



        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        wintext = font1.render('Попаданий:' + str(score), 1, (255, 255, 255))
        losetext = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(wintext, (20, 40))
        window.blit(losetext, (20, 70))


        collides =sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            enemy_test = Enemy1(('ufo.png'), randint(0, 800), 0, randint(1, 3), 60, 60) 
            monsters.add(enemy_test)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1  
        
        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (250, 200))
        
        if score >= max_score:
            finish = True 
            window.blit(win, (225,200))
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        for b in bullets:
            b.kill()
        for a in monsters:
            a.kill()
        for c in asteroids:
            c.kill()

        time.delay(3000)

        for i in range(1, 9):
            enemy_test = Enemy1(('ufo.png'), randint(0, 800), 0, randint(1, 3), 60, 60) 
            monsters.add(enemy_test)

        for i in range(1, 3):
            asteroid = Enemy1(('asteroid.png'), randint(0,800), 0, randint(1, 2), 70, 70)
            asteroids.add(asteroid)


    clock.tick(FPS)
    display.update()