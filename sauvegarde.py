import json
import pygame
import random
from utils import charger_json
from selection_pokemon import SelectionPokemon
from combat import Combat

def load_game(graphic):
    from menu import menu_principal
    """
    Interface pour charger une sauvegarde existante avec le fond du menu.
    """
    running = True
    while running:
        graphic.draw_menu_background() 

       
        graphic.draw_text("Charger une Partie", graphic.WIDTH // 2 - 150, 100, size=48, color=graphic.WHITE)

       
        bouton_confirmer = graphic.draw_button(300, "Continuer", graphic.GRAY, graphic.HIGHLIGHT)
        bouton_retour = graphic.draw_button(380, "Retour", graphic.GRAY, graphic.HIGHLIGHT)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_confirmer.collidepoint(x, y):
                    SelectionPokemon(graphic.screen).run()
                elif bouton_retour.collidepoint(x, y):
                    menu_principal()
                    return
