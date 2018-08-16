import pygame
from plane_sprites import *

class PlaneGame(object):
    def __init__(self):
        print("游戏初始化")  #自己一直打印不出来的原因竟然是初始化函数写错了，尼玛
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #创建游戏时钟
        self.clock = pygame.time.Clock()
        #调用私有方法
        self._create_sprites()
        # 4 设置定时器方法，创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)

    def _create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)

        #创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        pass

    def start_game(self):
         #print("游戏开始...")

        while True:
            # 1.设置刷新频率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

            pass

    def __event_handler(self): # 事件监听方法
        for event in pygame.event.get():
            #判断是否退出
            if event.type == pygame.QUIT: # 如何调用静态方法，用类名方式
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                #print ("敌机出现。。。")
                # 创建敌机精灵
                enemy =  Enemy()
                # 将敌机精灵添加到精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                # print ("向右移动")

        #用键盘提供的方法获取键盘按键，
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 持续移动
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 1.子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        # 2.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        # 3,判断列表是否有内容
        if len(enemies)>0:
            #让英雄牺牲
            self.hero.kill()
            # end games
            PlaneGame.__game_over()

        pass

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)


    @staticmethod
    def __game_over():
        print("game over")
        pygame.quit()
        exit()


if __name__ == '__main__':  #对空行有严格要求，在类之后必须有两个空行
    #创建对象
    game = PlaneGame()

    #开始游戏
    game.start_game()