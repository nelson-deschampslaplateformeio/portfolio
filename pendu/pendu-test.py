import pygame
import random
import sys
import os

# ----------------------------------------------Interface-----------------------
# Pygame initialisation 
pygame.init()

# Showing the interface
display_width = 800
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Main menu")

# main colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 36)

# Global variables
player_name = ""
selected_level = None
difficulty_attempts = {"Light": 10, "Middle": 7, "Hard": 5}
words_file = "words.txt"
score_file = "scores.txt"
score = 0

# ------------------------------Utility Functions-----------------------

# Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, padding=5):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(window, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, default_color, (x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    window.blit(text_surface, text_rect)

# Load words from a file with validation
def load_words(words_file):
    if not os.path.exists(words_file):
        with open(words_file, "w", encoding="utf-8") as file:
            file.write("example\n")  # Default word

    with open(words_file, "r", encoding="utf-8") as file:
        content = file.read().strip()
    
    if content:  # Check if content is not empty
        levels = content.split("\n\n")
        if len(levels) == 3:  # Check if there are 3 levels (easy, medium, hard)
            easy_words = levels[0].split("\n")  
            medium_words = levels[1].split("\n")  
            hard_words = levels[2].split("\n")
        else:
            easy_words, medium_words, hard_words = [], [], []  # Empty lists if format is wrong
    else:
        easy_words, medium_words, hard_words = [], [], []

    return easy_words, medium_words, hard_words

def load_words_by_level():
    easy_words, medium_words, hard_words = load_words(words_file)  
    
    if selected_level == "Easy":
        return easy_words
    elif selected_level == "Medium":
        return medium_words
    elif selected_level == "Hard":
        return hard_words
    else:
        return []  # Return empty list if no level selected

def select_easy():
    global selected_level
    selected_level = "Easy"
    start_game()

def select_medium():
    global selected_level
    selected_level = "Medium"
    start_game()

def select_hard():
    global selected_level
    selected_level = "Hard"
    start_game()

# Choose word function
def choose_word(words):
    return random.choice(words)

# Save scores
def save_score(name, score):
    with open(score_file, "a", encoding="utf-8") as file:
        file.write(f"{name}: {score}\n")

# ------------------------------------------------------Main Menu-----------------------------------------------------
def main_menu():
    global selected_level 
    running = True
    while running:
        window.fill(WHITE)

        draw_button(300, 190, 200, 50, "Enter your name", GRAY, HIGHLIGHT, enter_name)
        draw_button(300, 250, 200, 50, "The level", GRAY, HIGHLIGHT, level_menu)
        draw_button(300, 320, 200, 50, "Play", GRAY, HIGHLIGHT, start_game)
        draw_button(300, 390, 200, 50, "Add new word", GRAY, HIGHLIGHT, add_word)
        draw_button(300, 460, 200, 50, "Watch score", GRAY, HIGHLIGHT, score_list)
        draw_button(300, 530, 200, 50, "Exit", GRAY, HIGHLIGHT, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

# --------------------------------------------------Add new word------------------------------------------
def add_word():
    # Interface for adding a new word
    running = True
    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ""
    active = False
    font_input = pygame.font.Font(None, 36)

    while running:
        window.fill(WHITE)
        pygame.draw.rect(window, color, input_box)

        draw_button(300, 400, 200, 50, "Confirm", GRAY, HIGHLIGHT, lambda: confirm_word(text))
        draw_button(300, 470, 200, 50, "Back", GRAY, HIGHLIGHT, main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font_input.render(text, True, BLACK)
        window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.flip()

def confirm_word(word):
    # Confirm the word and save it to the file
    if word.isalpha():
        with open(words_file, "a", encoding="utf-8") as file:
            file.write(word + "\n")
        print(f"Word '{word}' added successfully!")
    else:
        print("Invalid word. Please enter a valid word.")
    main_menu()

# Start the game
def start_game():
    global selected_level, player_name, score
    if selected_level is None: 
        print("Error: Level not selected!")  
        return 
    
    print(f"Starting game with level: {selected_level}")

    words = load_words_by_level()
    if not words:  # If no words for selected level
        print("No words available for this level.")
        return
    
    word = choose_word(words).upper()
    guessed = ["_" for _ in word]
    guessed_letters = set()
    attempts_left = 6
    score = 0
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    running = True
    while running:
        window.fill(WHITE)

        # Handle the hangman and word
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key).upper() 
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter in word:
                            for i, l in enumerate(word):
                                if l == letter:
                                    guessed[i] = letter
                        else:
                            attempts_left -= 1

        # -----------------------------Win/lost
        if "_" not in guessed:
            score += 1
            end_message(f"Congratulations, {player_name}! You Win!", GREEN)
            selected_level = None
            return

        if attempts_left == 0:
            end_message(f"Sorry, {player_name}. You Lose! The word was {word}", RED)
            save_score(player_name, score)
            selected_level = None
            return

def end_message(message, color):
    window.fill(WHITE)
    font = pygame.font.Font(None, 40)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(display_width // 2, display_height // 2))
    window.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    main_menu()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
