import pygame
import random
import os

#基本设置
FPS = 120
WIDTH = 600
HEIGHT= 700
SCREEN_COLOR=(2,25,25)
PLAYER_COLOR=(0,255,0)
TITLE="刘作豪打飞机"

#游戏初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
score = 0
health = 3
running = True
#文字功能实现
#字体
font_name = pygame.font.match_font('arial')
#写字
def draw_txt(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    #渲染字体
    text_surface = font.render(text,True,(255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    #显示
    surf.blit(text_surface,text_rect)
#图片载入
background_img = pygame.image.load(os.path.join("image","background.png")).convert()
player_img = pygame.image.load(os.path.join("image","player.jpg")).convert()
bullet_img = pygame.image.load(os.path.join("image","bullet.jpg")).convert()
rock_img = pygame.image.load(os.path.join("image","rock.jpg")).convert()
#声音载入
pygame.mixer.init()

shoot_sounds = [
    pygame.mixer.Sound(os.path.join("sound","shoot.wav")),
    pygame.mixer.Sound(os.path.join("sound","shoot1.wav")),
    pygame.mixer.Sound(os.path.join("sound","shoot2.wav")),
    pygame.mixer.Sound(os.path.join("sound","shoot3.wav"))
]
rock_sound = pygame.mixer.Sound(os.path.join("sound","rock.mp3"))
hit_sound = pygame.mixer.Sound(os.path.join("sound","hit.mp3"))
pygame.mixer.Sound.set_volume(rock_sound,0.2)

#背景音乐
pygame.mixer.music.load(os.path.join("sound","background.mp3"))
pygame.mixer.music.set_volume(0.4)
#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(100,60))
        self.health = health
        self.hidden = False

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 30
        self.speedx = 6
        self.speedy = 6
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d] and self.rect.right < WIDTH-1:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a] and self.rect.left > 1:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_s] and self.rect.bottom < HEIGHT-1:
            self.rect.y += self.speedy
        if key_pressed[pygame.K_w] and self.rect.top > 1:
            self.rect.y -= self.speedy
        if self.hidden == True and pygame.time.get_ticks() - self.hide_time > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

    def Shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        random.choice(shoot_sounds).play()
    def Hide(self):
        player.health = health
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+500)
#陨石
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = pygame.transform.scale(rock_img,(50,50))
        self.image_origin.set_colorkey((255,255,255))
        self.image = self.image_origin.copy()

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1,WIDTH-self.rect.width)
        self.rect.y = random.randint(-100,-40)

        self.speedy = random.randint(2,4)
        self.speedx = random.randint(-2,2)

        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randint(1, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100,-40)
            self.speedy = random.randint(2, 4)
            self.speedx = random.randint(-2, 2)
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_origin,self.total_degree)
        #重新寻找中心位置定位/避免鬼畜
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
#子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(20,40))
        #将白色透明化
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#存放列表
all_sprites=pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
#玩家
player = Player()
all_sprites.add(player)
#生成陨石
for i in range(6):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)
#播放背景声音
pygame.mixer.music.play(-1)

#重启游戏（妈的未响应了）
def ReStart():
    key_pressed = pygame.key.get_pressed()
    if key_pressed == pygame.K_b:
        player.Hide()
def Count():
    init_time = pygame.time.get_ticks()
    time = pygame.time.get_ticks() + 1
    while time - init_time <= 10000:
        draw_txt(screen, "PRESS 'B' TO RESTART",40, WIDTH / 2, HEIGHT / 2)
        draw_txt(screen, str((time - init_time) / 1000), 40, WIDTH / 2, HEIGHT / 2 + 50)
        ReStart()
        time = pygame.time.get_ticks()
#游戏循环
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.Shoot()
    #更新游戏
    all_sprites.update()
    #子弹碰撞检测
    hits_rocks_bullets = pygame.sprite.groupcollide(rocks,bullets,True,True)
    #将被击中的陨石重新生成
    for hit in hits_rocks_bullets:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
        rock_sound.play()
        score += 1
    #陨石与玩家碰撞
    hits_rocks_player = pygame.sprite.spritecollide(player,rocks,True)
    for hit in hits_rocks_player:
        player.health = player.health - 1
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)
        hit_sound.play()
        if player.health <= 0:
            #若10秒无操作则退出游戏
            #Count()
            running = False
    #显示画面
    screen.fill(SCREEN_COLOR)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_txt(screen,"Chicken:"+str(score),38,WIDTH/2,40)
    draw_txt(screen, "Health:" + str(player.health), 38, 80, HEIGHT-40)
    pygame.display.update()

pygame.quit()