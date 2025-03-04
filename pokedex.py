import os
import json
import pygame
import time  # Import pour gérer le délai avant de revenir au menu

class Pokedex:
    def __init__(self, image_directory, data_file, menu_principal_func):
        self.image_directory = image_directory
        self.data_file = data_file
        self.menu_principal_func = menu_principal_func  # Fonction pour retourner au menu principal

        self.pokemon_data = self.charger_pokemon()
        self.pokemon_keys = list(self.pokemon_data['available'].keys()) + list(self.pokemon_data['unavailable'].keys())
        self.current_index = 0

        self.init_pygame()

    def charger_pokemon(self):
        """ Charge les Pokémon à partir du fichier JSON """
        if not os.path.exists(self.data_file):
            print(f"⚠️ Erreur : Fichier {self.data_file} introuvable !")
            return {'available': {}, 'unavailable': {}}

        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)['en']['pokemon']

    def init_pygame(self):
        """ Initialise la fenêtre du Pokédex """
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokédex")
        self.clock = pygame.time.Clock()

        # Charger la musique du Pokédex
        pygame.mixer.music.load("sounds/menu.mp3")
        pygame.mixer.music.play(-1)

    def afficher_pokedex(self):
        """ Affiche le Pokédex avec le statut "Disponible" ou "Invalable" """
        if not self.pokemon_keys:
            print("⚠️ Aucun Pokémon enregistré dans le Pokédex.")
            self.afficher_message_vide()
            return

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_keys)
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_keys)

            self.screen.fill((255, 255, 255))

            # Affichage du Pokémon actuel
            pokemon_key = self.pokemon_keys[self.current_index]
            if pokemon_key in self.pokemon_data['available']:
                pokemon = self.pokemon_data['available'][pokemon_key]
                availability_text = "Disponible"
                availability_color = (0, 255, 0)  # Vert
            else:
                pokemon = self.pokemon_data['unavailable'][pokemon_key]
                availability_text = "Invalable"
                availability_color = (255, 0, 0)  # Rouge

            # Chargement et affichage de l'image du Pokémon
            image_path = os.path.join(self.image_directory, f"{pokemon_key}.png")
            try:
                pokemon_image = pygame.image.load(image_path)
                pokemon_image = pygame.transform.scale(pokemon_image, (325, 325))
                self.screen.blit(pokemon_image, (250, 100))
            except pygame.error:
                print(f"⚠️ Image introuvable : {image_path}")

            # Affichage des informations du Pokémon
            font = pygame.font.SysFont("Comic Sans MS", 24)
            info_text = f"Nom: {pokemon['name']}\nNiveau: {pokemon['level']}\nPV: {pokemon['hit_points']}\nType: {pokemon['type_']}\nAttaque: {pokemon['attack']}\nDéfense: {pokemon['defense']}"
            y_offset = 450
            for line in info_text.split('\n'):
                text_surface = font.render(line, True, (0, 0, 0))
                self.screen.blit(text_surface, (250, y_offset))
                y_offset += 30

            # Affichage du statut (Disponible ou Invalable)
            font_status = pygame.font.SysFont("Comic Sans MS", 26, bold=True)
            status_surface = font_status.render(availability_text, True, (255, 255, 255))
            status_rect = pygame.Rect(250, y_offset, status_surface.get_width() + 20, status_surface.get_height() + 10)
            pygame.draw.rect(self.screen, availability_color, status_rect, border_radius=10)
            self.screen.blit(status_surface, (status_rect.x + 10, status_rect.y + 5))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def afficher_message_vide(self):
        """ Affiche un message et revient au menu après 5 secondes si le Pokédex est vide """
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Comic Sans MS", 30)
        text_surface = font.render("Aucun Pokémon dans le Pokédex ! Retour au menu...", True, (255, 0, 0))
        self.screen.blit(text_surface, (150, 250))
        pygame.display.flip()

        time.sleep(5)  # Attendre 5 secondes avant de revenir au menu
        self.menu_principal_func()  # Retour au menu principal
