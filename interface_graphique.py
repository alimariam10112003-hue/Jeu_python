import pygame
import sys
import random
import os
import copy
from catalogue_salle import (
    creer_salles_bleues, 
    creer_salles_verte, 
    creer_salles_viollette,
    creer_salles_orange,
    creer_salles_jaune,
    creer_salles_rouge
)

# === CONFIGURATION DE BASE ===
ROWS, COLS = 9, 5  # taille du manoir (lignes, colonnes)

# === INITIALISATION PYGAME & FENETRE ADAPTATIVE ===
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = int(info.current_w * 0.8)
SCREEN_HEIGHT = int(info.current_h * 0.8)

# Calcul dynamique de la taille des tuiles et de l'inventaire
TILE_SIZE = SCREEN_HEIGHT // ROWS
WIDTH = TILE_SIZE * COLS
INVENTORY_WIDTH = SCREEN_WIDTH - WIDTH
SCREEN_HEIGHT = TILE_SIZE * ROWS

# === COULEURS ===
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
BLACK = (0, 0, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (50, 50, 50)

PIECE_COLORS = {
    "bleue": (100, 100, 255),
    "verte": (100, 200, 100),
    "violette": (180, 100, 180),
    "orange": (255, 165, 0),
    "rouge": (255, 100, 100),
    "jaune": (255, 255, 100),
}

# === FENETRE ===
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Interface")
clock = pygame.time.Clock()

# === POLICES ===
font = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 22)
font_title = pygame.font.SysFont(None, 36)

# Police emoji (optionnelle)
try:
    emoji_font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", 30)
except:
    print("Avertissement: Police emoji non trouvée. Les emojis peuvent ne pas s'afficher.")
    emoji_font = pygame.font.SysFont(None, 30)

# === CHARGEMENT DES IMAGES ===
def charger_image(nom_fichier):
    chemin = os.path.join("images", nom_fichier)
    if os.path.exists(chemin):
        try:
            return pygame.image.load(chemin)
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

# === ETAT INITIAL DU JEU ===
player_pos = [ROWS - 1, COLS // 2]  # Départ centré en bas
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Création du catalogue complet
catalogue_pieces_original = (
    creer_salles_bleues() +
    creer_salles_verte() +
    creer_salles_viollette() +
    creer_salles_orange() +
    creer_salles_jaune() +
    creer_salles_rouge()
)

catalogue_pieces = catalogue_pieces_original.copy()

# Pièce de départ
grid[player_pos[0]][player_pos[1]] = {
    "nom": "Entrance Hall",
    "couleur": "bleue",
    "image": charger_image("entrance_hall.png")
}

# === INVENTAIRE ===
inventory = {
    "Pas": 96,
    "Gemmes": 2,
    "Clés": 0,
    "Dés": 1,
    "Pièces d'or": 0,
    "Pelle": True,
    "Crochetage": False,
    "Détecteur": True,
    "Patte de lapin": False,
    "Marteau": False
}

# === VARIABLES DE CONTROLE ===
message_action = ""
choix_en_cours = False
index_selection = 0
pieces_proposees = []
intended_dir = None
images_cache = {}

# === UTILITAIRES ===
def charger_image_salle(salle):
    """Charge l'image d'une salle (avec cache)"""
    image_path = salle.image_path if hasattr(salle, 'image_path') else salle.get('image_path', f"img/{salle['nom'].lower().replace(' ', '_')}.png")
    if image_path in images_cache:
        return images_cache[image_path]
    if os.path.exists(image_path):
        try:
            img = pygame.image.load(image_path)
            images_cache[image_path] = img
            return img
        except Exception:
            return None
    return None

def salle_to_dict(salle):
    """Convertit un objet Salle en dictionnaire pour la grille"""
    if isinstance(salle, dict):
        return salle
    return {
        "nom": salle.nom,
        "couleur": salle.couleur,
        "image_path": salle.image_path,
        "cout_gem": salle.cout_gem,
        "rarete": salle.rarete,
        "porte": salle.porte,
        "objets_initiaux": salle.objets_initiaux,
        "effet": salle.effet,
        "image": charger_image_salle(salle)
    }

def tirer_pieces(catalogue, n=3):
    """Tirage aléatoire de n pièces selon la rareté"""
    pieces_disponibles = []
    for piece in catalogue:
        rarete = piece.rarete if hasattr(piece, 'rarete') else piece.get("rarete", 0)
        poids = 1 / (3 ** rarete)
        pieces_disponibles.append((piece, poids))

    tirage = random.choices([p[0] for p in pieces_disponibles],
                            weights=[p[1] for p in pieces_disponibles], k=n)

    # garantir au moins une pièce gratuite
    if not any((p.cout_gem if hasattr(p, 'cout_gem') else p.get("gemmes", 0)) == 0 for p in tirage):
        gratuites = [p for p in catalogue if (p.cout_gem if hasattr(p, 'cout_gem') else p.get("gemmes", 0)) == 0]
        if gratuites:
            tirage[random.randint(0, n - 1)] = random.choice(gratuites)

    return tirage

def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# === DESSIN DE LA GRILLE ===
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            piece = grid[row][col]

            if piece:
                image = piece.get("image") or charger_image_salle(piece)
                if image:
                    screen.blit(pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE)), (x, y))
                else:
                    color = PIECE_COLORS.get(piece.get("couleur", "bleue"), GRAY)
                    pygame.draw.rect(screen, color, rect)
                    text = font_small.render(piece.get("nom", "???"), True, WHITE)
                    screen.blit(text, (x + 5, y + 5))
            else:
                pygame.draw.rect(screen, BLACK, rect)

            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

            # Curseur joueur
            if [row, col] == player_pos:
                pygame.draw.rect(screen, RED, rect, 4)

