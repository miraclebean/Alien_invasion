# -*- coding:utf-8 -*-

import sys
import pygame
from bullets import Bullet
from alien import Alien
from pygame.sprite import Sprite
import time



def check_keydown_events(ai_settings, event, screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        '''更新移动标志'''
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        '''创建一个子弹，并将其加入到编组中，若未消失子弹数目小于设定值则发射'''
        fire_bullets(ai_settings, bullets, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    '''响应松开按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    '''响应按键以及鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # 对于每个按键注册为KEYDOEWN事件并判断其类型
            check_keydown_events(ai_settings, event, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    '''在玩家单击play按钮且此时游戏状态为False时才开始游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        '''重置游戏设置'''
        ai_settings.initialize_dynamic_settings()

        '''隐藏光标'''
        pygame.mouse.set_visible(False)

        '''重置游戏统计信息'''
        stats.reset_stats()
        stats.game_active = True

        '''在点击play按钮之后清空外星人和子弹'''
        aliens.empty()
        bullets.empty()

        '''重置记分牌图像'''
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        '''创建新外星人，并将飞船居中'''
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullets(ai_settings, bullets, screen, ship):
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    screen.fill(ai_settings.bg_color)

    '''在飞船和外星人后面绘制所有子弹'''
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    '''显示得分'''
    sb.show_score()

    '''在游戏非活动状态时显示play按钮'''
    if not stats.game_active:
        play_button.draw_button()

    '''让最近的屏幕可见'''
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''更新子弹位置，并删除消失的子弹'''
    bullets.update()  # 更新子弹位置

    '''删除消失的子弹'''
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens, stats, sb):
    '''检查是否有子弹与外星人碰撞，如果碰撞，则删除响应的外星人和子弹'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    '''子弹撞到外星人时加分并更新图像，且将每个被消灭的外星人都计入分数'''
    '''字典collisions中，与外星人碰撞的子弹是键，其值为被子弹击中的外星人，遍历collisions中的值，将其中的每个外星人的分
    数都记上'''
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_highest_score(stats, sb)

    if len(aliens) == 0:
        '''删除现有的子弹并新建一批外星人'''
        bullets.empty()
        ai_settings.increase_speed()

        '''提升等级'''
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    '''计算每一行可以容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number ):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕上能容纳多少行外星人'''
    available_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_y/(2 * alien_height))
    return number_rows


def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    '''创建一个外星人，并计算每行能容纳多少个'''
    '''外星人间距为外星人宽'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)


    '''创建第一行外星人'''
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            '''创建一个外星人并将其加入当前行'''
            alien = Alien(ai_settings, screen)
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    '''有外星人到达边缘时采取的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''将整群外星人下移并改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        '''将ships_left减1'''
        stats.ships_left -= 1

        '''清空外星人列表和子弹列表'''
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        sb.prep_ships()

        '''创建一群新的外星人，并把飞船放到屏幕中央'''
        create_fleet(ai_settings, screen, ship, aliens)


        '''暂停一段时间'''
        time.sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人到达底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            '''碰到底部与碰到飞船一样处理'''
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def update_aliens(ai_settings, stats, aliens, ship, screen, bullets, sb):
    '''更新外星人位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    '''检测外星人和飞船之间的碰撞，若为真，则停止游戏'''
    if pygame.sprite.spritecollide(ship, aliens, True):
       ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    '''检查外星人是否到达屏幕底端'''
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_highest_score(stats, sb):
    '''检测是否产生了最高分'''
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        sb.prep_highest_score()


