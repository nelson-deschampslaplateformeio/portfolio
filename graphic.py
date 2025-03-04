import pygame

class Graphic:
    
    def __init__(self, game, width=1280, height=720):
        self.WIDTH = width 
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = game

       
        self.WIDTH, self.HEIGHT = 800, 600

       
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 200, 50)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.HIGHLIGHT = (100, 149, 237)
        self.BLUE = (0, 0, 255)

        self.FPS = 30

        
        try:
            self.background = pygame.image.load("pictures/menu-background.jpg")
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        except pygame.error:
            print("⚠️ Erreur : Image de fond du menu introuvable.")
            self.background = None 

        try:
            self.battle_background = pygame.image.load("pictures/battle_background.png")
            self.battle_background = pygame.transform.scale(self.battle_background, (self.WIDTH, self.HEIGHT))
        except pygame.error:
            print("⚠️ Erreur : Image de fond du combat introuvable.")
            self.battle_background = None

    def remplir_ecran(self, couleur):
       
        self.screen.fill(couleur)
        pygame.display.set_caption("Pokémon Game")

    def draw_menu_background(self):
        
        if self.background:
            self.screen.blit(self.background, (0, 0))

    def draw_button(self, y, text, color, highlight_color, width=250, height=50):
        x = (self.WIDTH - width) // 2  # Centrer le bouton
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
    
    # Dessiner le texte au centre du bouton
        font = pygame.font.Font(None, 36)
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
        return rect


    def draw_text(self, text, x, y, size=36, color=(255, 255, 255)):
     
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
