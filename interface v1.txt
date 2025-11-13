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

# === CONFIGURATION DE BASE ===
ROWS, COLS = 9, 5 # taille du manoir (lignes, colonnes)

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

# constantes couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
BLACK = (0, 0, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (50, 50, 50)  # Pour les cases non découvertes

PIECE_COLORS = {
    "bleue": (100, 100, 255),
    "verte": (100, 200, 100),
    "violette": (180, 100, 180),
    "orange": (255, 165, 0),
    "rouge": (255, 100, 100),
    "jaune": (255, 255, 100),
}

# Crée la fenêtre avec bordures
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Interface")
clock = pygame.time.Clock()
font_path = os.path.join("fonts", "NotoColorEmoji.ttf")
font = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 22)
font_title = pygame.font.SysFont(None, 36)

# === CHARGEMENT DES IMAGES ===
def charger_image(nom_fichier):
    chemin = os.path.join("images", nom_fichier)
    if os.path.exists(chemin):
        try:
            # Correction potentielle: Ajout de .convert_alpha() si les images ont de la transparence
            return pygame.image.load(chemin).convert_alpha()
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
# === CACHE D'IMAGES ===
images_cache = {}

# === UTILITAIRES DE SALLE (Déplacé pour résoudre la NameError) ===

def charger_image_salle(salle):
    """Charge l'image d'une salle (avec cache)"""
    global images_cache
    
    if hasattr(salle, 'image_path'):
        image_path = salle.image_path
    else:
        # Si c'est un dictionnaire
        image_path = salle.get('image_path', f"img/{salle['nom'].lower().replace(' ', '_')}.png")
    
    if image_path in images_cache:
        return images_cache[image_path]
    
    if os.path.exists(image_path):
        try:
            img = pygame.image.load(image_path).convert_alpha()
            images_cache[image_path] = img
            return img
        except Exception:
            return None
    return None

def salle_to_dict(salle):
    """Convertit un objet Salle en dictionnaire pour la grille"""
    if isinstance(salle, dict):
        return salle
    
    # Correction: On s'assure que la clé 'image' est valorisée après que les images_cache sont définies
    # Cependant, pour le moment on laisse la logique telle quelle, elle sera appelée par l'initialisation.
    return {
        "nom": salle.nom,
        "couleur": salle.couleur,
        "image_path": salle.image_path,
        "cout_gem": salle.cout_gem,
        "rarete": salle.rarete,
        "porte": salle.porte,
        "objets_initiaux": salle.objets_initiaux,
        "effet": salle.effet,
        "image": charger_image_salle(salle) # Utilisation de la fonction définie ci-dessus
    }

def get_rotation_angle_for_placement(target_r, target_c):
    """
    Détermine l'angle de rotation nécessaire pour orienter le mur (la face sans porte)
    d'une pièce sur le bord du manoir.
    """
    if target_r == 0: # Rangée du haut (N) -> la pièce doit généralement faire face au SUD (porte N devient S)
        return 180 
    if target_r == ROWS - 1: # Rangée du bas (S) -> la pièce doit généralement faire face au NORD
        return 0 # Pas de rotation nécessaire (ou 0 degrés)
    if target_c == 0: # Colonne de gauche (O) -> la pièce doit généralement faire face à l'EST (porte O devient E)
        return 90
    if target_c == COLS - 1: # Colonne de droite (E) -> la pièce doit généralement faire face à l'OUEST (porte E devient O)
        return 270
    
    return 0

def rotate_piece(piece_dict, angle_deg):
    """
    Fait pivoter la logique de porte de la pièce et son image.
    angle_deg doit être 90, 180, ou 270.
    """
    rotated_piece = piece_dict.copy()

    # 1. Rotation de la Logique de Porte
    portes_originales = piece_dict.get("porte", {})
    portes_rotatives = {}
    
    rotation_map = {}
    if angle_deg == 90:
        rotation_map = {"N": "E", "E": "S", "S": "O", "O": "N"}
    elif angle_deg == 180:
        rotation_map = {"N": "S", "E": "O", "S": "N", "O": "E"}
    elif angle_deg == 270:
        rotation_map = {"N": "O", "O": "S", "S": "E", "E": "N"}
    else:
        return piece_dict 

    for old_dir, new_dir in rotation_map.items():
        portes_rotatives[new_dir] = portes_originales.get(old_dir, False)

    rotated_piece["porte"] = portes_rotatives

    # 2. Rotation de l'Image (si elle existe)
    image_originale = piece_dict.get("image")
    if image_originale:
        rotated_piece["image"] = pygame.transform.rotate(image_originale, angle_deg)

    return rotated_piece

