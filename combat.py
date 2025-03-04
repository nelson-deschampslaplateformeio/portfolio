import pygame
import random
import sys
from utils import (
    afficher_texte, dessiner_bouton, calculer_dommages, get_pokemon_sprite,
    enregistrer_json, charger_json, augmenter_niveau
)

class Combat:
    def __init__(self, screen, equipe_joueur, adversaire):
        self.screen = screen

        if not equipe_joueur:
            print("⚠️ Erreur : L'équipe du joueur est vide !")
            return  

        self.pokemon_joueur = equipe_joueur[0]  
        self.equipe_joueur = equipe_joueur
        self.adversaire = adversaire   
        self.clock = pygame.time.Clock()
        self.sauvegarde_fichier = "data/sauvegarde.json"

        # ✅ Charger l'image de fond du combat
        self.background = pygame.image.load("pictures/battle_background.png")

        # Chargement des sprites Pokémon
        self.sprite_joueur = get_pokemon_sprite(self.pokemon_joueur["nom"], "back")
        self.sprite_adversaire = get_pokemon_sprite(self.adversaire["nom"], "front")

    def run(self):
        running = True
        while running:
            # ✅ Afficher le fond du combat
            self.screen.blit(self.background, (0, 0))

            afficher_texte(self.screen, "Combat Pokémon !", (300, 50), 36, (255, 255, 255))

            if self.sprite_adversaire:
                self.screen.blit(self.sprite_adversaire, (500, 100))
            afficher_texte(self.screen, f"{self.adversaire['nom']} - PV: {self.adversaire['pv']}", (500, 250), 28)

            if self.sprite_joueur:
                self.screen.blit(self.sprite_joueur, (100, 300))
            afficher_texte(self.screen, f"{self.pokemon_joueur['nom']} - PV: {self.pokemon_joueur['pv']}", (100, 450), 28)

            # Dessin des boutons d'attaque
            boutons_attaque = []
            for i, attaque in enumerate(self.pokemon_joueur["attaques"]):
                bouton = dessiner_bouton(self.screen, attaque, (50, 500 + i * 50))
                boutons_attaque.append((bouton, attaque))

            change_btn = dessiner_bouton(self.screen, "Changer", (300, 500))
            run_btn = dessiner_bouton(self.screen, "Abandonner", (500, 500))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for bouton, attaque in boutons_attaque:
                        if bouton.collidepoint(x, y):
                            self.attaquer(attaque)
                    if change_btn.collidepoint(event.pos):
                        self.changer_pokemon()
                    elif run_btn.collidepoint(event.pos):
                        self.sauvegarder_progres()
                        return

            self.clock.tick(30)

    def attaquer(self, attaque):
        degats = calculer_dommages(self.pokemon_joueur, self.adversaire, attaque)
        print(f"{self.pokemon_joueur['nom']} utilise {attaque} et inflige {degats} dégâts à {self.adversaire['nom']} !")
        self.adversaire["pv"] -= degats

        if self.adversaire["pv"] <= 0:
            print(f"{self.adversaire['nom']} est K.O. !")
            augmenter_niveau(self.pokemon_joueur)
            self.fin_du_combat()
            return

        self.attaque_adversaire()

    def attaque_adversaire(self):
        attaque = random.choice(self.adversaire["attaques"])
        degats = calculer_dommages(self.adversaire, self.pokemon_joueur, attaque)
        print(f"{self.adversaire['nom']} utilise {attaque} et inflige {degats} dégâts à {self.pokemon_joueur['nom']} !")
        self.pokemon_joueur["pv"] -= degats

        if self.pokemon_joueur["pv"] <= 0:
            print(f"{self.pokemon_joueur['nom']} est K.O. !")
            self.changer_pokemon(force=True)

    def changer_pokemon(self, force=False):
        for pokemon in self.equipe_joueur:
            if pokemon["pv"] > 0 and pokemon != self.pokemon_joueur:
                print(f"{self.pokemon_joueur['nom']} est remplacé par {pokemon['nom']} !")
                self.pokemon_joueur = pokemon
                self.sprite_joueur = get_pokemon_sprite(pokemon["nom"], "back")
                return

        if force:
            print("Tous les Pokémon sont K.O. ! Fin du combat.")
            self.fin_du_combat()

    def fin_du_combat(self):
        print("⚔️ Fin du combat !")

        joueur_gagne = self.adversaire["pv"] <= 0
        self.ajouter_au_pokedex(self.adversaire["nom"], joueur_gagne)

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            afficher_texte(self.screen, "Le combat est terminé !", (250, 200), 36)

            if joueur_gagne:
                afficher_texte(self.screen, f"Vous avez capturé {self.adversaire['nom']} !", (250, 250), 30, (0, 255, 0))
            else:
                afficher_texte(self.screen, f"{self.adversaire['nom']} est marqué comme invalable.", (250, 250), 30, (255, 0, 0))

            bouton_continuer = dessiner_bouton(self.screen, "Nouveau Combat", (250, 350))
            bouton_fuir = dessiner_bouton(self.screen, "Retour au menu", (250, 450))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if bouton_continuer.collidepoint((x, y)):
                        self.nouveau_combat()
                        running = False
                    elif bouton_fuir.collidepoint((x, y)):
                        self.sauvegarder_progres()
                        running = False
                        return

    def nouveau_combat(self):
        print("🔄 Un nouveau combat commence !")
        tous_les_pokemons = charger_json("pokemon_data.json")
        if not tous_les_pokemons:
            print("⚠️ Erreur : Impossible de charger la liste des Pokémon.")
            return

        nouvel_adversaire = random.choice(tous_les_pokemons)
        while nouvel_adversaire["nom"] == self.adversaire["nom"]:
            nouvel_adversaire = random.choice(tous_les_pokemons)

        self.adversaire = nouvel_adversaire
        self.run()

    def sauvegarder_progres(self):
        print("💾 Sauvegarde de la progression...")
        sauvegarde = charger_json("sauvegarde.json")

        if not isinstance(sauvegarde, dict):
            sauvegarde = {}

        sauvegarde["equipe_joueur"] = self.equipe_joueur
        enregistrer_json("sauvegarde.json", sauvegarde)

        print("✅ Progression sauvegardée ! Retour au menu.")
        from menu import menu_principal
        menu_principal()

    def ajouter_au_pokedex(self, nom_pokemon, est_gagnant):
        pokedex = charger_json("pokedex.json")

        for entry in pokedex:
            if entry["nom"] == nom_pokemon:
                print(f"📖 {nom_pokemon} est déjà dans le Pokédex.")
                return

        new_entry = {
            "nom": nom_pokemon,
            "statut": "JOUABLE" if est_gagnant else "INVALABLE"
        }
        pokedex.append(new_entry)

        enregistrer_json("pokedex.json", pokedex)
        print(f"✅ {nom_pokemon} ajouté au Pokédex avec le statut: {new_entry['statut']}")
