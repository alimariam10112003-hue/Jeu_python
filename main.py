import pygame
import numpy as np
import sys
import random
import os
import copy

from joueur import Inventaire, Joueur
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
from objets import *
from aleatoire import GenerateurAlea 


ROWS, COLS = 9, 5

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


# Gestionnaire d'images
menu_background = None
images_cache = {}

def load_all_assets():
    """
    Charge l'image de fond du menu et gère le cache global d'images.

    Cette fonction tente de charger l'image 'jeu.jpg' depuis le dossier 'img/', 
    la met à l'échelle pour correspondre aux dimensions de l'écran (SCREEN_WIDTH, 
    SCREEN_HEIGHT), et la stocke dans la variable globale menu_background.
    Le cache d'images (images_cache) est réinitialisé au début.
    """
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
    """
    Charge une image de tuile de salle à partir du chemin spécifié et la stocke dans un cache.

    Cette fonction gère le chargement de l'image pour un objet Salle (ou son dictionnaire équivalent)
    en vérifiant d'abord si l'image est déjà présente dans le cache global (images_cache) 
    avant de la charger depuis le disque. Elle tente de charger l'image à partir de plusieurs 
    chemins d'accès courants ('images/', 'img/') et convertit la Surface Pygame pour l'affichage.
    
    :param salle: L'objet Salle ou le dictionnaire contenant l'attribut 'image_path'.
    :return: Une surface Pygame chargée (pygame.Surface) si le chargement réussit, sinon None.
    """
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

# Gestionnaire d'objets et de rotations

def salle_to_dict(salle):
    """
    Convertit un objet Salle POO (ou un dictionnaire d'état) en un dictionnaire 
    standardisé pour le stockage dans la grille de jeu.

    Cette fonction assure la cohérence des données en extrayant les attributs de la salle,
    charge l'image correspondante via charger_image_salle, et initialise les clés 
    dynamiques nécessaires à l'affichage et à la rotation (comme 'rotation_angle', 'image_original').

    :param salle: L'objet Salle (instance de classe) ou le dictionnaire à convertir.
                Retourne un dictionnaire d'erreur si la salle est None.
    :return: Un dictionnaire d'état complet de la pièce, prêt pour la grille.
    """
    if salle is None:
        return {
            "nom": "PIECE NULLE",
            "couleur": "rouge",
            "image_path": None,
            "image": None,
            "cout_gem": 99,
            "rarete": 99,
            "porte": {},
            "objets_initiaux": [],
            "effet": "ERREUR: PIECE NULLE",
            "rotation_angle": 0,
            "default_entry_direction": "S",
            "visited": True,
            "image_original": None
        }

    img_chargee = charger_image_salle(salle)

    if isinstance(salle, dict):
        default_entry = salle.get("default_entry_direction", "S")
        nom = salle.get('nom', '???')
        couleur = salle.get('couleur', 'bleue')
        image_path = salle.get('image_path', None)
        cout_gem = salle.get('cout_gem', 0)
        rarete = salle.get('rarete', 0)
        # S'assurer que 'porte' est un dict, même si None est passé
        porte = salle.get('porte', {})
        if porte is None:
            porte = {}
        objets_initiaux = salle.get('objets_initiaux', [])
        effet = salle.get('effet', None)
        visited = salle.get('visited', False)
        
    else:
        default_entry = getattr(salle, "default_entry_direction", "S")
        nom = getattr(salle, 'nom', '???')
        couleur = getattr(salle, 'couleur', 'bleue')
        image_path = getattr(salle, 'image_path', None)
        cout_gem = getattr(salle, 'cout_gem', 0)
        rarete = getattr(salle, 'rarete', 0)
        # S'assurer que 'porte' est un dict, même si None est passé
        porte = getattr(salle, 'porte', {})
        if porte is None:
            porte = {}
        objets_initiaux = list(getattr(salle, 'objets_initiaux', []))
        effet = getattr(salle, 'effet', None)
        visited = getattr(salle, 'visited', False)

    piece_dict = {
        "nom": nom,
        "couleur": couleur,
        "image_path": image_path,
        "image": img_chargee,
        "cout_gem": cout_gem,
        "rarete": rarete,
        "porte": porte,
        "objets_initiaux": objets_initiaux,
        "effet": effet,
        "rotation_angle": 0,
        "default_entry_direction": "S",
        "visited": visited
    }
    
    if piece_dict.get("image"):
        try:
            piece_dict["image_original"] = pygame.transform.smoothscale(piece_dict["image"], (TILE_SIZE, TILE_SIZE))
            if piece_dict.get("rotation_angle", 0) == 0:
                piece_dict["image"] = piece_dict["image_original"]
        except Exception as e:
            print(f"Erreur de scaling image pour {piece_dict['nom']}: {e}")
            piece_dict["image"] = None
            piece_dict["image_original"] = None
            
    return piece_dict