def tirer_pieces(catalogue, n=3):
    """
    Renvoie n copies de pièces choisies aléatoirement selon leur rareté (np.choice)
    et garantit qu'au moins une pièce est gratuite (coût_gem = 0).
    """
    pieces_list = []
    poids_list = []
    pieces_gratuites = []

    for piece in catalogue:
        if hasattr(piece, 'rarete'):
            rarete = piece.rarete
            cout_gem = piece.cout_gem
        else:
            rarete = piece.get("rarete", 0)
            cout_gem = piece.get("cout_gem", 0) 
            
        poids = 1.0 / (3 ** rarete)
        
        pieces_list.append(piece)
        poids_list.append(poids)
        
        if cout_gem == 0:
            pieces_gratuites.append(piece)

    if not pieces_list:
        return []

    tirage = np.random.choice(
        pieces_list,
        size=n,
        p=np.array(poids_list) / sum(poids_list),
        replace=False if len(pieces_list) >= n and n>0 else True
    ).tolist()

    # --- Garantie de Pièce Gratuite ---
    if pieces_gratuites and not any(p.cout_gem == 0 for p in tirage if hasattr(p, 'cout_gem')):
        index_a_remplacer = random.randint(0, n - 1)
        tirage[index_a_remplacer] = random.choice(pieces_gratuites)

    return tirage

def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


