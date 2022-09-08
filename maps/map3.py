# -------------------------------------------------------------------------------
# Name:        map3.py
# Created:     05.09.2022
# Copyright:   (c) Fischer, Gürschke, Hennig  2022
# -------------------------------------------------------------------------------
import os

import pygame

from platform import Platform


class Map3:
    def __init__(self):

        self.tiles = {}

        dir_path = "img/tiles/"

        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)) and path.endswith(".png"):
                self.tiles[path.replace(".png", "")] = pygame.transform.scale(pygame.image.load(dir_path + "/" + path),
                                                                              (32, 32))

        self.goal_pos_x = 100000

        self.cam_pos_x = 0
        self.positions = [(1, 28, 85, 2), (1, 1, 40, 20), (40, 1, 3, 22), (42, 1, 20, 24), (61, 1, 10, 15),
                          (70, 1, 11, 24), (80, 1, 40, 15), (100, 28, 28, 2), (105, 1, 20, 24), (200, 10, 20, 18),
                          (135, 22, 5, 2), (145, 20, 7, 4), (160, 18, 18, 5), (180, 14, 8, 2)]  ##Map3
        self.platform_group = pygame.sprite.Group()

        for position in self.positions:
            x, y, width, height = position
            self.platform_group.add(Platform(x, y, width, height))

    def is_in_goal(self, player_pos_x) -> bool:
        return player_pos_x >= self.goal_pos_x

    def update(self, screen, player_pos_x):
        self.cam_pos_x += 1

        self.platform_group.update(screen, player_pos_x)
        self.platform_group.draw(screen)

        water = self.tiles["waterTop"]
        water_width = water.get_width()
        water_height = screen.get_height() - water.get_height()

        for x in range(screen.get_height() // 16):
            pygame.draw.line(screen, (0, 0, 0), (0, x * 16), (1000000, x * 16))

        for y in range(player_pos_x + screen.get_width() // 16 + 1):
            pygame.draw.line(screen, (0, 0, 0), (y * 16 - player_pos_x, 0),
                             (y * 16 - player_pos_x, 1000))

        my_font = pygame.font.SysFont('Comic Sans MS', 9)
        for y in range(screen.get_width() * 6):
            text_surface = my_font.render(str(y * 5), False, (0, 0, 0))
            screen.blit(text_surface, (y * 5 * 16 - player_pos_x, 0))

        for y in range(screen.get_height()):
            text_surface = my_font.render(str(y + 1), False, (0, 0, 0))
            screen.blit(text_surface, (5, (y + 1) * 16 + 3))

        for i in range(player_pos_x + screen.get_width() // water_width + 1):
            screen.blit(water, (i * water_width - player_pos_x, water_height))