# === INVENTAIRE ===
def draw_inventory(inv):
    x_start = WIDTH + 20
    y = 20
    screen.fill(WHITE, pygame.Rect(WIDTH, 0, INVENTORY_WIDTH, SCREEN_HEIGHT))

    title = font_title.render("Inventory:", True, BLACK)
    screen.blit(title, (x_start, y))
    y += 50

    resources = [
        ("Pas", "🚶", inv["Pas"]),
        ("Gemmes", "💎", inv["Gemmes"]),
        ("Clés", "🔑", inv["Clés"]),
        ("Dés", "🎲", inv["Dés"]),
        ("Pièces d'or", "🪙", inv["Pièces d'or"])
    ]

    for name, icon, value in resources:
        icon_text = emoji_font.render(icon, True, BLACK)
        val_text = font.render(str(value), True, BLACK)
        screen.blit(icon_text, (x_start, y))
        screen.blit(val_text, (x_start + 50, y))
        y += 35

    y += 20

    permanent_items = [
        ("Pelle", "Shovel"),
        ("Détecteur", "Metal Detector"),
        ("Patte de lapin", "Lucky Rabbit's Foot"),
        ("Crochetage", "Lockpick Kit"),
        ("Marteau", "Hammer")
    ]
    for key, display_name in permanent_items:
        if inv.get(key, False):
            text = font_small.render(display_name, True, BLACK)
            screen.blit(text, (x_start + 20, y))
            y += 30

    # Nom de la pièce actuelle
    y += 40
    current_room = grid[player_pos[0]][player_pos[1]]
    if current_room:
        room_title = font_title.render(current_room["nom"], True, BLACK)
        screen.blit(room_title, (x_start, y))
        y += 50

    # Message d’action
    if message_action:
        y = SCREEN_HEIGHT - 80
        for line in message_action.split('\n'):
            msg_text = font_small.render(line, True, BLACK)
            screen.blit(msg_text, (x_start, y))
            y += 25

