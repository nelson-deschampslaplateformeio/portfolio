import pygame
import sys
from selection_pokemon import SelectionPokemon
from pokedex import Pokedex
from sauvegarde import load_game
from utils import charger_json, enregistrer_json, get_pokemon_data
from graphic import Graphic
import os

def menu_principal():
    pygame.init()
    
    # Récupérer la résolution de l'écran
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    
    # Mode plein écran
    screen = pygame.display.set_mode((screen_width, screen_height))
    graphic = Graphic(screen)

    # Charger et redimensionner l’image de fond
    background = pygame.image.load(os.path.join("pictures", "menu-background.jpg"))
  # Remplace avec ton image
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # Ajuster les dimensions des boutons en fonction de l’écran
    button_width = int(screen_width * 0.3)   # 30% de la largeur de l'écran
    button_height = int(screen_height * 0.08) # 8% de la hauteur de l'écran
    spacing = int(button_height * 0.5)  # Espacement des boutons

    pos_x = (screen_width - button_width) // 2
    pos_y = screen_height // 4

    running = True
    while running:
        screen.blit(background, (0, 0))  # Affichage du fond plein écran
        graphic.draw_text("Menu Principal", screen_width // 2 - 150, screen_height // 10, size=48, color=graphic.WHITE)

        # Création des boutons ajustés
        bouton_nouvelle_partie = graphic.draw_button(pos_y, "Nouvelle Partie", graphic.GRAY, graphic.HIGHLIGHT, button_width, button_height)
        bouton_pokedex = graphic.draw_button(pos_y + (button_height + spacing), "Pokédex", graphic.GRAY, graphic.HIGHLIGHT, button_width, button_height)
        bouton_ajouter_pokemon = graphic.draw_button(pos_y + 2 * (button_height + spacing), "Ajouter Pokémon", graphic.GRAY, graphic.HIGHLIGHT, button_width, button_height)
        bouton_regles = graphic.draw_button(pos_y + 3 * (button_height + spacing), "Rules & Settings", graphic.GRAY, graphic.HIGHLIGHT, button_width, button_height)
        bouton_quitter = graphic.draw_button(pos_y + 4 * (button_height + spacing), "Quitter", graphic.GRAY, graphic.HIGHLIGHT, button_width, button_height)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_nouvelle_partie.collidepoint(x, y):
                    SelectionPokemon(graphic.screen, menu_principal).run()
                elif bouton_pokedex.collidepoint(x, y):
                    image_directory = "pokemon_sprites"  # Dossier des images Pokémon
                    data_file = "data/generated_pokemon.json"  # Fichier JSON contenant les Pokémon

                    Pokedex(image_directory, data_file, menu_principal).afficher_pokedex()

                elif bouton_ajouter_pokemon.collidepoint(x, y):
                    ajouter_pokemon_interface(graphic, menu_principal)
                elif bouton_regles.collidepoint(x, y):
                    afficher_regles_et_parametres(graphic, menu_principal)
                elif bouton_quitter.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

    pygame.quit()
    sys.exit()

def ajouter_pokemon_interface(graphic, menu_principal_func):
    
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(graphic.WIDTH // 2 - 150, 250, 300, 40)  # Centré
    couleur_active = (255, 255, 255)
    couleur_inactive = (200, 200, 200)
    couleur = couleur_inactive
    actif = False
    texte = ""

    running = True
    while running:
        graphic.draw_menu_background()  

        graphic.draw_text("Entrez le nom du Pokémon :", graphic.WIDTH // 2 - 200, 200, size=30, color=graphic.WHITE)

        pygame.draw.rect(graphic.screen, couleur, input_box, 2)
        txt_surface = font.render(texte, True, (255, 255, 255))
        graphic.screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

        bouton_retour = graphic.draw_button(graphic.HEIGHT // 2, "Retour", graphic.GRAY, graphic.HIGHLIGHT)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    actif = True
                else:
                    actif = False
                couleur = couleur_active if actif else couleur_inactive
                if bouton_retour.collidepoint(event.pos):
                    menu_principal_func()
                    return
            elif event.type == pygame.KEYDOWN:
                if actif:
                    if event.key == pygame.K_RETURN:
                        if texte:
                            pokemons = charger_json("data/pokemon.json")
                            if texte.lower() not in [p["nom"].lower() for p in pokemons]:
                                pokemon_data = get_pokemon_data(texte)
                                if pokemon_data:
                                    pokemons.append(pokemon_data)
                                    enregistrer_json("data/pokemon.json", pokemons)
                                    print(f"{texte.capitalize()} ajouté avec succès !")
                            menu_principal_func()
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        texte = texte[:-1]
                    else:
                        texte += event.unicode


def afficher_regles_et_parametres(graphic, menu_principal_func):
   
    running = True
    volume = 0.5  
    pygame.mixer.music.set_volume(volume)

    while running:
        graphic.draw_menu_background() 

        graphic.draw_text("Rules & Settings", graphic.WIDTH // 2 - 150, 100, size=48, color=graphic.WHITE)

        rules_text = [
            "1. Choisissez un Pokémon pour commencer.",
            "2. Combattez d'autres Pokémon pour gagner de l'expérience.",
            "3. Attrapez et collectionnez des Pokémon dans le Pokédex.",
            "4. Certains Pokémon évoluent en montant de niveau.",
            "5. Fuir un combat sauvegarde votre progression.",
        ]

        y_offset = 180
        for rule in rules_text:
            graphic.draw_text(rule, graphic.WIDTH // 2 - 250, y_offset, size=24, color=graphic.YELLOW)
            y_offset += 40

        bouton_retour = graphic.draw_button(550, "Retour", graphic.GRAY, graphic.HIGHLIGHT)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_retour.collidepoint(x, y):
                    menu_principal_func()
                    return


if __name__ == "__main__":
    menu_principal()
