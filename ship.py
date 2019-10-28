# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        '''初始化飞船并设置其初始位置'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        '''加载飞船图像并获取其外接矩形'''
        self.image = pygame.image.load('images/ship.bmp')
        '''原图图像过大，按比例缩小至适合大小'''
        width, height = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (width // 27, height // 27))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()  # 存储表示屏幕的矩形

        '''将每艘飞船置于屏幕底部中央'''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        '''在飞船的属性center中储存小数值,因为rect只支持'''
        self.center = float(self.rect.centerx)
        self.center_up = float(self.rect.centery)

        '''移动标志，用于持续移动判断'''
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        '''根据移动标志调整飞船位置'''
        '''更新飞船的center以及center_up值，而非rect'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.center_up -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_up += self.ai_settings.ship_speed_factor

        '''更新self.center对象更新rect'''
        self.rect.centerx = self.center
        self.rect.centery = self.center_up

    def blitme(self):
        '''在指定位置绘制飞机'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''将飞船重置在屏幕底部中间'''
        self.center = self.screen_rect.centerx
        self.center_up = self.screen_rect.bottom
        self.rect.centerx = self.center
        self.rect.centery = self.center_up





