# main_fixed.py
import pygame
import numpy as np
import sys
import random
import os
import copy

# --- Importations des classes métier (doivent exister dans le même dossier/projet) ---
from joueur import Inventaire, Joueur
from aleatoire import GenerateurAlea
from porte import Porte
from manoir import Manoir
from salle import Salle
from salles_speciales import EntranceHall, Antechamber
from catalogue_salle import (
    creer_salles_bleues,
    creer_salles_verte,
    creer_salles_viollette,
    creer_salles_orange,
    creer_salles_jaune,
    creer_salles_rouge
)

# === CONFIGURATION DE BASE ===
ROWS, COLS = 9, 5

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = int(info.current_w * 0.8)
SCREEN_HEIGHT = int(info.current_h * 0.8)

TILE_SIZE = SCREEN_HEIGHT // ROWS
WIDTH = TILE_SIZE * COLS
INVENTORY_WIDTH = SCREEN_WIDTH - WIDTH
SCREEN_HEIGHT = TILE_SIZE * ROWS

# --- COULEURS (Blueprint style) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)

BLUEPRINT_BG = (30, 30, 90)
BLUEPRINT_GRID_COLOR = (120, 120, 255)
BLUEPRINT_TEXT_COLOR = (180, 200, 255)
DARK_GRAY = (20, 20, 30)
GREEN_HELP = (50, 150, 50)

PIECE_COLORS = {
    "bleue": (100, 100, 255), "verte": (100, 200, 100), "violette": (180, 100, 180),
    "orange": (255, 165, 0), "rouge": (255, 100, 100), "jaune": (255, 255, 100),
}

# fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Interface Fusionnée")
clock = pygame.time.Clock()

# fonts
try:
    font_emoji = pygame.font.SysFont('segoeuiemoji', 28)
except Exception:
    font_emoji = pygame.font.SysFont(None, 28)
font = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 22)
font_title = pygame.font.SysFont(None, 36)
font_button = pygame.font.SysFont(None, 60, bold=True)

# === MENU / START SCREEN STATE & ASSETS ===
menu_active = True
exit_button_rect = pygame.Rect(0, 0, 0, 0)
help_button_rect = pygame.Rect(0, 0, 0, 0)
play_button_rect = None

# Charger l'image du menu depuis img/jeu.jpg (robuste)
menu_background = None
menu_path = os.path.join("img", "jeu.jpg")
if os.path.exists(menu_path):
    try:
        # convert_alpha pour conserver transparence si png, sinon convert ok
        menu_background = pygame.image.load(menu_path)
        # si surface a alpha, on garde convert_alpha, sinon convert
        try:
            menu_background = menu_background.convert_alpha()
        except Exception:
            menu_background = menu_background.convert()
        menu_background = pygame.transform.smoothscale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"[WARN] Impossible de charger l'image de menu '{menu_path}': {e}")
        menu_background = None
else:
    # print pour debug utile
    #print(f"[INFO] menu image not found at {menu_path}, using blueprint background")
    menu_background = None

# === CHARGEMENT IMAGES SALLES ===
def charger_image(nom_fichier):
    chemin = os.path.join("images", nom_fichier)
    if os.path.exists(chemin):
        try:
            img = pygame.image.load(chemin)
            try:
                return img.convert_alpha()
            except Exception:
                return img.convert()
        except Exception:
            return None
    return None

images_pieces = {
    "Vault": charger_image("vault.png"),
    "Veranda": charger_image("veranda.png"),
    "Bedroom": charger_image("bedroom.png"),
    "Corridor": charger_image("corridor.png"),
    "Chapel": charger_image("chapel.png"),
    "Pantry": charger_image("pantry.png"),
    "Entrance Hall": charger_image("entrance_hall.png"),
}

images_cache = {}

def charger_image_salle(salle):
    global images_cache
    image_path = None
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

def salle_to_dict(salle):
    if isinstance(salle, dict):
        d = salle.copy()
        d["image"] = charger_image_salle(salle)
        return d
    return {
        "nom": salle.nom,
        "couleur": salle.couleur,
        "image_path": getattr(salle, "image_path", None),
        "image": charger_image_salle(salle),
        "cout_gem": getattr(salle, "cout_gem", 0),
        "rarete": getattr(salle, "rarete", 0),
        "porte": getattr(salle, "porte", {}),
        "objets_initiaux": getattr(salle, "objets_initiaux", []),
        "effet": getattr(salle, "effet", None),
    }

