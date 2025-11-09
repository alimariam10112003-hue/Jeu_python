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
font = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 22)
font_title = pygame.font.SysFont(None, 36)

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

# === ETAT DU JEU ===
player_pos = [ROWS - 1, COLS // 2]
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Créer le catalogue complet de pièces
catalogue_pieces_original = []
catalogue_pieces_original.extend(creer_salles_bleues())
catalogue_pieces_original.extend(creer_salles_verte())
catalogue_pieces_original.extend(creer_salles_viollette())
catalogue_pieces_original.extend(creer_salles_orange())
catalogue_pieces_original.extend(creer_salles_jaune())
catalogue_pieces_original.extend(creer_salles_rouge())

# Catalogue actif (on retire les pièces utilisées de celui-ci)
catalogue_pieces = catalogue_pieces_original.copy()

# La pièce de départ doit être créée séparément si elle est spéciale
grid[player_pos[0]][player_pos[1]] = {
    "nom": "Entrance Hall", 
    "couleur": "bleue",
    "image": charger_image("entrance_hall.png")
}

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

# === UTILITAIRES ===
def charger_image_salle(salle):
    """Charge l'image d'une salle (avec cache)"""
    if hasattr(salle, 'image_path'):
        image_path = salle.image_path
    else:
        # Si c'est un dictionnaire
        image_path = salle.get('image_path', f"img/{salle['nom'].lower().replace(' ', '_')}.png")
    
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
    """
    Renvoie n copies de pièces choisies aléatoirement selon leur rareté.
    """
    pieces_disponibles = []
    for piece in catalogue:
        # Accès à rarete selon le type (objet ou dict)
        rarete = piece.rarete if hasattr(piece, 'rarete') else piece.get("rarete", 0)
        poids = 1 / (3 ** rarete)
        pieces_disponibles.append((piece, poids))

    tirage = random.choices(
        [p[0] for p in pieces_disponibles],
        weights=[p[1] for p in pieces_disponibles],
        k=n
    )

    # garantir au moins une pièce gratuite (gemmes == 0)
    has_free = False
    for p in tirage:
        cout = p.cout_gem if hasattr(p, 'cout_gem') else p.get("gemmes", 0)
        if cout == 0:
            has_free = True
            break
    
    if not has_free:
        free_pieces = [p for p in catalogue if (p.cout_gem if hasattr(p, 'cout_gem') else p.get("gemmes", 0)) == 0]
        if free_pieces:
            tirage[random.randint(0, n - 1)] = random.choice(free_pieces)

    return tirage

def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# === DESSIN ===
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            piece = grid[row][col]
            if piece:
                # Case découverte avec image ou couleur
                image = piece.get("image") or charger_image_salle(piece)
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
    """Affiche l'inventaire avec mise en page améliorée comme dans l'image 2"""
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
    """Menu de sélection des pièces centré verticalement"""
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
def attempt_open_choice(direction):
    global choix_en_cours, pieces_proposees, index_selection, intended_dir, message_action
    dy, dx = direction
    target_r = player_pos[0] + dy
    target_c = player_pos[1] + dx
    
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
    global choix_en_cours, intended_dir, message_action, inventory
    piece = pieces_proposees[idx]
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