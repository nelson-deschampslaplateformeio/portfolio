import os
import requests
import pygame
from io import BytesIO

def get_first_151_pokemon():
    """
    Récupère la liste des 151 premiers Pokémon depuis l'API PokéAPI.
    Retourne une liste de noms.
    """
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [pokemon["name"] for pokemon in data["results"]]
    else:
        print("Erreur lors de la récupération des Pokémon")
        return []

def get_pokemon_sprites(name):
    """
    Récupère les URL des sprites de face et de dos pour un Pokémon donné.
    Retourne un dictionnaire avec les clés 'front' et 'back'.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sprites = data.get("sprites", {})
        return {
            "front": sprites.get("front_default"),
            "back": sprites.get("back_default")
        }
    else:
        print(f"Erreur lors de la récupération des données pour {name}")
        return {"front": None, "back": None}

def download_and_save_image(url, path):
    """
    Télécharge l'image depuis l'URL et l'enregistre sur le disque à l'emplacement spécifié.
    Retourne True en cas de succès, False sinon.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print("Erreur lors du téléchargement de l'image :", e)
    return False

def main():
  
    pygame.init()
    
  
    os.makedirs("sprites", exist_ok=True)
    

    pokemon_names = get_first_151_pokemon()
    print(f"Récupération des sprites pour {len(pokemon_names)} Pokémon...")
    
    for name in pokemon_names:
        sprites = get_pokemon_sprites(name)
        print(f"{name}: front={sprites['front']}, back={sprites['back']}")
        
   
        if sprites["front"]:
            front_path = os.path.join("sprites", f"{name.lower()}_front.png")
            if download_and_save_image(sprites["front"], front_path):
                print(f"Sprite de face pour {name} enregistré dans {front_path}")
            else:
                print(f"Erreur lors de l'enregistrement du sprite de face pour {name}")
        
    
        if sprites["back"]:
            back_path = os.path.join("sprites", f"{name.lower()}_back.png")
            if download_and_save_image(sprites["back"], back_path):
                print(f"Sprite de dos pour {name} enregistré dans {back_path}")
            else:
                print(f"Erreur lors de l'enregistrement du sprite de dos pour {name}")
    
    print("Téléchargement terminé.")

if __name__ == "__main__":
    main()
