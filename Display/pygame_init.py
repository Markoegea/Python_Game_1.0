from Enums.game_state import GameState
import pygame

class InitiateGame(pygame.sprite.Sprite):
    current_game_state: GameState = GameState.MENU

    def __init__(self) -> None:
        #Start the game logic
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800,400)) #width,height
        pygame.display.set_caption('Super Run and Jump')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Graphics/Fonts/Pixel.ttf',50)