import pygame
import json
import random
import sys

class Map:
    pass

def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {image_path}")
        raise SystemExit(e)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Map")

    # List of images
    images = [
        "main_code/template/temp1.webp",
        "main_code/template/temp2.png"
    ]

    # Choose a random image
    chosen_image_path = random.choice(images)
    chosen_image = load_image(chosen_image_path)

    # Resize image if necessary
    chosen_image = pygame.transform.scale(chosen_image, (800, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen with black
        screen.blit(chosen_image, (0, 0))  # Draw chosen image

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()