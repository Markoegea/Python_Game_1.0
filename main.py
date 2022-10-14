import os
import pygame
import platform
import Pool.enemy_inst as enemy_inst
from sys import exit
from Sprites.player import player
from Enums.game_state import GameState
from Pool.enemy_pool import enemys_pool
from Display.pygame_init import InitiateGame
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

#draw elements
#update logic
class GameManager(InitiateGame):
    
    def __init__(self) -> None:
        super(GameManager,self).__init__()
        self.game_time: float = 0
        self.game_score: float = 0
        self.menu_music = pygame.mixer.Sound('Music/menu.wav')
        self.bg_music = pygame.mixer.Sound('Music/background.wav')
        self.over_music = pygame.mixer.Sound('Music/game_over.wav')

    def startGame(self):

        #Background surfaces
        background_surface = pygame.image.load('Graphics/Background/fog_trees.png').convert_alpha()
        trees_bush = pygame.image.load('Graphics/Background/bush.png').convert_alpha()
        trees_surface = pygame.image.load('Graphics/Background/out_trees.png').convert_alpha()
        ground_surface = pygame.image.load('Graphics/Background/ground_green.png').convert_alpha()

        #Enemys declaration
        enemys:enemys.Enemy = []

        enemy_1_anim_walk:list = []
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk01.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk02.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk03.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk04.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk05.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk06.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk07.png').convert_alpha())
        enemy_1_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy01/walk08.png').convert_alpha())
        monster_1 = enemy_inst.PooledEnemys(enemy_1_anim_walk,2,False,'pig')
    
        enemy_2_anim_walk:list = []
        enemy_2_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy02/walk01.png').convert_alpha())
        enemy_2_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy02/walk02.png').convert_alpha())
        enemy_2_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy02/walk03.png').convert_alpha())
        enemy_2_anim_walk.append(pygame.image.load('Graphics/Enemys/Enemy02/walk04.png').convert_alpha())
        monster_2 = enemy_inst.PooledEnemys(enemy_2_anim_walk,2,False,'fly')

        #Menu Surfaces
        menu_surface = pygame.image.load('Graphics/Player/run01.png').convert_alpha()
        menu_scale = pygame.transform.rotozoom(menu_surface,0,3)
        menu_rect_scale = menu_scale.get_rect(midbottom = (400,250))

        #Game Over Surfaces
        player_dead = pygame.image.load('Graphics/Player/dead01.png').convert_alpha()
        player_dead = pygame.transform.rotozoom(player_dead,0,3)
        player_dead_rect = player_dead.get_rect(center = (400,200))

        #Timer
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer,1500)

        while True:
            for event in pygame.event.get():
            #Exit Game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #Restart Game
            if event.type == pygame.MOUSEBUTTONUP and InitiateGame.current_game_state != GameState.INGAME:
                if event.button == 1: 
                    InitiateGame.current_game_state = GameState.INGAME
            
            #Enemy Timer
            if event.type == obstacle_timer and InitiateGame.current_game_state == GameState.INGAME:
                enemy =enemys_pool.get_random_enemy()
                if enemy != None:
                    enemys_pool.activate_enemys.add(enemy)

            if InitiateGame.current_game_state == GameState.MENU:
                self.play_musics(0)

                self.screen.fill((104, 102, 101))
                self.screen.blit(menu_scale,menu_rect_scale)
                self.menu_game(self.font,self.screen)
                self.game_time = pygame.time.get_ticks()

            elif InitiateGame.current_game_state == GameState.INGAME:
                self.play_musics(1)
                #Background surfaces
                self.screen.blit(background_surface,(0,0))
                self.screen.blit(trees_surface,(-10,100))
                self.screen.blit(trees_bush,(0,-150))
                self.screen.blit(ground_surface,(0,350))  
                self.display_score(pygame.time.get_ticks(),self.font,self.screen)

                #Player behavior
                player.player_sprite.draw(self.screen)
                player.player_sprite.update()

                enemys_pool.activate_enemys.draw(self.screen)
                enemys_pool.activate_enemys.update()

            elif InitiateGame.current_game_state == GameState.GAMEOVER:
                self.play_musics(2)
                self.game_restart()
                self.screen.fill((104, 102, 101))
                self.screen.blit(player_dead,player_dead_rect)
                self.game_over_menu(self.font,self.screen)
                self.display_score(pygame.time.get_ticks(),self.font,self.screen,False)
                self.game_time = pygame.time.get_ticks()

            pygame.display.update()
            self.clock.tick(60)

    def play_musics(self,type_music:int):
        if(type_music == 0):
            self.menu_music.play()
        elif(type_music == 1):
            self.menu_music.stop()
            self.bg_music.play()
            self.bg_music.set_volume(0.7)
            self.over_music.stop()
        elif(type_music == 2):
            self.menu_music.stop()
            self.bg_music.stop()
            self.over_music.play()


    def game_restart(self):
        self.restart_player(player)
        self.restart_enemys(enemys_pool.activate_enemys)

    def restart_player(self,player):
        player.player_spawn()

    def restart_enemys(self,enemys_list):
        for enemy in enemys_list.sprites():
            enemy.enemy_spawn()
        enemys_list.empty()
    

    def game_over_menu(self,font,screen):
        restart_text = font.render("Press left mouse click to restart game", False, (241, 87, 87))
        restart_rect = restart_text.get_rect(center = (screen.get_width()*0.5,screen.get_height()*0.8))
        pygame.draw.rect(screen,(59, 152, 21),restart_rect,5,30)
        screen.blit(restart_text,restart_rect)

    def menu_game(self,font,screen):
        game_text = font.render("Super Run and Jump", False, (9, 47, 176))
        game_rect = game_text.get_rect(center = (screen.get_width()*0.5,screen.get_height()*0.1))
        pygame.draw.rect(screen,(176, 9, 24),game_rect,5,30)
        screen.blit(game_text,game_rect)

        start_text = font.render("Press left mouse click to start game", False, (176, 9, 24))
        start_rect = start_text.get_rect(center = (screen.get_width()*0.5,screen.get_height()*0.8))
        pygame.draw.rect(screen,(9, 47, 176),start_rect,5,30)
        screen.blit(start_text,start_rect)

    def display_score(self,time:float,font,screen,isPlaying:bool=True):
        if isPlaying:
            total_time:float = time - self.game_time
            current_time:float = (total_time/1000)
            self.game_score = round(current_time,1)  

        score_surface = font.render(str(self.game_score)+ "s", False, (59, 152, 21))
        score_rect = score_surface.get_rect(center = (screen.get_width()*0.5,screen.get_height()*0.1))
        pygame.draw.rect(screen,(183, 4, 4),score_rect,1)
        pygame.draw.rect(screen,(183, 4, 4),score_rect,1,30)
        screen.blit(score_surface,score_rect)

    #fps_surface = font.render(str(int(clock.get_fps())), False, (59, 152, 21))
    #fps_rect = fps_surface.get_rect(center = (screen.get_width()*0.1,screen.get_height()*0.1))
    #screen.blit(fps_surface,fps_rect)
game = GameManager()

if __name__ == '__main__':
    game.startGame()