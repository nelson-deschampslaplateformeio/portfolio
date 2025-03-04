import pygame
import random
import sys
from utils import charger_json, afficher_texte, dessiner_bouton
from combat import Combat
from graphic import Graphic

class SelectionPokemon:
    def __init__(self, screen, menu_principal):
        """
        Initialise la sélection de Pokémon avec la gestion des sprites et des données.
        """
        self.screen = screen
        self.menu_principal = menu_principal
        self.graphic = Graphic(screen)
        data = charger_json("data/pokemon.json")

      
        if isinstance(data, list):
            self.pokemon_list = data
        else:
            self.pokemon_list = []  

        self.clock = pygame.time.Clock()
        self.index = 0  

    def run(self):
        """
        Affichage de l'interface de sélection de Pokémon.
        """
        running = True
        
        while running:
            self.screen.fill((0, 0, 0))

           
            self.graphic.draw_text("Sélectionnez votre Pokémon", 200, 100, size=36, color=self.graphic.WHITE)

        
            bouton_valider = self.graphic.draw_button(350, "Valider", self.graphic.GRAY, self.graphic.HIGHLIGHT)
            bouton_retour = self.graphic.draw_button(420, "Retour", self.graphic.GRAY, self.graphic.HIGHLIGHT)

           
            current = self.pokemon_list[self.index]  

            nom = current.get("nom", "Inconnu")
            type_pokemon = ', '.join(current.get("type", ["Inconnu"]))
            pv = current.get("pv", 0)
            attaque = current.get("attaque", 0)
            defense = current.get("defense", 0)

            details = f"{nom} | Type: {type_pokemon} | PV: {pv} | ATK: {attaque} | DEF: {defense}"
            afficher_texte(self.screen, details, (100, 150), 28, (255, 255, 255))

           
            prev_btn = dessiner_bouton(self.screen, "<", (150, 300))
            next_btn = dessiner_bouton(self.screen, ">", (500, 300))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if prev_btn.collidepoint(event.pos):
                        self.index = (self.index - 1) % len(self.pokemon_list) 
                    elif next_btn.collidepoint(event.pos):
                        self.index = (self.index + 1) % len(self.pokemon_list)
                    elif bouton_valider.collidepoint(event.pos):
                        pokemon_joueur = self.pokemon_list[self.index]
                        equipe_joueur = [pokemon_joueur] 
                        adversaire = random.choice(self.pokemon_list)
                        combat = Combat(self.screen, equipe_joueur, adversaire) 
                        combat.run()
                        return
                    elif bouton_retour.collidepoint(event.pos):
                        self.menu_principal()  
                        return

            self.clock.tick(30)
