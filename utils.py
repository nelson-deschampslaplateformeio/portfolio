import json
import pygame
import os
import random
from io import BytesIO
import requests  

# --- Gestion JSON ---
def charger_json(fichier):
    """ Charge un fichier JSON et retourne son contenu sous forme de liste. """
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def enregistrer_json(fichier, data):
    """ Enregistre les données dans un fichier JSON. """
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Fonctions d'affichage ---
def afficher_texte(fenetre, texte, position, taille=24, couleur=(255,255,255)):
    """ Affiche un texte sur la fenêtre Pygame. """
    font = pygame.font.Font(None, taille)
    surface = font.render(texte, True, couleur)
    fenetre.blit(surface, position)

def dessiner_bouton(screen, texte, position, largeur=200, hauteur=50, couleur=(0, 122, 255)):
    font = pygame.font.Font(None, 32)  # ✅ Taille fixe pour tous les boutons
    texte_rendu = font.render(texte, True, (255, 255, 255))

    bouton_rect = pygame.Rect(position[0], position[1], largeur, hauteur)
    pygame.draw.rect(screen, couleur, bouton_rect)

    # Centrage du texte
    text_x = bouton_rect.centerx - texte_rendu.get_width() // 2
    text_y = bouton_rect.centery - texte_rendu.get_height() // 2
    screen.blit(texte_rendu, (text_x, text_y))

    return bouton_rect




table_types = {
    "Normal": {"Roche": 0.5, "Spectre": 0, "Acier": 0.5},
    "Feu": {"Eau": 0.5, "Plante": 2, "Glace": 2, "Insecte": 2, "Acier": 2, "Roche": 0.5, "Dragon": 0.5},
    "Eau": {"Feu": 2, "Plante": 0.5, "Sol": 2, "Roche": 2, "Dragon": 0.5},
    "Plante": {"Feu": 0.5, "Eau": 2, "Plante": 0.5, "Poison": 0.5, "Vol": 0.5, "Insecte": 0.5, "Sol": 2, "Roche": 2, "Dragon": 0.5},
    "Électrik": {"Eau": 2, "Plante": 0.5, "Sol": 0, "Vol": 2, "Dragon": 0.5},
    "Glace": {"Feu": 0.5, "Eau": 0.5, "Plante": 2, "Glace": 0.5, "Sol": 2, "Vol": 2, "Dragon": 2, "Acier": 0.5},
    "Combat": {"Normal": 2, "Glace": 2, "Roche": 2, "Spectre": 0, "Poison": 0.5, "Vol": 0.5, "Psy": 0.5, "Insecte": 0.5, "Ténèbres": 2, "Fée": 0.5},
    "Poison": {"Plante": 2, "Sol": 0.5, "Roche": 0.5, "Spectre": 0.5, "Acier": 0, "Fée": 2},
    "Sol": {"Feu": 2, "Électrik": 2, "Plante": 0.5, "Poison": 2, "Vol": 0, "Roche": 2, "Acier": 2},
}


def calculer_dommages(attaquant, defenseur, attaque):
    """ 
    Calcule les dégâts en fonction de l'attaque, la défense et des types.
    """
    base = random.randint(10, 25)
    
    type_attaquant = attaquant["type"][0] if isinstance(attaquant["type"], list) else attaquant["type"]
    type_defenseur = defenseur["type"][0] if isinstance(defenseur["type"], list) else defenseur["type"]
    
    modificateur = table_types.get(type_attaquant, {}).get(type_defenseur, 1)
    
    dommages = int((attaquant["attaque"] * modificateur) - defenseur["defense"] + base)
    
    return max(1, dommages) 


def get_pokemon_data(nom):
    """ Récupère les stats et attaques du Pokémon depuis `pokemon_data.json` ou PokéAPI. """
    pokemons = charger_json("pokemon_data.json")
    
    for pokemon in pokemons:
        if pokemon["nom"].lower() == nom.lower():
            return pokemon  

    print(f"⚠️ Pokémon {nom} non trouvé dans `pokemon_data.json`. Tentative de récupération via PokéAPI...")
    return ajouter_pokemon_depuis_api(nom)