# === ETAT DU JEU ===
player_pos = [ROWS - 1, COLS // 2]
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# 1. Initialisation CORRECTE et UNIQUE de l'Entrance Hall
salle_depart_obj = EntranceHall() 
grid[player_pos[0]][player_pos[1]] = salle_to_dict(salle_depart_obj) # <-- CORRECT

# Créer le catalogue complet de pièces (Inchangé)
catalogue_pieces = []
catalogue_pieces.extend(creer_salles_bleues())
catalogue_pieces.extend(creer_salles_verte())
catalogue_pieces.extend(creer_salles_viollette())
catalogue_pieces.extend(creer_salles_orange())
catalogue_pieces.extend(creer_salles_jaune())
catalogue_pieces.extend(creer_salles_rouge())

# 2. Suppression de la Ligne Erronée qui écrasait l'attribut 'porte' (Était ici)

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

# message d'action affiché en bas
message_action = ""

# menu / sélection
choix_en_cours = False
index_selection = 0
pieces_proposees = []
intended_dir = None

# Dictionnaire pour stocker les images déjà chargées (pour éviter de recharger)
images_cache = {}


# === DESSIN ===
def draw_grid():
    # ... (code inchangé) ...
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            piece = grid[row][col]
            if piece:
                # Case découverte avec image ou couleur
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
                # Case non découverte = fond noir
                pygame.draw.rect(screen, BLACK, rect)
            
            # Bordure grise pour toutes les cases
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

            # Curseur rouge sur la position du joueur
            if [row, col] == player_pos:
                pygame.draw.rect(screen, RED, rect, 4)

def draw_inventory(inv):
    # ... (code inchangé) ...
    x_start = WIDTH + 20
    y = 20
    
    # Fond blanc pour la zone inventaire
    screen.fill(WHITE, pygame.Rect(WIDTH, 0, INVENTORY_WIDTH, SCREEN_HEIGHT))
    
    # Titre "Inventory:"
    title = font_title.render("Inventory:", True, BLACK)
    screen.blit(title, (x_start, y))
    y += 50
    
    # Ressources avec icônes alignées à droite
    resources = [
        ("Pas", "🚶", inv.get("Pas", 0)),
        ("Gemmes", "💎", inv.get("Gemmes", 0)),
        ("Clés", "🔑", inv.get("Clés", 0)),
        ("Dés", "🎲", inv.get("Dés", 0)),
        ("Pièces d'or", "🪙", inv.get("Pièces d'or", 0))
    ]
    
    max_width = INVENTORY_WIDTH - 100
    for name, icon, value in resources:
        # Valeur à droite
        val_text = font.render(str(value), True, BLACK)
        val_x = x_start + max_width - val_text.get_width()
        screen.blit(val_text, (val_x, y))
        
        # Icône juste à gauche de la valeur
        icon_text = font.render(icon, True, BLACK)
        icon_x = val_x - icon_text.get_width() - 10
        screen.blit(icon_text, (icon_x, y))
        
        y += 35
    
    y += 20
    
    # Objets permanents
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
    
    # Afficher le nom de la pièce actuelle en gros
    y += 40
    current_room = grid[player_pos[0]][player_pos[1]]
    if current_room:
        room_title = font_title.render(current_room["nom"], True, BLACK)
        screen.blit(room_title, (x_start, y))
        y += 50
    
    # Message d'action en bas
    if message_action:
        y = SCREEN_HEIGHT - 80
        msg_lines = message_action.split('\n')
        for line in msg_lines:
            msg_text = font_small.render(line, True, BLACK)
            screen.blit(msg_text, (x_start, y))
            y += 25

def draw_selection_menu():
    # ... (code inchangé) ...
    if not choix_en_cours:
        return

    # Titre avec direction
    dir_text = {
        (-1, 0): "Vers le HAUT",
        (1, 0): "Vers le BAS",
        (0, -1): "Vers la GAUCHE",
        (0, 1): "Vers la DROITE"
    }.get(intended_dir, "Direction")

    x_base = WIDTH + 20
    y_start = 150
    
    title = font.render(f"Choix ({dir_text})", True, BLACK)
    screen.blit(title, (x_base, y_start - 40))

    for i, piece in enumerate(pieces_proposees):
        y = y_start + i * 130
        
        # Extraire les infos de la pièce (objet Salle ou dict)
        nom = piece.nom if hasattr(piece, 'nom') else piece.get("nom", "???")
        cout_gem = piece.cout_gem if hasattr(piece, 'cout_gem') else piece.get("gemmes", 0)
        rarete = piece.rarete if hasattr(piece, 'rarete') else piece.get("rarete", 0)
        couleur = piece.couleur if hasattr(piece, 'couleur') else piece.get("couleur", "bleue")
        
        # Rectangle de fond
        rect = pygame.Rect(x_base, y, INVENTORY_WIDTH - 40, 120)
        if i == index_selection:
            pygame.draw.rect(screen, (255, 200, 200), rect)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, rect)
        
        pygame.draw.rect(screen, RED if i == index_selection else BLACK, rect, 3)

        # Image de la pièce à gauche
        image = charger_image_salle(piece)
        if image:
            img_scaled = pygame.transform.scale(image, (100, 100))
            screen.blit(img_scaled, (x_base + 10, y + 10))
        else:
            # Rectangle coloré si pas d'image
            color_rect = pygame.Rect(x_base + 10, y + 10, 100, 100)
            color = PIECE_COLORS.get(couleur, GRAY)
            pygame.draw.rect(screen, color, color_rect)

        # Texte à droite de l'image
        text_x = x_base + 120
        nom_text = font.render(nom, True, BLACK)
        screen.blit(nom_text, (text_x, y + 15))
        
        gemmes_text = f"{cout_gem} gemmes" if cout_gem > 0 else "Gratuit"
        gemmes = font_small.render(gemmes_text, True, BLACK)
        screen.blit(gemmes, (text_x, y + 50))
        
        rarete_text = font_small.render(f"Rareté: {rarete}", True, BLACK)
        screen.blit(rarete_text, (text_x, y + 75))


