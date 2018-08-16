import random
import pygame

#定义屏幕大小常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
FRAME_PER_SEC = 60 #刷新帧率
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT +1   #发射子弹事件

class GameSprite(pygame.sprite.Sprite): #error

    def __init__(self,image_name,speed=1):
        #调用父类的初始化方法
        super().__init__()  #不是object的类，一定要调用一下父类的方法
        self.image=pygame.image.load(image_name) #error
        self.rect = self.image.get_rect()
        self.speed  = speed

    def update(self):
        #在屏幕的垂直方向上移动
        self.rect.y +=self.speed


class Background(GameSprite):

    def __init__(self,is_alt = False):
        # 1 调用父类方法实现精灵的创建
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y =  -self.rect.height

    def update(self):
        # 1. 调用父类的方法实现
        super().update()
        # 2. 判断时候移出屏幕
        if self.rect.y>= SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        pass


class Enemy(GameSprite):
    '''敌机精灵'''
    def __init__(self):
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")
        # 2. 指定敌机的初始随机速度
        self.speed = random.randint(1,3)
        # 3. 指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)


        pass

    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        # 2. 判断是否飞出屏幕，如果是，需要从精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            #kill 方法可以将精灵从精灵组中移出
            self.kill()
            #print ("飞出屏幕，从精灵组删除")

    def __del__(self): #内置方法
        #print("敌机挂了%s"%self.rect)
        pass


class Hero(GameSprite):
    '''英雄精灵'''
    def __init__(self):
        # 1.调用父类方法
        super().__init__("./images/me1.png",0)
        # 2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom =  SCREEN_RECT.bottom-120

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        #英雄在水平方向移动
        self.rect.x += self.speed

        # 判断是否移出屏幕：
        if self.rect.x<0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right =  SCREEN_RECT.right

    def fire(self):
        print("发射子弹")
        #  1 创建子弹精灵
        for i in (0,1,2):
            bullet = Bullet()
            # 2.设置精灵的位置
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.centerx = self.rect.centerx
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet)



class Bullet(GameSprite):

    def __init__(self):
        #调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png",-3)
        pass

    def update(self):
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        if self.rect.bottom <0:
            self.kill()


    def __del__(self):
        print ("")