import pygame
from Sprites.player import player
from random import randint
from Enums.game_state import GameState
from Pool.enemy_pool import enemys_pool
from Display.pygame_init import InitiateGame

class Enemy(InitiateGame):
    def __init__(self, list_anim:list, isActivate:bool,type:str) -> None:
        super().__init__()
        self.enemy_anim_walk:list = list_anim
        self.enemy_index_walk = 0
        self.image = self.enemy_anim_walk[self.enemy_index_walk]
        self.rect = self.image.get_rect(midbottom=(1000,1000))
        self.isActivate = isActivate
        self.type = type
        self.speed:int = 0
        self.enemy_spawn()
        
    
    def enemy_spawn(self):
        self.isActivate = False
        if self.type == 'fly':
            random_tuple = (randint(800,1200),randint(230,330))
            self.speed = 4
        else:
            random_tuple = (randint(800,1200),355)
            self.speed = 3
        self.rect.midbottom=random_tuple

    def enemy_behavior(self):
        if self.isActivate:
            self.rect.x -= self.speed
        if (self.rect.x < -50):
            self.isActivate = False
            self.enemy_spawn()
            enemys_pool.activate_enemys.remove(self)

    def enemy_collision(self):
        if pygame.sprite.spritecollide(player.player_sprite.sprite,enemys_pool.activate_enemys,False):
            InitiateGame.current_game_state = GameState.GAMEOVER

    def enemy_animation(self):
        self.enemy_index_walk += 0.1     
        if self.enemy_index_walk >= len(self.enemy_anim_walk):self.enemy_index_walk=0
        self.image = self.enemy_anim_walk[int(self.enemy_index_walk)]

    def update(self) -> None:
        self.enemy_behavior()
        self.enemy_animation()
        self.enemy_collision()

