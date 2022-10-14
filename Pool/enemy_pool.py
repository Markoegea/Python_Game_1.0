from random import randint
import pygame

class InstantiateEnemys:
    def __init__(self) -> None:
        self.enemys_list:list = []
        self.activate_enemys = pygame.sprite.Group()

    def get_random_enemy(self):
        random_number = randint(0,(len(self.enemys_list)-1))
        self.enemy = self.enemys_list[random_number]

        if self.enemy.isActivate == False:
            self.enemy.isActivate = True
            return self.enemy 
        else:
            return None

enemys_pool = InstantiateEnemys()