def get_rotation_angle_for_placement(target_r, target_c):
    if target_r == 0: return 180
    if target_r == ROWS - 1: return 0
    if target_c == 0: return 90
    if target_c == COLS - 1: return 270
    return 0

def rotate_piece(piece_dict, angle_deg):
    rotated_piece = piece_dict.copy()
    portes_originales = piece_dict.get("porte", {})
    portes_rotatives = {}
    rotation_map = {}
    if angle_deg == 90: rotation_map = {"N": "E", "E": "S", "S": "O", "O": "N"}
    elif angle_deg == 180: rotation_map = {"N": "S", "E": "O", "S": "N", "O": "E"}
    elif angle_deg == 270: rotation_map = {"N": "O", "O": "S", "S": "E", "E": "N"}
    else: return piece_dict
    for old_dir, new_dir in rotation_map.items():
        portes_rotatives[new_dir] = portes_originales.get(old_dir, False)
    rotated_piece["porte"] = portes_rotatives
    img = piece_dict.get("image")
    if img:
        rotated_piece["image"] = pygame.transform.rotate(img, angle_deg)
    return rotated_piece

def tirer_pieces(catalogue, n=3):
    pieces_list = []; poids_list = []; pieces_gratuites = []
    for piece in catalogue:
        if hasattr(piece, 'rarete'):
            rarete = piece.rarete; cout_gem = piece.cout_gem
        else:
            rarete = piece.get("rarete", 0); cout_gem = piece.get("cout_gem", 0)
        poids = 1.0 / (3 ** rarete)
        pieces_list.append(piece); poids_list.append(poids)
        if cout_gem == 0: pieces_gratuites.append(piece)
    if not pieces_list: return []
    tirage = np.random.choice(pieces_list, size=n, p=np.array(poids_list)/sum(poids_list),
                              replace=False if len(pieces_list) >= n and n > 0 else True).tolist()
    if pieces_gratuites and not any((hasattr(p, 'cout_gem') and p.cout_gem == 0) or (isinstance(p, dict) and p.get("cout_gem", 0) == 0) for p in tirage):
        tirage[random.randint(0, n-1)] = random.choice(pieces_gratuites)
    return tirage

