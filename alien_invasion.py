# -*- coding:utf-8 -*-

import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf  # 将函数文件导入
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    '''初始化游戏,设置并创建一个屏幕对象'''
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    '''创建一个用于统计游戏信息的实例'''
    stats = GameStats(ai_settings)

    '''创建游戏记分牌'''
    sb = ScoreBoard(screen, ai_settings, stats)

    '''创建一艘飞船, 一个子弹编组和一个外星人编组'''
    ship = Ship(ai_settings, screen)

    '''创建用于储存子弹和外星人的编组'''
    bullets = Group()
    aliens = Group()

    '''创建外星人群'''
    gf.create_fleet(ai_settings, screen, ship, aliens)

    '''创建play按钮'''
    play_button = Button(ai_settings, screen, 'Play')

    '''开始游戏的主循环'''
    while True:

        '''监视键盘鼠标事件'''
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)

        if stats.game_active:
            ship.update()

            '''更新子弹位置并删除已经消失的子弹'''
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb)

            '''更新外星人位置'''
            gf.update_aliens(ai_settings, stats, aliens, ship, screen, bullets, sb)

        '''每次循环时重绘背景'''
        gf.update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb)


run_game()