def ajouter_pokemon_depuis_api(nom):
    """ Ajoute un Pokémon dans `pokemon_data.json` en récupérant ses données depuis PokéAPI. """
    url = f"https://pokeapi.co/api/v2/pokemon/{nom.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Erreur : Impossible de récupérer {nom} depuis l'API.")
        return None

    data = response.json()
    
    nouveau_pokemon = {
        "nom": nom.capitalize(),
        "type": [t["type"]["name"].capitalize() for t in data["types"]],
        "pv": data["stats"][0]["base_stat"],
        "attaque": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "attaques": [m["move"]["name"].capitalize() for m in data["moves"][:4]], 
        "sprites": {
            "face": data["sprites"]["front_default"],
            "dos": data["sprites"]["back_default"]
        }
    }
    
    
    pokemons = charger_json("pokemon_data.json") 

 
    if any(p["nom"].lower() == nom.lower() for p in pokemons):
        print(f"⚠️ {nom} est déjà enregistré dans `pokemon_data.json`.")
        return nouveau_pokemon

    
    pokemons.append(nouveau_pokemon)
    enregistrer_json("pokemon_data.json", pokemons)
    
    print(f"✅ {nom} ajouté avec succès depuis l'API !")
    return nouveau_pokemon

def get_pokemon_sprite(nom, side="front"):
    """
    Récupère le sprite du Pokémon depuis `pokemon_data.json` ou PokéAPI.
    side = "front" pour le sprite avant, "back" pour le sprite arrière.
    """
    pokemon = get_pokemon_data(nom)
    
    if pokemon:
        sprite_url = pokemon["sprites"]["face"] if side == "front" else pokemon["sprites"]["dos"]

        
    if sprite_url:
        sprite_url = sprite_url.replace("spriites", "sprites")

        
        if sprite_url:
            try:
                sprite_response = requests.get(sprite_url)
                if sprite_response.status_code == 200:
                    image_bytes = BytesIO(sprite_response.content)
                    sprite = pygame.image.load(image_bytes).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (150, 150))  
                    return sprite
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement du sprite de {nom} : {e}")

    print(f"⚠️ Aucun sprite trouvé pour {nom}.")
    return None


evolution_data = {
    "Bulbizarre": {"evolution": "Herbizarre", "niveau": 5},
    "Herbizarre": {"evolution": "Florizarre", "niveau": 10},
    "Salamèche": {"evolution": "Reptincel", "niveau": 5},
    "Reptincel": {"evolution": "Dracaufeu", "niveau": 10},
    "Carapuce": {"evolution": "Carabaffe", "niveau": 5},
    "Carabaffe": {"evolution": "Tortank", "niveau": 10},
    "Pikachu": {"evolution": "Raichu", "niveau": 7}
}

def augmenter_niveau(pokemon):
    """
    Augmente le niveau du Pokémon après un combat gagné.
    Vérifie si une évolution est possible et l'applique.
    """
    if "niveau" not in pokemon:
        pokemon["niveau"] = 1  

    pokemon["niveau"] += 1
    print(f"✨ {pokemon['nom']} est maintenant niveau {pokemon['niveau']} !")


    if pokemon["nom"] in evolution_data:
        evo_info = evolution_data[pokemon["nom"]]
        if pokemon["niveau"] >= evo_info["niveau"]:
            print(f"🔥 {pokemon['nom']} évolue en {evo_info['evolution']} !")
            evolution = get_pokemon_data(evo_info["evolution"])
            if evolution:
                pokemon.update(evolution) 
                pokemon["niveau"] = evo_info["niveau"]  
            else:
                print(f"⚠️ Erreur : Données de {evo_info['evolution']} introuvables.")