def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# === ETAT DU JEU ===
player_pos = [ROWS - 1, COLS // 2]
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
salle_depart_obj = EntranceHall()
grid[player_pos[0]][player_pos[1]] = salle_to_dict(salle_depart_obj)

catalogue_pieces = []
catalogue_pieces.extend(creer_salles_bleues())
catalogue_pieces.extend(creer_salles_verte())
catalogue_pieces.extend(creer_salles_viollette())
catalogue_pieces.extend(creer_salles_orange())
catalogue_pieces.extend(creer_salles_jaune())
catalogue_pieces.extend(creer_salles_rouge())

inventory = {
    "Pas": 96, "Gemmes": 2, "Clés": 0, "Dés": 1, "Pièces d'or": 0,
    "Pelle": True, "Crochetage": False, "Détecteur": True, "Patte de lapin": False, "Marteau": False
}

message_action = ""
choix_en_cours = False
index_selection = 0
pieces_proposees = []
intended_dir = None

# === DESSIN ===
def draw_start_screen():
    """Affiche le menu; si menu_background existe on l'affiche, sinon fallback blueprint."""
    global play_button_rect, menu_background

    # draw background image if present, else blueprint pattern
    if menu_background:
        # blit l'image entière (déjà scalée au chargement)
        screen.blit(menu_background, (0, 0))
    else:
        screen.fill(BLUEPRINT_BG)
        step = 60
        for x in range(0, SCREEN_WIDTH, step):
            pygame.draw.line(screen, BLUEPRINT_GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, step):
            pygame.draw.line(screen, BLUEPRINT_GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)

    # titre
    title_surf = font_title.render("BLUE PRINCE", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title_surf, ((SCREEN_WIDTH - title_surf.get_width()) // 2, SCREEN_HEIGHT // 4))

    # bouton JOUER (retourné pour debug/usage)
    button_w, button_h = 360, 100
    bx = (SCREEN_WIDTH - button_w) // 2
    by = SCREEN_HEIGHT // 2
    play_button_rect = pygame.Rect(bx, by, button_w, button_h)

    # hover effect
    mx, my = pygame.mouse.get_pos()
    if bx <= mx <= bx + button_w and by <= my <= by + button_h:
        color = BLUEPRINT_GRID_COLOR
    else:
        color = (60, 90, 180)

    pygame.draw.rect(screen, color, play_button_rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, play_button_rect, 4, border_radius=12)

    play_text = font_button.render("JOUER", True, WHITE)
    screen.blit(play_text, (bx + (button_w - play_text.get_width()) // 2, by + (button_h - play_text.get_height()) // 2))

    inst = font_small.render("Cliquez sur JOUER ou appuyez sur ENTREE", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(inst, ((SCREEN_WIDTH - inst.get_width()) // 2, by + button_h + 20))

    return play_button_rect

def draw_grid():
    screen.fill(BLUEPRINT_BG, pygame.Rect(0, 0, WIDTH, SCREEN_HEIGHT))
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            piece = grid[row][col]
            if piece:
                image = piece.get("image")
                if image:
                    image_scaled = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    screen.blit(image_scaled, (x, y))
                else:
                    couleur = piece.get("couleur", "bleue")
                    color = PIECE_COLORS.get(couleur, GRAY)
                    pygame.draw.rect(screen, color, rect)
                    text = font_small.render(piece.get("nom", "???"), True, WHITE)
                    screen.blit(text, (x + 5, y + 5))
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
            pygame.draw.rect(screen, BLUEPRINT_GRID_COLOR, rect, 1)
    grid_rect_full = pygame.Rect(0, 0, WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BLUEPRINT_GRID_COLOR, grid_rect_full, 4)
    global_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, WHITE, global_rect, 5)
    # curseur joueur
    r, c = player_pos
    pygame.draw.rect(screen, RED, pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 4)

def draw_inventory(inv):
    global exit_button_rect, help_button_rect
    x_start = WIDTH + 20
    y = 20
    screen.fill(BLUEPRINT_BG, pygame.Rect(WIDTH, 0, INVENTORY_WIDTH, SCREEN_HEIGHT))
    help_text = font_small.render("AIDE", True, WHITE)
    help_button_width = help_text.get_width() + 15
    help_button_rect = pygame.Rect(WIDTH + INVENTORY_WIDTH - help_button_width - 15, 25, help_button_width, 30)
    pygame.draw.rect(screen, GREEN_HELP, help_button_rect, border_radius=5)
    pygame.draw.rect(screen, BLUEPRINT_GRID_COLOR, help_button_rect, 1, border_radius=5)
    screen.blit(help_text, (help_button_rect.x + 5, help_button_rect.y + 5))

    title = font_title.render("INVENTAIRE", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title, (x_start, y)); y += 50

    resources = [
        ("Pas", "🚶", inv.get("Pas", 0)), ("Gemmes", "💎", inv.get("Gemmes", 0)),
        ("Clés", "🔑", inv.get("Clés", 0)), ("Dés", "🎲", inv.get("Dés", 0)),
        ("Pièces d'or", "🪙", inv.get("Pièces d'or", 0))
    ]

    max_width = INVENTORY_WIDTH - 20
    for name, icon, value in resources:
        name_text = font.render(name, True, BLUEPRINT_TEXT_COLOR)
        val_icon_text = font_emoji.render(f"{value} {icon}", True, BLUEPRINT_TEXT_COLOR)
        screen.blit(name_text, (x_start, y))
        val_icon_x = WIDTH + max_width - val_icon_text.get_width()
        screen.blit(val_icon_text, (val_icon_x, y))
        y += 35

    y += 20
    title_perm = font_small.render("OBJETS PERMANENTS:", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title_perm, (x_start, y)); y += 30
    perm_rect = pygame.Rect(WIDTH + 10, y - 5, INVENTORY_WIDTH - 20, 150)
    pygame.draw.rect(screen, BLUEPRINT_GRID_COLOR, perm_rect, 2)

    permanent_items = [
        ("Pelle", inv.get("Pelle", False)), ("Marteau", inv.get("Marteau", False)),
        ("Crochetage", inv.get("Crochetage", False)), ("Détecteur", inv.get("Détecteur", False)),
        ("Patte de lapin", inv.get("Patte de lapin", False))
    ]
    for name, possede in permanent_items:
        if possede:
            text = font_small.render(name.upper(), True, BLUEPRINT_TEXT_COLOR)
            screen.blit(text, (x_start + 10, y)); y += 25

    if message_action:
        y_msg = SCREEN_HEIGHT - 80
        msg_rect = pygame.Rect(WIDTH + 10, y_msg - 5, INVENTORY_WIDTH - 20, 70)
        pygame.draw.rect(screen, BLUEPRINT_GRID_COLOR, msg_rect, 2)
        yy = y_msg
        for line in message_action.split('\n'):
            msg_text = font_small.render(line, True, BLUEPRINT_TEXT_COLOR)
            screen.blit(msg_text, (x_start, yy)); yy += 25

    button_x = WIDTH + INVENTORY_WIDTH - 120
    button_y = SCREEN_HEIGHT - 60
    exit_button_rect = pygame.Rect(button_x, button_y, 100, 40)
    pygame.draw.rect(screen, RED, exit_button_rect, border_radius=5)
    exit_text = font_small.render("QUITTER", True, WHITE)
    text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, text_rect)

def draw_selection_menu():
    if not choix_en_cours:
        return
    dir_text = {(-1, 0): "Vers le HAUT", (1, 0): "Vers le BAS", (0, -1): "Vers la GAUCHE", (0, 1): "Vers la DROITE"}.get(intended_dir, "Direction")
    x_base = WIDTH + 20; y_start = 150
    title = font.render(f"Choix ({dir_text})", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title, (x_base, y_start - 40))
    for i, piece in enumerate(pieces_proposees):
        y = y_start + i * 130
        nom = piece.nom if hasattr(piece, 'nom') else piece.get("nom", "???")
        cout_gem = piece.cout_gem if hasattr(piece, 'cout_gem') else piece.get("cout_gem", piece.get("gemmes", 0))
        rarete = piece.rarete if hasattr(piece, 'rarete') else piece.get("rarete", 0)
        couleur = piece.couleur if hasattr(piece, 'couleur') else piece.get("couleur", "bleue")
        rect = pygame.Rect(x_base, y, INVENTORY_WIDTH - 40, 120)
        bg_color = (255, 200, 200) if i == index_selection else (40, 40, 70)
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, RED if i == index_selection else BLUEPRINT_GRID_COLOR, rect, 3)
        image = charger_image_salle(piece)
        if image:
            img_scaled = pygame.transform.scale(image, (100, 100))
            screen.blit(img_scaled, (x_base + 10, y + 10))
        else:
            color_rect = pygame.Rect(x_base + 10, y + 10, 100, 100)
            color = PIECE_COLORS.get(couleur, GRAY)
            pygame.draw.rect(screen, color, color_rect)
        text_x = x_base + 120
        screen.blit(font.render(nom, True, BLUEPRINT_TEXT_COLOR), (text_x, y + 15))
        gemmes_text = f"💎 {cout_gem} gemmes" if cout_gem > 0 else "Gratuit"
        screen.blit(font_small.render(gemmes_text, True, BLUEPRINT_TEXT_COLOR), (text_x, y + 50))
        rarete_text = font_small.render(f"Rareté: {rarete}", True, BLUEPRINT_TEXT_COLOR)
        screen.blit(rarete_text, (text_x, y + 75))

# === LOGIQUE ===
def handle_move(direction):
    global choix_en_cours, pieces_proposees, index_selection, intended_dir, message_action, inventory, player_pos
    dy, dx = direction
    current_r, current_c = player_pos
    target_r, target_c = current_r + dy, current_c + dx
    direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
    dir_key = direction_map.get(direction)
    if inventory["Pas"] <= 0:
        message_action = "💀 Défaite : vous n'avez plus de pas!"
        return False
    if not in_bounds(target_r, target_c):
        message_action = "Mur extérieur : Limite du manoir atteinte."
        return False
    current_room = grid[current_r][current_c]
    if current_room and current_room.get("porte", {}).get(dir_key) is not True:
        message_action = f"Mur interne : La salle '{current_room['nom']}' n'a pas de porte vers {dir_key}."
        return False
    target_room = grid[target_r][target_c]
    if target_room is not None:
        inventory["Pas"] -= 1
        player_pos[0], player_pos[1] = target_r, target_c
        message_action = f"Déplacement vers {target_room['nom']} ({inventory['Pas']} pas restants)."
        return True
    else:
        inventory["Pas"] -= 1
        pieces_proposees.clear()
        pieces_proposees.extend(tirer_pieces(catalogue_pieces, n=3))
        index_selection = 0
        choix_en_cours = True
        intended_dir = direction
        message_action = "Sélectionnez une nouvelle pièce."
        return True

def place_selected_piece(idx):
    global choix_en_cours, intended_dir, message_action, inventory, catalogue_pieces, player_pos
    piece = pieces_proposees[idx]
    if piece in catalogue_pieces:
        catalogue_pieces.remove(piece)
    dy, dx = intended_dir
    target_r = player_pos[0] + dy
    target_c = player_pos[1] + dx
    cout_gem = piece.cout_gem if hasattr(piece, 'cout_gem') else piece.get("cout_gem", piece.get("gemmes", 0))
    nom = piece.nom if hasattr(piece, 'nom') else piece.get("nom", "???")
    if cout_gem > inventory["Gemmes"]:
        message_action = "Pas assez de gemmes! (Pas remboursé)"
        inventory["Pas"] += 1
        choix_en_cours = False
        intended_dir = None
        return False
    piece_dict = salle_to_dict(piece)
    angle = get_rotation_angle_for_placement(target_r, target_c)
    if angle != 0:
        piece_dict = rotate_piece(piece_dict, angle)
    if in_bounds(target_r, target_c) and grid[target_r][target_c] is None:
        grid[target_r][target_c] = piece_dict
        player_pos[0], player_pos[1] = target_r, target_c
        inventory["Gemmes"] -= cout_gem
        message_action = f"Vous entrez dans {nom}."
    else:
        message_action = "Erreur logique: La pièce n'a pas été placée."
    choix_en_cours = False
    intended_dir = None
    return True

# === BOUCLE PRINCIPALE ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # menu actif : on gère uniquement les événements du menu
        if menu_active:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # calculer rect du bouton JOUER (même position que dans draw_start_screen)
                button_w, button_h = 360, 100
                bx = (SCREEN_WIDTH - button_w) // 2; by = SCREEN_HEIGHT // 2
                rect_now = pygame.Rect(bx, by, button_w, button_h)
                if rect_now.collidepoint(event.pos):
                    menu_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_active = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            # ignorer le reste tant que menu actif
            continue

        # clics en jeu (aide, quitter)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if exit_button_rect.collidepoint(mouse_pos):
                pygame.quit(); sys.exit()
            if help_button_rect.collidepoint(mouse_pos):
                choix_en_cours = False
                message_action = "AIDE: Déplacez-vous avec ZQSD ou les flèches.\nTrouvez l'Antichambre pour gagner."

        # gestion clavier en jeu
        if event.type == pygame.KEYDOWN:
            if choix_en_cours:
                if event.key in (pygame.K_UP, pygame.K_z):
                    index_selection = (index_selection - 1) % max(1, len(pieces_proposees))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    index_selection = (index_selection + 1) % max(1, len(pieces_proposees))
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if pieces_proposees:
                        place_selected_piece(index_selection)
                elif event.key == pygame.K_ESCAPE:
                    choix_en_cours = False; intended_dir = None; message_action = "Sélection annulée."
            else:
                if event.key in (pygame.K_z, pygame.K_UP):
                    handle_move((-1, 0))
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    handle_move((1, 0))
                elif event.key in (pygame.K_q, pygame.K_LEFT):
                    handle_move((0, -1))
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    handle_move((0, 1))

    # DESSIN
    if menu_active:
        play_button_rect = draw_start_screen()
    else:
        screen.fill(BLUEPRINT_BG)
        draw_grid()
        draw_inventory(inventory)
        draw_selection_menu()

    pygame.display.flip()
    clock.tick(30)