def rotate_piece(piece_dict, angle_deg):
    """
    Applique une rotation à une pièce (dictionnaire d'état) pour aligner ses portes et son image.

    Cette fonction prend en charge deux aspects cruciaux de la rotation:
    1. Logique (Portes): Elle met à jour le dictionnaire 'porte' pour refléter les nouvelles directions 
    des ouvertures suite à la rotation (90, 180, ou 270 degrés).
    2. Visuel (Image): Elle utilise Pygame pour faire pivoter la surface graphique stockée ('image_original') 
    et crée une nouvelle surface pour le rendu.

    :param piece_dict: Le dictionnaire d'état de la pièce à faire pivoter.
    :param angle_deg: L'angle de rotation en degrés (90, 180, ou 270).
    :return: Une copie du dictionnaire de la pièce mise à jour avec la nouvelle orientation des portes et l'image tournée.
    """
    rotated_piece = piece_dict.copy()
    
    portes_originales = piece_dict.get("porte", {})
    if portes_originales is None:
        portes_originales = {}
    
    portes_rotatives = {}
    rotation_map = {}
    
    if angle_deg == 90: 
        rotation_map = {"N": "O", "O": "S", "S": "E", "E": "N"}
    elif angle_deg == 180: 
        rotation_map = {"N": "S", "S": "N", "E": "O", "O": "E"}
    elif angle_deg == 270: 
        rotation_map = {"N": "E", "E": "S", "S": "O", "O": "N"}
    else: 
        rotated_piece["rotation_angle"] = 0
        return rotated_piece 
    
    for old_dir, new_dir in rotation_map.items():
        portes_rotatives[new_dir] = portes_originales.get(old_dir, False)
        
    rotated_piece["porte"] = portes_rotatives
    rotated_piece["rotation_angle"] = angle_deg

    img_original_scaled = rotated_piece.get("image_original")
    
    if img_original_scaled:
        rotated_img = pygame.transform.rotate(img_original_scaled, angle_deg)
        final_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        dest_center = (TILE_SIZE // 2, TILE_SIZE // 2)
        rotated_rect = rotated_img.get_rect(center = dest_center)
        final_surface.blit(rotated_img, rotated_rect)
        rotated_piece["image"] = final_surface
        
    return rotated_piece


def in_bounds(row, col):
    """
    Vérifie si les coordonnées (ligne et colonne) spécifiées se trouvent à l'intérieur 
    des limites définies de la grille du manoir (ROWS x COLS).

    Cette fonction est utilisée pour s'assurer que le joueur ne tente pas de se 
    déplacer en dehors des murs extérieurs de la grille.

    :param row: L'index de la ligne à vérifier.
    :param col: L'index de la colonne à vérifier.
    :return: True si (row, col) est dans la grille, False sinon.
    """
    
    return 0 <= row < ROWS and 0 <= col < COLS

# Etat du jeu (Variables Globales)
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
    """
    Réinitialise complètement l'état du jeu pour commencer une nouvelle partie.

    Cette fonction effectue les étapes cruciales suivantes :
    1. Réinitialise la position du joueur (player_pos) au point de départ (bas, centre).
    2. Crée une nouvelle grille (grid) et initialise les objets POO (Inventaire, GenerateurAlea).
    3. Place les pièces fixes : l'EntranceHall (salle de départ) et l'Antichambre (salle d'arrivée).
    4. Reconstruit le catalogue_pieces complet en utilisant les fonctions creer_salles_...
    5. Réinitialise toutes les variables d'état (choix_en_cours, menu_active, game_over, game_won) 
    pour préparer le jeu à la boucle principale.
    """
    global player_pos, grid, inventaire, catalogue_pieces, message_action, choix_en_cours
    global index_selection, pieces_proposees, intended_dir, menu_active, game_over, game_won
    global selected_move_direction, just_cancelled_selection, generateur_alea
    
    player_pos = [ROWS - 1, COLS // 2]
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    
    inventaire = Inventaire() 
    generateur_alea = GenerateurAlea() 

    # PLACEMENT DE L'ENTRANCE HALL (Bas Centre)
    salle_depart_obj = EntranceHall()
    grid[player_pos[0]][player_pos[1]] = salle_to_dict(salle_depart_obj)

    # AJOUT CRITIQUE : PLACEMENT DE L'ANTICHAMBRE (Haut Centre)
    salle_fin_obj = Antechamber()
    grid[0][COLS // 2] = salle_to_dict(salle_fin_obj) 
    

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

# Logique du jeu

def process_room_entry(room_dict):
    """
    Déclenche l'interaction immédiate avec une salle lors de la première entrée du joueur.

    Cette fonction exécute les étapes suivantes :
    1. Marque la salle comme 'visited' (visitée) pour éviter de redéclencher les effets initiaux.
    2. Parcourt la liste 'objets_initiaux' de la salle, mettant à jour l'inventaire 
    (gain de clés, gemmes, pièces d'or, pas, objets permanents) en fonction du type d'objet.
    3. Analyse la chaîne de caractères 'effet' de la salle (si présente) pour appliquer 
    des modifications de ressources spécifiques (ex: perte de pas, gain aléatoire).
    4. Met à jour la variable globale 'message_action' avec un résumé des gains/pertes 
    et vérifie l'état de victoire si l'effet 'Victoire' est détecté.

    :param room_dict: Le dictionnaire d'état de la salle que le joueur vient d'entrer.
    """
    
    global inventaire, message_action, game_won
    
    if room_dict is None:
        return
        
    if room_dict.get("visited", False):
        message_action = f"Vous entrez dans : {room_dict.get('nom', '???')}"
        return
    
    room_dict["visited"] = True 
    
    objets_a_retirer = []
    objets_gagnes = []
    message_effet = ""

    if "objets_initiaux" in room_dict:
        for item_name in room_dict["objets_initiaux"]:
            if item_name == "Key":
                inventaire.gagner_cle(1)
                objets_gagnes.append("1 Clé")
            elif item_name == "Gem":
                inventaire.gagner_gemme(1)
                objets_gagnes.append("1 Gemme")
            elif item_name == "Coin":
                inventaire.gagner_coin(1)
                objets_gagnes.append("1 Pièce")
            elif item_name == "Dé":
                inventaire.des += 1 
                objets_gagnes.append("1 Dé")
                
            elif item_name in NOURRITURE_VALEURS:
                pas = NOURRITURE_VALEURS[item_name]
                inventaire.gagner_pas(pas)
                objets_gagnes.append(f"{item_name} (+{pas} pas)")
            elif item_name == "Random Food":
                nourriture = creer_objet_aleatoire_nourriture()
                inventaire.gagner_pas(nourriture.pas_rendus)
                objets_gagnes.append(f"{nourriture.nom} (+{nourriture.pas_rendus} pas)")

            elif item_name in PERMANENT_VALEURS:
                if item_name == "Pelle": inventaire.possede_pelle = True
                elif item_name == "Marteau": inventaire.possede_marteau = True
                elif item_name == "Kit de Crochetage": inventaire.possede_kit_crochetage = True
                elif item_name == "Détecteur de Métaux": inventaire.possede_detecteur_metaux = True
                elif item_name == "Patte de Lapin": inventaire.possede_patte_lapin = True
                
                objets_gagnes.append(f"Objet: {item_name}")
                
            elif " Coins" in item_name:
                try:
                    quantite = int(item_name.split(" ")[0])
                    inventaire.gagner_coin(quantite)
                    objets_gagnes.append(f"{quantite} Pièces")
                except:
                    pass 
        
    # S'assurer que 'effet' est une chaîne vide par défaut, jamais None
    effet = room_dict.get("effet")
    if effet is None:
        effet = ""

    if "Perte de" in effet:
        try:
            parties = effet.split(" ")
            quantite = int(parties[2])
            if "pas" in effet:
                inventaire.depenser_pas(quantite)
                message_effet = f"Vous perdez {quantite} pas !"
            elif "coin" in effet:
                inventaire.retirer_coin(quantite)
                message_effet = f"Vous perdez {quantite} pièce(s) !"
            elif "Gem" in effet:
                inventaire.retirer_gemme(quantite)
                message_effet = f"Vous perdez {quantite} gemme(s) !"
        except Exception as e:
            print(f"Erreur d'analyse de l'effet: {e}")
            
    elif "Gagne aléatoirement 1 à 5 pas" in effet: 
        pas_gagnes = random.randint(1, 5)
        inventaire.gagner_pas(pas_gagnes)
        message_effet = f"Vous gagnez {pas_gagnes} pas."
    
    elif "Victoire" in effet:
        message_effet = "Vous avez trouvé l'Antichambre !"
        game_won = True
        pygame.event.clear(pygame.KEYDOWN)
    
    if objets_gagnes:
        message_action = "Vous trouvez: " + ", ".join(objets_gagnes)
        if message_effet:
            message_action += "\n" + message_effet
    elif message_effet:
        message_action = message_effet


# Dessin
def draw_start_screen():
    """
    Dessine l'écran d'accueil (menu principal) du jeu.

    Cette fonction est responsable de :
    1. Afficher l'image de fond du menu (menu_background) ou un fond Blueprint de secours.
    2. Afficher le titre du jeu.
    3. Dessiner le bouton 'JOUER' et appliquer un effet visuel (hover effect) basé sur la position de la souris.
    4. Retourner l'objet pygame.Rect du bouton 'JOUER' pour permettre la détection des clics dans la boucle principale.

    :return: L'objet pygame.Rect correspondant au bouton 'JOUER'.
    """
    global play_button_rect, menu_background

    if menu_background:
        screen.blit(menu_background, (0, 0))
    else:
        screen.fill(BLUEPRINT_BG)
        step = 60
        for x in range(0, SCREEN_WIDTH, step):
            pygame.draw.line(screen, BLUEPRINT_GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, step):
            pygame.draw.line(screen, BLUEPRINT_GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)

    
    title_surf = font_title.render("BLUE PRINCE", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title_surf, ((SCREEN_WIDTH - title_surf.get_width()) // 2, SCREEN_HEIGHT // 4))

    button_w, button_h = 360, 100
    bx = (SCREEN_WIDTH - button_w) // 2
    by = SCREEN_HEIGHT // 2
    play_button_rect = pygame.Rect(bx, by, button_w, button_h)

    mx, my = pygame.mouse.get_pos()
    if play_button_rect and play_button_rect.collidepoint((mx, my)):
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
    """
    Dessine l'état actuel de la grille du manoir sur l'écran Pygame.

    Cette fonction itère sur la grille (ROWS x COLS) et est responsable de :
    1. Dessiner le fond (BLUEPRINT_BG) et les bordures de la grille (BLUEPRINT_GRID_COLOR).
    2. Afficher chaque tuile (TILE_SIZE) : soit l'image de la pièce découverte, soit un fond sombre 
    (DARK_GRAY) si la pièce est inconnue.
    3. Afficher un fond coloré ou le nom de la pièce si l'image n'est pas disponible.
    4. Mettre en évidence la position actuelle du joueur (player_pos) avec un contour rouge (RED).
    5. Afficher un indicateur de sélection de mouvement (YELLOW_CURSOR) si l'utilisateur a choisi une direction.
    """
    screen.fill(BLUEPRINT_BG, pygame.Rect(0, 0, WIDTH, SCREEN_HEIGHT))
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            piece = grid[row][col]
            if piece:
                image = piece.get("image")
                if image:
                    try:
                        screen.blit(image, (x, y))
                    except Exception as e:
                        print(f"[ERROR] Impossible de blitter la pièce '{piece.get('nom', '???')}': {e}")
                        pygame.draw.rect(screen, PIECE_COLORS.get(piece.get("couleur", "bleue"), GRAY), rect)
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
    
    r, c = player_pos
    pygame.draw.rect(screen, RED, pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 4)

    if selected_move_direction and not choix_en_cours:
        r, c = player_pos
        dr, dc = selected_move_direction
        tr, tc = r + dr, c + dc
        if in_bounds(tr, tc):
            target_rect = pygame.Rect(tc * TILE_SIZE, tr * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill(YELLOW_CURSOR) 
            screen.blit(s, target_rect.topleft)


def draw_inventory(inv):
    """
    Dessine la zone d'inventaire complète, incluant les ressources, les objets permanents
    et les boutons d'action AIDE et QUITTER.

    Cette fonction est responsable de :
    1. Effacer et dessiner le fond de la zone d'inventaire (style Blueprint).
    2. Afficher la liste des ressources consommables (Pas, Gemmes, Clés, Dés, Pièces d'or)
    en utilisant les attributs de l'objet Inventaire (inv).
    3. Afficher les objets permanents possédés (Pelle, Crochetage, etc.).
    4. Dessiner le message d'action actuel (message_action).
    5. Calculer et dessiner les rectangles cliquables des boutons AIDE et QUITTER, 
    en mettant à jour leurs variables globales associées (exit_button_rect, help_button_rect).
    
    :param inv: L'instance de la classe Inventaire contenant l'état des ressources du joueur.
    :return: None.
    """
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
        ("Pas", "🚶", inv.pas), ("Gemmes", "💎", inv.gem),
        ("Clés", "🔑", inv.cles), ("Dés", "🎲", inv.des),
        ("Pièces d'or", "🪙", inv.coin)
    ]

    max_width = INVENTORY_WIDTH - 20
    for name, icon, value in resources:
        name_text = font.render(name, True, BLUEPRINT_TEXT_COLOR)
        try:
            val_icon_text = font_emoji.render(f"{value} {icon}", True, BLUEPRINT_TEXT_COLOR)
        except:
            # Fallback si le rendu emoji échoue
            val_icon_text = font.render(f"{value}", True, BLUEPRINT_TEXT_COLOR)
            
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
        ("Pelle", inv.possede_pelle), ("Marteau", inv.possede_marteau),
        ("Crochetage", inv.possede_kit_crochetage), ("Détecteur", inv.possede_detecteur_metaux),
        ("Patte de lapin", inv.possede_patte_lapin)
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
    """
    Dessine le menu de sélection de salle lorsque le joueur tente d'ouvrir une nouvelle porte.

    Cette fonction est responsable de :
    1. Afficher l'indication de la direction du mouvement visé (N, S, O, E).
    2. Afficher jusqu'à trois options de pièces (pieces_proposees) tirées au sort.
    3. Rendre les informations de chaque pièce, incluant le nom, la couleur, le niveau de rareté,
    et le coût en gemmes.
    4. Mettre en évidence (avec un contour rouge) la pièce actuellement sélectionnée par l'utilisateur.
    """
    if not choix_en_cours:
        return
    dir_text = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}.get(intended_dir, "Direction")
    x_base = WIDTH + 20; y_start = 500
    title = font.render(f"Choix ({dir_text})", True, BLUEPRINT_TEXT_COLOR)
    screen.blit(title, (x_base, y_start - 40))
    
    if not pieces_proposees:
        return 

    for i, piece in enumerate(pieces_proposees):
        y = y_start + i * 130
        
        piece_dict = salle_to_dict(piece)
        nom = piece_dict.get("nom", "???")
        cout_gem = piece_dict.get("cout_gem", 0)
        rarete = piece_dict.get("rarete", 0)
        couleur = piece_dict.get("couleur", "bleue")
        
        rect = pygame.Rect(x_base, y, INVENTORY_WIDTH - 40, 120)
        bg_color = (255, 200, 200) if i == index_selection else (40, 40, 70)
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, RED if i == index_selection else BLUEPRINT_GRID_COLOR, rect, 3)
        
        image = piece_dict.get("image_original") 
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

def draw_end_screen(titre, couleur):
    """
    Dessine un écran de fin de partie (Victoire ou Défaite) par-dessus l'état actuel du jeu.

    Cette fonction crée un calque semi-transparent qui recouvre tout l'écran 
    et affiche un message central, ainsi que les instructions pour rejouer ou quitter.

    :param titre: La chaîne de caractères à afficher comme titre (ex: "VICTOIRE !", "DÉFAITE").
    :param couleur: La couleur du titre (couleur) (ex: RED pour la défaite, GREEN pour la victoire).
    :return: None.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    titre_surf = font_game_over.render(titre, True, couleur)
    titre_rect = titre_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(titre_surf, titre_rect)
    
    inst_surf = font_title.render("Appuyez sur ENTREE pour rejouer", True, WHITE)
    inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(inst_surf, inst_rect)
    
    inst_surf_2 = font_title.render("Appuyez sur ÉCHAP pour quitter", True, WHITE)
    inst_rect_2 = inst_surf_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(inst_surf_2, inst_rect_2)

def draw_game_over_screen():
    """
    Déclenche l'affichage de l'écran de Défaite (Game Over).

    Cette fonction appelle draw_end_screen() avec le titre "DÉFAITE" et la couleur rouge (RED).
    Elle gère l'état de fin de partie lorsque le joueur a épuisé ses Pas ou est bloqué.
    """
    draw_end_screen("DÉFAITE", RED)

def draw_win_screen():
    """
    Déclenche l'affichage de l'écran de Victoire.

    Cette fonction appelle draw_end_screen() avec le titre "VICTOIRE !" et une couleur verte/claire
    pour signaler la réussite de l'objectif (atteinte de l'Antichambre).
    """
    draw_end_screen("VICTOIRE !", (100, 255, 100))

# Nouvelle fonction pour cerifier le blocage
def check_for_blockade(current_r, current_c, inventaire, catalogue_pieces):
    """
    Vérifie si le joueur est complètement bloqué (ne peut plus se déplacer ou poser de nouvelle pièce).
    Le joueur est bloqué si, à partir de sa position actuelle, il ne peut atteindre aucune
    nouvelle salle ou salle existante car :
    1. Tous les chemins mènent à un mur (interne ou externe).
    2. Toutes les portes vers des cases non découvertes nécessitent une clé (Niveau 1 ou 2)
    et le joueur n'a pas les ressources nécessaires (clés ou Kit de crochetage).

    :param current_r: La ligne actuelle du joueur.
    :param current_c: La colonne actuelle du joueur.
    :param inventaire: L'objet Inventaire contenant les ressources du joueur.
    :param catalogue_pieces: La liste des pièces restantes dans la pioche.
    :return: True si le joueur est bloqué, False s'il existe au moins un chemin déverrouillé.
    """
    direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
    
    can_place_new_room = len(catalogue_pieces) > 0
    
    # Vérifier toutes les 4 directions
    for direction, dir_key in direction_map.items():
        dy, dx = direction
        target_r, target_c = current_r + dy, current_c + dx
        
        # Vérification des limites et des murs internes (salle actuelle)
        if not in_bounds(target_r, target_c):
            continue 
            
        current_room = grid[current_r][current_c]
        if current_room and current_room.get("porte", {}).get(dir_key) is not True:
            continue 
            
        target_room = grid[target_r][target_c]
        
        if target_room is not None:
            # Possibilité de mouvement vers une salle existante: non bloqué
            return False 
        
        else:
            # Tentative de PLACER une nouvelle salle
            if not can_place_new_room:
                continue 
                
            # Déterminer le niveau de verrouillage de la porte vers la cible
            niveau_verrouillage = generateur_alea.tirer_niveau_verrouillage(target_r)
            
            if niveau_verrouillage == 0:
                # Niveau 0: Toujours possible de placer
                return False 
            elif niveau_verrouillage == 1:
                # Niveau 1: Possible avec Clé ou Kit
                if inventaire.cles > 0 or inventaire.possede_kit_crochetage:
                    return False
            elif niveau_verrouillage == 2:
                # Niveau 2: Possible seulement avec Clé
                if inventaire.cles > 0:
                    return False
    
    # Si aucune issue trouvée, le joueur est bloqué.
    return True 

# Logique du jeu principale

def handle_move(direction):
    """
    Gère la tentative de déplacement du joueur dans une direction donnée (Haut, Bas, Gauche, Droite).

    Cette fonction orchestre le flux de jeu en exécutant les vérifications suivantes :
    1. Vérification de la défaite immédiate (Pas épuisés ou joueur bloqué).
    2. Vérification des Murs (limites externes et portes internes manquantes).
    3. Consommation du Pas (déduit au début de l'action, remboursé en cas d'échec d'ouverture de porte).
    4. CAS SALLE EXISTANTE : Déplace le joueur et déclenche les effets d'entrée de salle (process_room_entry).
    5. CAS NOUVELLE PORTE : Détermine le niveau de verrouillage (0, 1, ou 2) via GenerateurAlea, vérifie les ressources
    (clés/Kit de Crochetage), consomme les ressources si l'ouverture est réussie, et lance le menu de tirage de pièces.

    :param direction: Tuple (dy, dx) représentant la direction du mouvement.
    :return: True si l'action aboutit (déplacement ou lancement du tirage), False en cas de blocage ou défaite.
    """
    global choix_en_cours, pieces_proposees, index_selection, intended_dir, message_action, inventaire, player_pos, grid, game_over, generateur_alea
    dy, dx = direction
    current_r, current_c = player_pos
    target_r, target_c = current_r + dy, current_c + dx
    
    direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
    dir_key = direction_map.get(direction)
    
    if inventaire.pas <= 0:
        message_action = "💀 Défaite : vous n'avez plus de pas!"
        game_over = True 
        return False
    
    if not in_bounds(target_r, target_c):
        message_action = "Mur extérieur : Limite du manoir atteinte."
        # Vérification si cette tentative de mouvement non-valide aurait dû révéler un blocage complet
        if check_for_blockade(current_r, current_c, inventaire, catalogue_pieces):
            message_action = "💀 Défaite : Vous êtes complètement bloqué. Plus de chemins disponibles ou manquants de ressources clés/pièces."
            game_over = True
        return False
        
    current_room = grid[current_r][current_c]
    if current_room and current_room.get("porte", {}).get(dir_key) is not True:
        message_action = f"Mur interne : La salle '{current_room['nom']}' n'a pas de porte vers {dir_key}."
        # Vérification si cette tentative de mouvement non-valide aurait dû révéler un blocage complet
        if check_for_blockade(current_r, current_c, inventaire, catalogue_pieces):
            message_action = "💀 Défaite : Vous êtes complètement bloqué. Plus de chemins disponibles ou manquants de ressources clés/pièces."
            game_over = True
        return False
        
    target_room = grid[target_r][target_c]
    
    # Dépenser le pas (sera remboursé en cas d'échec de l'ouverture de porte)
    inventaire.depenser_pas(1)
    if inventaire.pas <= 0:
        message_action = "💀 Défaite : vous n'avez plus de pas!"
        game_over = True 
        pygame.event.clear(pygame.KEYDOWN)
        return False 

    if target_room is not None:
        # Déplacement vers une salle existante (Mouvement réussi)
        player_pos[0], player_pos[1] = target_r, target_c
        message_action = f"Déplacement vers {target_room['nom']} ({inventaire.pas} pas restants)."
        process_room_entry(target_room)
        
        # Vérification de verouillage (Après l'entrée dans une pièce)
        r, c = player_pos
        if check_for_blockade(r, c, inventaire, catalogue_pieces):
            message_action = "💀 Défaite : Vous êtes complètement bloqué. Plus de chemins disponibles ou manquants de ressources clés/pièces."
            game_over = True
            return False
        
        return True
    else:
        # Ouverture d'une nouvelle porte (vérification de verrouillage)

        # Déterminer le niveau de verouillage (Logique fixe par rangée)
        niveau_verrouillage = generateur_alea.tirer_niveau_verrouillage(target_r)

        cle_utilisee = False
        kit_crochetage_utilise = False
        
        if niveau_verrouillage == 0:
            message_action = "Porte déverrouillée (Niveau 0). Vous pouvez continuer."
            pass
        elif niveau_verrouillage == 1:
            # Porte verrouillée simple (Niveau 1)
            if inventaire.possede_kit_crochetage: 
                kit_crochetage_utilise = True
                message_action = "Porte verrouillée simple (Niveau 1).\nKit de Crochetage utilisé pour l'ouvrir!."
            elif inventaire.cles > 0:
                inventaire.retirer_cle(1)
                cle_utilisee = True
                message_action = "Porte verrouillée simple (Niveau 1).\n🔑 Clé dépensée pour l'ouvrir!."
            else:
                # Échec de l'ouverture
                message_action = "Porte verrouillée simple (Niveau 1)! Nécessite 🔑 ou Kit de Crochetage."
                inventaire.gagner_pas(1) # Rembourser le pas
                
                # Verification de blocage apres erreur
                if check_for_blockade(current_r, current_c, inventaire, catalogue_pieces):
                    message_action = "💀 Défaite : Vous êtes bloqué. Plus de chemins disponibles ou manquants de ressources clés/pièces."
                    game_over = True
                return False
                
        elif niveau_verrouillage == 2:
            # Porte verrouillée à double tour (Niveau 2)
            if inventaire.cles > 0:
                inventaire.retirer_cle(1)
                cle_utilisee = True
                message_action = "Porte verrouillée double tour (Niveau 2).\n🔑 Clé dépensée pour l'ouvrir!."
            else:
                # Échec de l'ouverture
                message_action = "Porte verrouillée double tour (Niveau 2)! Nécessite 🔑."
                inventaire.gagner_pas(1) # Rembourser le pas
                
                # Verification de blocage
                if check_for_blockade(current_r, current_c, inventaire, catalogue_pieces):
                    message_action = "💀 Défaite : Vous êtes bloqué. Plus de chemins disponibles ou manquants de ressources clés/pièces."
                    game_over = True
                return False
        
        # La porte est ouverte => tirage de pièce

        if not catalogue_pieces:
            message_action += "\nImpasse... La pioche est vide."
            inventaire.gagner_pas(1) # Rembourser le pas
            game_over = True
            return False
            
        pieces_proposees.clear()
        
        # Determiner la direction cible
        dir_cible = direction_map.get(direction)
        
        # TIRER LES PIÈCES (via la méthode de l'instance GenerateurAlea)
        pieces_proposees.extend(generateur_alea.tirer_pieces(catalogue_pieces, n=3, dir_cible=dir_cible))
        
        if not pieces_proposees:
            message_action += "\nImpasse... La pioche est vide."
            inventaire.gagner_pas(1) # Rembourser le pas
            game_over = True
            return False
            
        index_selection = 0
        choix_en_cours = True
        intended_dir = direction
        
        # Le message final de sélection est affiché après le message d'ouverture de porte
        message_action += "\nSélectionnez une nouvelle pièce." 
        return True

def place_selected_piece(idx):
    """
    Exécute le placement définitif de la pièce choisie par le joueur dans le manoir.

    Cette fonction est appelée après qu'une pièce ait été sélectionnée dans le menu de tirage et est responsable de :
    1. Vérifier si le joueur possède suffisamment de gemmes pour couvrir le coût (cout_gem). En cas d'échec, le pas consommé pour l'ouverture de la porte est remboursé.
    2. Retirer la pièce sélectionnée du catalogue global (pioche).
    3. Calculer l'angle de rotation dynamique nécessaire pour que la porte d'entrée de la nouvelle pièce s'aligne avec la porte de la salle précédente.
    4. Confirmer que la pièce, une fois tournée, possède bien une porte active pour la connexion. Si non, l'action est annulée et le pas est remboursé.
    5. Placer le dictionnaire d'état de la pièce (piece_dict) dans la grille.
    6. Déduire le coût en gemmes, mettre à jour la position du joueur (player_pos), et déclencher les effets d'entrée de la salle (process_room_entry).

    :param idx: L'index de la pièce sélectionnée dans la liste temporaire pieces_proposees.
    :return: True si le placement est réussi et le jeu continue, False en cas d'erreur ou d'annulation.
    """
    global choix_en_cours, intended_dir, message_action, inventaire, catalogue_pieces, player_pos, grid
    
    if not pieces_proposees or idx >= len(pieces_proposees):
        message_action = "Erreur: Sélection invalide."
        choix_en_cours = False
        return False
        
    piece = pieces_proposees[idx]
    
    if piece in catalogue_pieces:
        try:
            catalogue_pieces.remove(piece)
        except ValueError:
            pass 
        
    dy, dx = intended_dir
    target_r = player_pos[0] + dy
    target_c = player_pos[1] + dx
    
    piece_info = salle_to_dict(piece)
    cout_gem = piece_info.get("cout_gem", 0)
    nom = piece_info.get("nom", "???")
    
    if cout_gem > inventaire.gem:
        message_action = "Pas assez de gemmes! (Pas remboursé)"
        inventaire.gagner_pas(1) 
        choix_en_cours = False
        intended_dir = None
        return False
    
    piece_dict = piece_info

    direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
    opposite_map = {"N": "S", "S": "N", "E": "O", "O": "E"}
    
    dir_actuelle = direction_map.get(intended_dir) 
    target_connection = opposite_map.get(dir_actuelle)
    
    default_entry = piece_dict.get("default_entry_direction", "S") 

    angle = 0
    
    rotation_from_N = {"N": 0, "S": 180, "E": 270, "O": 90}
    rotation_from_S = {"N": 180, "S": 0, "E": 90, "O": 270}
    rotation_from_E = {"N": 90, "S": 270, "E": 0, "O": 180}
    rotation_from_O = {"N": 270, "S": 90, "E": 180, "O": 0}
    
    if default_entry == "N":
        angle = rotation_from_N.get(target_connection, 0)
    elif default_entry == "S":
        angle = rotation_from_S.get(target_connection, 0)
    elif default_entry == "E":
        angle = rotation_from_E.get(target_connection, 0)
    elif default_entry == "O":
        angle = rotation_from_O.get(target_connection, 0)

    piece_dict = rotate_piece(piece_dict, angle)
    
    if piece_dict.get("porte", {}).get(target_connection) is not True:
        message_action = f"Erreur de connexion : La pièce '{nom}' n'a pas de porte pour cette entrée."
        inventaire.gagner_pas(1) 
        choix_en_cours = False
        intended_dir = None
        return False
    
    if in_bounds(target_r, target_c) and grid[target_r][target_c] is None:
        grid[target_r][target_c] = piece_dict
        player_pos[0], player_pos[1] = target_r, target_c
        inventaire.retirer_gemme(cout_gem)
        
        process_room_entry(piece_dict)
    else:
        message_action = "Erreur logique: La pièce n'a pas pu être placée à cet endroit."
        inventaire.gagner_pas(1) 
    
    choix_en_cours = False
    intended_dir = None
    return True

# Boucle principale
load_all_assets()
reset_game() 

while True:
    events = pygame.event.get()
    
    if just_cancelled_selection:
        just_cancelled_selection = False
        events_filtres = []
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                continue 
            events_filtres.append(event)
        events = events_filtres

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if menu_active:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect and play_button_rect.collidepoint(event.pos):
                    menu_active = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_active = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
        
        elif game_over or game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    reset_game() 
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        else: # Si le jeu est en cours
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()
                if help_button_rect.collidepoint(mouse_pos):
                    choix_en_cours = False
                    message_action = "AIDE: Déplacez-vous avec ZQSD ou les flèches.\nTrouvez l'Antichambre pour gagner."
            if event.type == pygame.KEYDOWN:
                if choix_en_cours:
                    if event.key in (pygame.K_UP, pygame.K_z):
                        index_selection = (index_selection - 1) % max(1, len(pieces_proposees))
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        index_selection = (index_selection + 1) % max(1, len(pieces_proposees))
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if pieces_proposees:
                            place_selected_piece(index_selection)
                    
                    # Logique: utilisation des clés (Touche R)
                    elif event.key == pygame.K_r: 
                        if inventaire.des > 0:
                            inventaire.des -= 1
                            pieces_proposees.clear() # Vider l'ancienne liste
                            
                            # Déterminer la direction cible pour maintenir le boost NORD
                            direction_map = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}
                            dir_cible = direction_map.get(intended_dir)

                            # Relancer le tirage via l'instance GenerateurAlea
                            pieces_proposees.extend(generateur_alea.tirer_pieces(catalogue_pieces, n=3, dir_cible=dir_cible))
                            index_selection = 0
                            message_action = f"Dé utilisé! Nouveau tirage de pièces ({inventaire.des} dés restants)."
                        else:
                            message_action = "Vous n'avez pas de dés pour relancer le tirage."
                    
        
                    
                    elif event.key == pygame.K_ESCAPE:
                        choix_en_cours = False; intended_dir = None; message_action = "Sélection annulée."
                        just_cancelled_selection = True # Déclenche le verrou
                else:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                        

                    if event.key in (pygame.K_z, pygame.K_UP):
                        selected_move_direction = (-1, 0)
                        message_action = "Direction HAUT sélectionnée. Appuyez sur Espace."
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        selected_move_direction = (1, 0)
                        message_action = "Direction BAS sélectionnée. Appuyez sur Espace."
                    elif event.key in (pygame.K_q, pygame.K_LEFT):
                        selected_move_direction = (0, -1)
                        message_action = "Direction GAUCHE sélectionnée. Appuyez sur Espace."
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        selected_move_direction = (0, 1)
                        message_action = "Direction DROITE sélectionnée. Appuyez sur Espace."
                        
                    elif event.key == pygame.K_SPACE:
                        if selected_move_direction:
                            handle_move(selected_move_direction)
                            selected_move_direction = None 
                        else:
                            message_action = "Veuillez d'abord choisir une direction (ZQSD)."

    # Logique d'affichage (basée sur l'état)
    if menu_active:
        play_button_rect = draw_start_screen()
    
    elif game_over:
        screen.fill(BLUEPRINT_BG)
        draw_grid()
        draw_inventory(inventaire)
        draw_game_over_screen()
        
    elif game_won:
        screen.fill(BLUEPRINT_BG)
        draw_grid()
        draw_inventory(inventaire)
        draw_win_screen()
        
        
    else: # Le jeu est en cours
        screen.fill(BLUEPRINT_BG)
        draw_grid()
        draw_inventory(inventaire)
        draw_selection_menu()

    pygame.display.flip()
    clock.tick(30)