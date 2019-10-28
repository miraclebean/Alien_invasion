# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Sprite

'''子弹精灵'''
class Bullet(Sprite):
    '''一个对飞船发射子弹进行管理的类'''

    def __init__(self, ai_settings, screen, ship):
        '''在飞船所处的位置创建子弹对象'''
        super(Bullet, self).__init__()
        self.screen = screen

        '''在(0, 0)处创建子弹对象，并将其移到飞船位置'''
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        '''存储用小数表示的子弹位置'''
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed__factor = ai_settings.bullet_speed_factor

    def update(self):
        '''向上移动子弹'''
        '''更新表示子弹移动的y值'''
        self.y -= self.speed__factor
        '''更新rect,y'''
        self.rect.y = self.y

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen, self.color, self.rect)