# -*- coding:utf-8 -*-

class Settings():
    '''存储《外星人入侵》的所有设置的类'''

    def __init__(self):
        '''初始化游戏的设置'''
        '''飞船和屏幕设置'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.ship_limit = 3

        '''子弹设置'''
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3  # 屏幕可容纳的子弹数目

        '''外星人设置'''
        self.fleet_drop_speed = 10

        '''以什么速度加快游戏节奏'''
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):

        '''初始化随游戏变化的设置'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5

        '''记分'''
        self.alien_points = 50


        '''fleet_direction为1表示右移，-1表示左移'''
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
