# -*- coding:utf-8 -*-

import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard():
    def __init__(self, screen, ai_settings, stats):
        '''初始化显示得分的属性'''
        self.screen =screen
        self.screen_rect = screen.get_rect()
        self.ai_settings =ai_settings
        self.stats = stats

        '''显示得分用的字体设置'''
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        '''准备当前得分和最高得分图像以及等级'''
        self.prep_highest_score()
        self.prep_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        '''round通常将小数精确到后几位，而第二个参数则指定小数位数，-1表示圆整到最近的10，100，1000等的整数倍'''
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)  # 将逗号作为千分位分隔符
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        '''将得分放在右上角'''
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 20

    def prep_highest_score(self):
        '''将最高得分渲染为图像'''
        rounded_highest_score = int(round(self.stats.highest_score, -1))
        highest_score_str = "{:,}".format(rounded_highest_score)
        self.highest_score_image = self.font.render(highest_score_str, True, self.text_color, self.ai_settings.bg_color)

        '''将得分放在屏幕顶端中央'''
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.screen_rect.top

    def prep_level(self):
        '''将等级转换为渲染的图像'''
        level_str = str(self.stats.level)
        self.level_str_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        '''将等级放在左上方'''
        self.level_rect = self.level_str_image.get_rect()
        self.level_rect.top = self.score_rect.bottom
        self.level_rect.right = self.screen_rect.right - 20

    def prep_ships(self):
        '''绘制剩余飞船图像'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_rect)
        self.screen.blit(self.level_str_image, self.level_rect)
        self.ships.draw(self.screen)
