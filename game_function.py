# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : game_function.py
# @Time    : 2019/8/28 17:43

import sys

import pygame
from bullet import Bullet
from alines import Alien
from time import sleep


def check_keydown_events(event, ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullets_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    # keys and mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y)


def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    # click the play button and then the game begin
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game's setting
        ai_setting.initialize_dynamic_settings()
        # cover the mouse
        pygame.mouse.set_visible(False)
        # reset the game's information
        stats.reset_stats()
        stats.game_active = True

        # reset the scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # clean the alien's and the bullet's list
        aliens.empty()
        bullets.empty()

        # create a group of aliens and put the ship on the center
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_setting.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.drawme()
    aliens.draw(screen)
    sb.show_score()
    # if the game is not active, it will draw the play button
    if not stats.game_active:
        play_button.draw_button()
    # show the new screen
    pygame.display.flip()


def update_bullet(ai_setting, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    # delete the missing bullet
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # detect if there are aliens killed by bullets or not
    # if killed we delete bullets and corresponding aliens
    check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_setting, screen, ship, aliens)


def get_number_alien_x(ai_setting, alien_width):
    # calculate how many aliens can stay in a row
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_rows(ai_setting, ship_height, alien_height):
    # calculate how many rows' alien can stay in the screen
    available_space_y = (ai_setting.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    # create a alien and put it on the current line
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    alien = Alien(ai_setting, screen)
    number_alien_x = get_number_alien_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)

    # create a group of alien
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    # detect the collision between the ship and aliens
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)

    # detect the alien fleet is at the bottom or not
    check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        # response the collisions between ship and aliens
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()
        # clean alien list and bullet list
        aliens.empty()
        bullets.empty()

        # create a group of aliens
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()

        # stop 0.5 seconds
        sleep(0.5)
    elif stats.ships_left <= 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # deal with it like hitting the ship
            ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