# === LOGIQUE ===
def handle_move(direction):
    global choix_en_cours, pieces_proposees, index_selection, intended_dir, message_action, inventory
    dy, dx = direction
    current_r, current_c = player_pos
    target_r, target_c = current_r + dy, current_c + dx
    
    direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
    dir_key = direction_map.get(direction) # Clé directionnelle (N, S, O, E)

    # 1. Vérification des Pas (Défaite)
    if inventory["Pas"] <= 0:
        message_action = "💀 Défaite : vous n'avez plus de pas!"
        return False

    # 2. Vérification des limites de la grille (Mur extérieur)
    if not in_bounds(target_r, target_c):
        message_action = "Mur extérieur : Limite du manoir atteinte."
        return False
    
    current_room = grid[current_r][current_c]
    
    # 3. Vérification de la Porte dans la Salle Actuelle (Mur intérieur)
    
    # Si la pièce n'a pas l'attribut 'porte' ou si la porte n'est pas True
    if current_room and current_room.get("porte", {}).get(dir_key) is not True:
        message_action = f"Mur interne : La salle '{current_room['nom']}' n'a pas de porte vers {dir_key}."
        return False
    
    # --- Si on arrive ici, il y a bien une porte, et la destination est dans la grille. ---
    
    target_room = grid[target_r][target_c]
    
    if target_room is not None:
        # CAS A : Déplacement vers une salle DÉCOUVERTE (Déplacement simple)
        
        # Consommation de 1 pas
        inventory["Pas"] -= 1
        player_pos[0], player_pos[1] = target_r, target_c
        message_action = f"Déplacement vers {target_room['nom']} ({inventory['Pas']} pas restants)."
        return True
        
    else:
        # CAS B : Ouverture de Nouvelle Porte (Lancement du Tirage)
        
        # Consommation de 1 pas (pour le mouvement qui suit le choix de la pièce)
        inventory["Pas"] -= 1
        
        # TODO: C'est ici que la logique de PORTE VERROUILLÉE doit être insérée.
        
        pieces_proposees.clear()
        pieces_proposees.extend(tirer_pieces(catalogue_pieces, n=3))
        index_selection = 0
        choix_en_cours = True
        intended_dir = direction
        message_action = "Sélectionnez une nouvelle pièce."
        return True

def place_selected_piece(idx):
    global choix_en_cours, intended_dir, message_action, inventory, catalogue_pieces
    piece = pieces_proposees[idx]
    
    # --- MODIFICATION: Retirer la pièce du catalogue (Pioche) doit être fait ici ---
    # Nous devons retirer l'OBJET Salle de la liste catalogue_pieces, pas le dict.
    if piece in catalogue_pieces:
        catalogue_pieces.remove(piece)
    # -----------------------------------------------------------------------------

    dy, dx = intended_dir
    target_r = player_pos[0] + dy
    target_c = player_pos[1] + dx

    # Extraire le coût en gemmes
    cout_gem = piece.cout_gem if hasattr(piece, 'cout_gem') else piece.get("gemmes", 0)
    nom = piece.nom if hasattr(piece, 'nom') else piece.get("nom", "???")

    # Vérifier les gemmes
    if cout_gem > inventory["Gemmes"]:
        message_action = "Pas assez de gemmes!"
        return False

    # Convertir la salle en dictionnaire pour la grille
    piece_dict = salle_to_dict(piece)
    # Determiner l'angle de rotation pour le placement sur les bords
    angle = get_rotation_angle_for_placement(target_r, target_c)
    # Appliquer la rotation
    if angle != 0:
        piece_dict = rotate_piece(piece_dict, angle)

    if in_bounds(target_r, target_c) and grid[target_r][target_c] is None:
        grid[target_r][target_c] = piece_dict
        player_pos[0], player_pos[1] = target_r, target_c
        inventory["Gemmes"] -= cout_gem
        # Les Pas ont déjà été consommés dans handle_move pour ouvrir la porte
        message_action = f"Vous entrez dans {nom}."
    else:
        # Cette partie est incorrecte car la pièce n'est jamais placée sur la position du joueur
        message_action = "Erreur logique: La pièce n'a pas été placée."

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
                    handle_move((-1, 0))
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    handle_move((1, 0))
                elif event.key in (pygame.K_q, pygame.K_LEFT):
                    handle_move((0, -1))
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    handle_move((0, 1))

    clock.tick(30)