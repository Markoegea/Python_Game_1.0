from typing import Dict
import pygame
from Enums.player_state import PlayerState
from Display.pygame_init import InitiateGame

class Player(InitiateGame):
    def __init__(self) -> None:
        super().__init__()
        #Player walk anim
        self.player_anim_walk:list = []
        self.player_anim_walk.append(pygame.image.load('Graphics/Player/run01.png').convert_alpha())
        self.player_anim_walk.append(pygame.image.load('Graphics/Player/run02.png').convert_alpha())
        self.player_anim_walk.append(pygame.image.load('Graphics/Player/run03.png').convert_alpha())
        self.player_anim_walk.append(pygame.image.load('Graphics/Player/run04.png').convert_alpha())
        self.player_anim_walk.append(pygame.image.load('Graphics/Player/run05.png').convert_alpha())
        self.player_index_walk = 0

        #Player jump anim
        self.player_anim_jump:list = []
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump01.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump02.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump03.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump04.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump05.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump06.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump07.png').convert_alpha())
        self.player_anim_jump.append(pygame.image.load('Graphics/Player/jump08.png').convert_alpha())   
        self.player_index_jump = 0

        #Player idle anim
        self.player_anim_idle:list = []
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle01.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle02.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle03.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle04.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle05.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle06.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle07.png').convert_alpha())
        self.player_anim_idle.append(pygame.image.load('Graphics/Player/idle08.png').convert_alpha())   
        self.player_index_idle = 0

        self.image = self.player_anim_idle[self.player_index_idle]
        self.rect = self.image.get_rect(midbottom=(50,355))
        self.jump = pygame.mixer.Sound('Music/Jump.wav')
        self.channel = pygame.mixer.Channel(1)
        self.GRAVITY = 10
        self.player_vector:Dict = {'x':0,'y':0}
        self.x:int
        self.y:int
        self.current_player_state: PlayerState = PlayerState.WALKING
        self.keys:bool
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self)

    def player_spawn(self):
        self.rect.midbottom=(50,355)

    def player_input(self):
        self.keys = pygame.key.get_pressed()
        if(self.keys[pygame.K_SPACE] and self.current_player_state != PlayerState.JUMP and self.current_player_state != PlayerState.JUMPING):
            self.player_vector['x'] += 0
            self.player_vector['y'] = -14
            self.channel.play(self.jump)
            self.current_player_state = PlayerState.JUMP

        if (self.keys[pygame.K_d]):
            self.player_vector['x'] = 2

        if (self.keys[pygame.K_a]):
            self.player_vector['x'] = -2

        if (not self.keys[pygame.K_d] and not self.keys[pygame.K_a]):
            self.player_vector['x'] = 0


    def player_behavior(self):
        #Limits of Map
        if self.rect.x > 790:
            self.rect.x = 780

        if self.rect.x < 0:
            self.rect.x = 0

        #Player behavior
        if self.current_player_state == PlayerState.IDLE:
            if self.player_vector['x'] != 0:
                self.current_player_state = PlayerState.WALKING
            else:
                self.current_player_state = PlayerState.IDLE

        if self.current_player_state == PlayerState.JUMP:
            self.y = self.player_vector['y']
            self.x = self.player_vector['x']
            self.current_player_state = PlayerState.JUMPING

        if self.current_player_state == PlayerState.JUMPING:
            self.y +=self.GRAVITY/15
            self.rect.y += self.y
            self.rect.x += self.x

        if self.rect.bottom > 358 and self.current_player_state == PlayerState.JUMPING:
            self.rect.bottom = 355
            self.current_player_state = PlayerState.IDLE


        if self.current_player_state == PlayerState.WALKING:
            self.rect.x += self.player_vector['x']

            if self.player_vector['x'] != 0:
                self.current_player_state = PlayerState.WALKING
            else:
                self.current_player_state = PlayerState.IDLE

    def player_animation(self):
        if self.current_player_state == PlayerState.IDLE:
            self.player_index_idle += 0.1
            if self.player_index_idle >= len(self.player_anim_idle):self.player_index_idle=0
            self.image = self.player_anim_idle[int(self.player_index_idle)]

        if self.current_player_state == PlayerState.JUMPING:
            self.player_index_jump += 0.1
            if self.player_index_jump >= len(self.player_anim_jump):self.player_index_jump=0
            self.image = self.player_anim_jump[int(self.player_index_jump)]

        if self.current_player_state == PlayerState.WALKING:
            self.player_index_walk += 0.1
            if self.player_index_walk >= len(self.player_anim_walk):self.player_index_walk=0
            self.image = self.player_anim_walk[int(self.player_index_walk)]
            
            if self.player_vector['x'] < 0:
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.player_vector['x'] > 0:
                self.player_surface = pygame.transform.flip(self.image,False,False)
        
    def update(self) -> None:
        self.player_input()
        self.player_behavior()
        self.player_animation()

#Player
player:Player = Player()