import pygame
import numpy as np
import sys
import random
import os
import copy
from salles_speciales import EntranceHall, Antechamber
from catalogue_salle import (
    creer_salles_bleues, 
    creer_salles_verte, 
    creer_salles_viollette,
    creer_salles_orange,
    creer_salles_jaune,
    creer_salles_rouge
)
from objets import *
from aleatoire import GenerateurAlea 

class Jeu:
    # Constantes globales du jeu (basées sur la grille 9x5)
    ROWS, COLS = 9, 5

    def __init__(self):
        pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

TILE_SIZE = SCREEN_HEIGHT // ROWS
WIDTH = TILE_SIZE * COLS
INVENTORY_WIDTH = SCREEN_WIDTH - WIDTH
SCREEN_HEIGHT = TILE_SIZE * ROWS 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
YELLOW_CURSOR = (255, 255, 0, 100) 

BLUEPRINT_BG = (30, 30, 90)
BLUEPRINT_GRID_COLOR = (120, 120, 255)
BLUEPRINT_TEXT_COLOR = (180, 200, 255)
DARK_GRAY = (20, 20, 30)
GREEN_HELP = (50, 150, 50)

PIECE_COLORS = {
    "bleue": (100, 100, 255), "verte": (100, 200, 100), "violette": (180, 100, 180),
    "orange": (255, 165, 0), "rouge": (255, 100, 100), "jaune": (255, 255, 100),
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Blue Prince - Interface Fusionnée")
clock = pygame.time.Clock()

try:
    font_emoji = pygame.font.SysFont('segoeuiemoji', 28)
except Exception:
    font_emoji = pygame.font.SysFont(None, 28)
font = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 22)
font_title = pygame.font.SysFont(None, 36)
font_button = pygame.font.SysFont(None, 60, bold=True)
font_game_over = pygame.font.SysFont(None, 100, bold=True) 


# === GESTIONNAIRES D'IMAGES ===
menu_background = None
images_cache = {}

def load_all_assets():
    global menu_background, images_cache
    
    images_cache = {} 
    
    menu_path = os.path.join("img", "jeu.jpg")
    if os.path.exists(menu_path):
        try:
            menu_background = pygame.image.load(menu_path)
            try:
                menu_background = menu_background.convert_alpha()
            except Exception:
                menu_background = menu_background.convert()
            menu_background = pygame.transform.smoothscale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"[WARN] Impossible de charger l'image de menu '{menu_path}': {e}")
            menu_background = None
    else:
        menu_background = None

def charger_image_salle(salle):
    global images_cache
    image_path = None
    
    if salle is None:
        return None

    if hasattr(salle, 'image_path'):
        image_path = salle.image_path
    else:
        image_path = salle.get("image_path", None) if isinstance(salle, dict) else None

    if not image_path:
        return None

    if image_path in images_cache:
        return images_cache[image_path]

    
    possibles = [image_path, os.path.join("images", image_path), os.path.join("img", image_path)]
    for p in possibles:
        if os.path.exists(p):
            try:
                img = pygame.image.load(p)
                try:
                    img = img.convert_alpha()
                except Exception:
                    img = img.convert()
                images_cache[image_path] = img
                return img
            except Exception:
                continue
    images_cache[image_path] = None
    return None

# === ETAT DU JEU (Variables Globales) ===
player_pos = []
grid = [[]]
inventaire = None
catalogue_pieces = []
message_action = ""
choix_en_cours = False
index_selection = 0
pieces_proposees = []
intended_dir = None
exit_button_rect = pygame.Rect(0, 0, 0, 0)
help_button_rect = pygame.Rect(0, 0, 0, 0)
play_button_rect = None

selected_move_direction = None

menu_active = True
game_over = False
game_won = False

just_cancelled_selection = False

generateur_alea = None 

def reset_game():
    global player_pos, grid, inventaire, catalogue_pieces, message_action, choix_en_cours
    global index_selection, pieces_proposees, intended_dir, menu_active, game_over, game_won
    global selected_move_direction, just_cancelled_selection, generateur_alea
    
    player_pos = [ROWS - 1, COLS // 2]
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    
    inventaire = Inventaire() 
    generateur_alea = GenerateurAlea() 

    # --- PLACEMENT DE L'ENTRANCE HALL (Bas Centre) ---
    salle_depart_obj = EntranceHall()
    grid[player_pos[0]][player_pos[1]] = salle_to_dict(salle_depart_obj)

    # --- AJOUT CRITIQUE : PLACEMENT DE L'ANTICHAMBRE (Haut Centre) ---
    salle_fin_obj = Antechamber()
    grid[0][COLS // 2] = salle_to_dict(salle_fin_obj) 
    # -----------------------------------------------------------------

    catalogue_pieces = []
    catalogue_pieces.extend(creer_salles_bleues())
    catalogue_pieces.extend(creer_salles_verte())
    catalogue_pieces.extend(creer_salles_viollette())
    catalogue_pieces.extend(creer_salles_orange())
    catalogue_pieces.extend(creer_salles_jaune())
    catalogue_pieces.extend(creer_salles_rouge())

    message_action = "Bienvenue ! (ZQSD/Flèches pour viser, Espace pour bouger)"
    choix_en_cours = False
    index_selection = 0
    pieces_proposees = []
    intended_dir = None
    
    selected_move_direction = None
    just_cancelled_selection = False
    
    menu_active = True
    game_over = False
    game_won = False