# === MENU DE SELECTION ===
def draw_selection_menu():
    if not choix_en_cours:
        return

    directions = {(-1, 0): "Vers le HAUT", (1, 0): "Vers le BAS", (0, -1): "Vers la GAUCHE", (0, 1): "Vers la DROITE"}
    dir_text = directions.get(intended_dir, "Direction")

    x_base = WIDTH + 20
    y_start = 150
    screen.blit(font.render(f"Choix ({dir_text})", True, BLACK), (x_base, y_start - 40))

    for i, piece in enumerate(pieces_proposees):
        y = y_start + i * 130
        rect = pygame.Rect(x_base, y, INVENTORY_WIDTH - 40, 120)
        pygame.draw.rect(screen, (255, 200, 200) if i == index_selection else LIGHT_GRAY, rect)
        pygame.draw.rect(screen, RED if i == index_selection else BLACK, rect, 3)

        nom = getattr(piece, "nom", piece.get("nom", "???"))
        cout_gem = getattr(piece, "cout_gem", piece.get("gemmes", 0))
        rarete = getattr(piece, "rarete", piece.get("rarete", 0))
        couleur = getattr(piece, "couleur", piece.get("couleur", "bleue"))

        image = charger_image_salle(piece)
        if image:
            screen.blit(pygame.transform.scale(image, (100, 100)), (x_base + 10, y + 10))
        else:
            color = PIECE_COLORS.get(couleur, GRAY)
            pygame.draw.rect(screen, color, pygame.Rect(x_base + 10, y + 10, 100, 100))

        text_x = x_base + 120
        screen.blit(font.render(nom, True, BLACK), (text_x, y + 15))
        screen.blit(font_small.render(f"{cout_gem} gemmes" if cout_gem > 0 else "Gratuit", True, BLACK), (text_x, y + 50))
        screen.blit(font_small.render(f"Rareté: {rarete}", True, BLACK), (text_x, y + 75))

# === LOGIQUE DU JEU ===
def attempt_open_choice(direction):
    global choix_en_cours, pieces_proposees, index_selection, intended_dir, message_action
    dy, dx = direction
    target_r, target_c = player_pos[0] + dy, player_pos[1] + dx
    if not in_bounds(target_r, target_c):
        message_action = "Impossible d'aller dans cette direction!"
        return False
    pieces_proposees = tirer_pieces(catalogue_pieces, n=3)
    index_selection = 0
    choix_en_cours = True
    intended_dir = direction
    message_action = ""
    return True

def place_selected_piece(idx):
    global choix_en_cours, intended_dir, message_action, inventory, catalogue_pieces
    piece = pieces_proposees[idx]
    if piece in catalogue_pieces:
        catalogue_pieces.remove(piece)

    dy, dx = intended_dir
    target_r, target_c = player_pos[0] + dy, player_pos[1] + dx
    cout_gem = getattr(piece, "cout_gem", piece.get("gemmes", 0))
    nom = getattr(piece, "nom", piece.get("nom", "???"))

    if cout_gem > inventory["Gemmes"]:
        message_action = "Pas assez de gemmes!"
        return False

    piece_dict = salle_to_dict(piece)
    if in_bounds(target_r, target_c) and grid[target_r][target_c] is None:
        grid[target_r][target_c] = piece_dict
        player_pos[0], player_pos[1] = target_r, target_c
        inventory["Gemmes"] -= cout_gem
        inventory["Pas"] -= 1
        message_action = f"Vous entrez dans {nom}."
    else:
        grid[player_pos[0]][player_pos[1]] = piece_dict
        message_action = "Pièce placée sur votre position."

    choix_en_cours = False
    intended_dir = None
    return True

# === BOUCLE PRINCIPALE ===
while True:
    screen.fill(WHITE)
    draw_grid()
    draw_inventory(inventory)
    draw_selection_menu()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if choix_en_cours:
                if event.key in (pygame.K_UP, pygame.K_z):
                    index_selection = (index_selection - 1) % len(pieces_proposees)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    index_selection = (index_selection + 1) % len(pieces_proposees)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    place_selected_piece(index_selection)
                elif event.key == pygame.K_ESCAPE:
                    choix_en_cours = False
                    intended_dir = None
                    message_action = "Sélection annulée."
            else:
                if event.key in (pygame.K_z, pygame.K_UP):
                    attempt_open_choice((-1, 0))
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    attempt_open_choice((1, 0))
                elif event.key in (pygame.K_q, pygame.K_LEFT):
                    attempt_open_choice((0, -1))
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    attempt_open_choice((0, 1))

    clock.tick(30)
