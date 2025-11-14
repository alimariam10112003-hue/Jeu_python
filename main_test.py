import pygame
import numpy as np
import sys
import random
import os
import copy
import math

# --- 1. IMPORTATIONS DES CLASSES DE LOGIQUE ---
from manoir import Manoir 
from joueur import Joueur
from aleatoire import GenerateurAlea 
from salle import Salle 
from salles_speciales import EntranceHall, Antechamber
from catalogue_salle import (
    creer_salles_bleues, creer_salles_verte, creer_salles_viollette,
    creer_salles_orange, creer_salles_jaune, creer_salles_rouge
)


# === UTILITAIRES DE SALLE (Migrés de l'ancien code) ===

# Note: Ces utilitaires sont intégrés ici pour l'UI, mais la logique principale de jeu
# devrait idéalement utiliser les méthodes des objets Salle dans manoir.py

images_cache = {}

def charger_image(nom_fichier):
    chemin = os.path.join("images", nom_fichier)
    if os.path.exists(chemin):
        try:
            return pygame.image.load(chemin).convert_alpha()
        except Exception:
            return None
    return None

def charger_image_salle(salle):
    """Charge l'image d'une salle (avec cache)"""
    global images_cache
    
    # Gère l'accès à image_path que ce soit un objet Salle ou un dict
    if hasattr(salle, 'image_path'):
        image_path = salle.image_path
    else:
        # Si c'est un dictionnaire, utiliser le chemin si disponible
        image_path = salle.get('image_path', f"img/{salle['nom'].lower().replace(' ', '_')}.png")
    
    if image_path in images_cache:
        return images_cache[image_path]
    
    # ... (logique de chargement et de cache simplifiée) ...
    if os.path.exists(image_path):
        try:
            img = pygame.image.load(image_path).convert_alpha()
            images_cache[image_path] = img
            return img
        except Exception:
            return None
    return None

def salle_to_dict(salle):
    """Convertit un objet Salle en dictionnaire pour la grille de dessin"""
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

def get_rotation_angle_for_placement(target_r, target_c):
    """
    Détermine l'angle de rotation pour l'alignement sur les bords (ROWS=9, COLS=5)
    Note: Cette logique est normalement gérée par manoir.py/Salle, mais est gardée ici 
    en utilitaire si manoir.py ne la gère pas encore.
    """
    if target_r == 0: return 180 
    if target_r == Manoir.LIGNES - 1: return 0 
    if target_c == 0: return 90
    if target_c == Manoir.COLONNES - 1: return 270
    return 0

def rotate_piece(piece_dict, angle_deg):
    """
    Fait pivoter la logique de porte de la pièce et son image.
    """
    rotated_piece = piece_dict.copy()
    
    # Logique de rotation des attributs 'porte' et 'image' (récupérée de votre code)
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

    image_originale = piece_dict.get("image")
    if image_originale:
        rotated_piece["image"] = pygame.transform.rotate(image_originale, angle_deg)
        
    return rotated_piece


# --- 2. CLASSE JEU (Le Contrôleur Principal/Interface) ---

class Jeu:
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_GAME_OVER = 2 

    def __init__(self):
        pygame.init()
        
        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h
        self.ROWS, self.COLS = Manoir.LIGNES, Manoir.COLONNES
        
        # Ajustement de la taille de la tuile pour que la grille rentre
        self.TILE_SIZE = (self.SCREEN_HEIGHT - 10) // self.ROWS # -10 pour une petite marge
        self.WIDTH = self.TILE_SIZE * self.COLS
        self.INVENTORY_WIDTH = self.SCREEN_WIDTH - self.WIDTH
        self.SCREEN_HEIGHT = self.TILE_SIZE * self.ROWS # Ajuste la hauteur finale

        # COULEURS (Style Blueprint)
        self.BLUEPRINT_BACKGROUND = (30, 30, 90) 
        self.BLUEPRINT_GRID_COLOR = (120, 120, 255)
        self.BLUEPRINT_TEXT_COLOR = (120, 120, 255)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 100, 100)
        self.GREEN_HELP = (50, 150, 50) 
        self.PIECE_COLORS = { 
            "bleue": (100, 100, 255), "verte": (100, 200, 100), "violette": (180, 100, 180),
            "orange": (255, 165, 0), "rouge": (255, 100, 100), "jaune": (255, 255, 100),
        }
        
        # Le mode FULLSCREEN est potentiellement la cause de l'absence des boutons système
        # Je retire FULLSCREEN et laisse Pygame gérer la fenêtre standard
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) 
        pygame.display.set_caption("🏰 Projet MANOIR - Blue Prince POO 🔑")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 22)
        self.font_title = pygame.font.SysFont(None, 36)
        self.font_button = pygame.font.SysFont(None, 60, bold=True)
        # Assurez-vous d'avoir une police pour les emojis si vous en utilisez
        self.font_emoji = pygame.font.SysFont(None, 30) 

        # Logique de jeu (Initialisation des classes POO)
        self.generateur = GenerateurAlea()
        self.joueur = Joueur()
        self.manoir = Manoir(self.joueur, self.generateur)
        
        # État UI
        self.game_state = self.STATE_MENU 
        self.menu_background_image = None
        self._load_menu_assets()
        self.choix_en_cours = False
        self.index_selection = 0
        self.pieces_proposees = [] # List d'objets Salle retournés par manoir.tirer_pieces_au_sort
        self.intended_dir_tuple = None # (dy, dx)
        self.message_action = "Bienvenue, Prince! Dirigez-vous vers l'Antichambre 👑."
        self.images_cache = {} # Initialisé en haut
        self.game_over = False
        self.exit_button_rect = None
        self.aide_ouverte = False
        self.play_button_rect = None # Sera défini par draw_menu
        self.cont_button_rect = None
        self.help_button_rect = None


    def _load_menu_assets(self):
        chemin_image = os.path.join("img", "jeu.jpg")
        if os.path.exists(chemin_image):
            self.menu_background_image = pygame.image.load(chemin_image).convert_alpha()
            self.menu_background_image = pygame.transform.scale(self.menu_background_image, 
                                                                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        else:
            self.menu_background_image = None 

    def charger_image(self, nom_fichier):
        # Utilise la logique de mise en cache pour le dessin de l'UI
        # Cette méthode est redondante avec charger_image_salle mais est gardée pour le style du binome
        if nom_fichier not in self.images_cache:
            base_name = os.path.basename(nom_fichier) 
            chemin = os.path.join("img", base_name)
            
            if os.path.exists(chemin):
                try: 
                    self.images_cache[base_name] = pygame.image.load(chemin).convert_alpha()
                except Exception: 
                    self.images_cache[base_name] = None
            else:
                self.images_cache[base_name] = None
        return self.images_cache.get(os.path.basename(nom_fichier))
    
    def draw_grid(self):
        # ... (Logique UI du binôme : Dessine la grille et les pièces) ...
        self.screen.fill(self.BLUEPRINT_BACKGROUND, pygame.Rect(0, 0, self.WIDTH, self.SCREEN_HEIGHT))

        for row in range(self.ROWS):
            for col in range(self.COLS):
                x, y = col * self.TILE_SIZE, row * self.TILE_SIZE
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                
                # --- ACCÈS À L'OBJET SALLE DU MANOIR ---
                piece = self.manoir.grille[row][col]

                if piece:
                    # Utiliser l'image de la pièce après la rotation dans place_selected_piece
                    # Note: La rotation doit être appliquée AVANT le dessin.
                    image = self.charger_image(piece.image_path) 
                    
                    if image:
                        # Assurer la rotation si la pièce a été tournée
                        angle = get_rotation_angle_for_placement(row, col)
                        if angle != 0:
                            image = pygame.transform.rotate(image, angle)
                            
                        image_scaled = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
                        self.screen.blit(image_scaled, (x, y))
                    else:
                        color = self.PIECE_COLORS.get(piece.couleur, self.WHITE)
                        pygame.draw.rect(self.screen, color, rect)
                        text = self.font_small.render(piece.nom, True, self.WHITE)
                        self.screen.blit(text, (x + 5, y + 5))
                else:
                    pygame.draw.rect(self.screen, self.BLUEPRINT_BACKGROUND, rect)
                
                pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, rect, 1)

                if (row, col) == self.joueur.position:
                    pygame.draw.rect(self.screen, self.RED, rect, 4)

        grid_rect_full = pygame.Rect(0, 0, self.WIDTH, self.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, grid_rect_full, 5) 
        
        global_rect = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, self.WHITE, global_rect, 5)

    def draw_inventory(self):
        # ... (Logique UI du binôme : Dessine l'inventaire) ...
        inv = self.joueur.inventaire
        x_start = self.WIDTH + 20
        y = 20
        
        self.screen.fill(self.BLUEPRINT_BACKGROUND, pygame.Rect(self.WIDTH, 0, self.INVENTORY_WIDTH, self.SCREEN_HEIGHT))
        
        # ... (Bouton AIDE) ...
        help_text = self.font_small.render("AIDE", True, self.WHITE)
        help_button_width = help_text.get_width() + 15
        
        self.help_button_rect = pygame.Rect(self.WIDTH + self.INVENTORY_WIDTH - help_button_width - 15, 25, help_button_width, 30)
        
        pygame.draw.rect(self.screen, self.GREEN_HELP, self.help_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, self.help_button_rect, 1, border_radius=5)
        self.screen.blit(help_text, (self.help_button_rect.x + 5, self.help_button_rect.y + 5))
        # --- FIN BOUTON AIDE ---

        # 1. ZONE INVENTAIRE (Ressources + Objets Permanents)
        inv_rect = pygame.Rect(self.WIDTH + 10, 10, self.INVENTORY_WIDTH - 20, 200)
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, inv_rect, 2)
        
        title = self.font_title.render("INVENTAIRE", True, self.BLUEPRINT_TEXT_COLOR)
        self.screen.blit(title, (x_start, y)); y += 50
        
        # --- DONNÉES INVENTAIRE UTILISANT LES ATTRIBUTS DE self.joueur ---
        resources = [
            ("Pas", "🚶", inv.pas), ("Gemmes", "💎", inv.gem), ("Clés", "🔑", inv.cles),
            ("Dés", "🎲", inv.des), ("Pièces d'or", "🪙", inv.coin)
        ]
        
        for name, icon, value in resources:
            name_text = self.font.render(name, True, self.BLUEPRINT_TEXT_COLOR)
            # Utilise font_emoji si disponible
            val_icon_text = self.font.render(f"{value} {icon}", True, self.BLUEPRINT_TEXT_COLOR) 
            
            self.screen.blit(name_text, (x_start, y))
            val_icon_x = self.WIDTH + self.INVENTORY_WIDTH - 20 - val_icon_text.get_width()
            self.screen.blit(val_icon_text, (val_icon_x, y))
            y += 35
        
        y += 20
        
        # ZONE PERMANENT ITEMS
        permanent_items = [
            ("Pelle", inv.possede_pelle), ("Marteau", inv.possede_marteau), 
            ("Crochetage", inv.possede_kit_crochetage), ("Détecteur", inv.possede_detecteur_metaux), 
            ("Patte de lapin", inv.possede_patte_lapin)
        ]
        
        title_perm = self.font_small.render("OBJETS PERMANENTS:", True, self.BLUEPRINT_TEXT_COLOR)
        self.screen.blit(title_perm, (x_start, y)); y += 30
        
        perm_rect = pygame.Rect(self.WIDTH + 10, y - 5, self.INVENTORY_WIDTH - 20, 150)
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, perm_rect, 2)
        
        for name, possede in permanent_items:
            if possede:
                text = self.font_small.render(name.upper(), True, self.BLUEPRINT_TEXT_COLOR)
                self.screen.blit(text, (x_start + 10, y)); y += 25

        # 3. Message d'action (Reste inchangé)
        if self.message_action:
            y_msg = self.SCREEN_HEIGHT - 80
            msg_rect = pygame.Rect(self.WIDTH + 10, y_msg - 5, self.INVENTORY_WIDTH - 20, 70)
            pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, msg_rect, 2)
            
            for line in self.message_action.split('\n'):
                msg_text = self.font_small.render(line, True, self.BLUEPRINT_TEXT_COLOR)
                self.screen.blit(msg_text, (x_start, y_msg)); y_msg += 25
        
        # 4. BOUTON QUITTER (Reste inchangé)
        button_x = self.WIDTH + self.INVENTORY_WIDTH - 120
        button_y = self.SCREEN_HEIGHT - 60
        button_width = 100
        button_height = 40
        
        self.exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        pygame.draw.rect(self.screen, self.RED, self.exit_button_rect, border_radius=5)
        
        exit_text = self.font_small.render("QUITTER", True, self.WHITE)
        text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, text_rect)

    def draw_selection_menu(self):
        # ... (Logique UI du binôme : Dessine le menu de sélection) ...
        if not self.choix_en_cours: return

        x_base = self.WIDTH + 20
        y_start = 150
        
        dir_text = {(-1, 0): "HAUT", (1, 0): "BAS", (0, -1): "GAUCHE", (0, 1): "DROITE"}.get(self.intended_dir_tuple, "")
        title = self.font.render(f"CHOIX VERS {dir_text}", True, self.BLUEPRINT_TEXT_COLOR)
        self.screen.blit(title, (x_base, y_start - 40))

        for i, piece in enumerate(self.pieces_proposees):
            y = y_start + i * 130
            
            nom = piece.nom
            cout_gem = piece.cout_gem
            rarete = piece.rarete
            
            rect = pygame.Rect(x_base, y, self.INVENTORY_WIDTH - 40, 120)
            
            pygame.draw.rect(self.screen, self.BLUEPRINT_BACKGROUND, rect)
            pygame.draw.rect(self.screen, self.RED if i == self.index_selection else self.BLUEPRINT_GRID_COLOR, rect, 3)
            
            text_x = x_base + 120
            self.screen.blit(self.font.render(nom, True, self.BLUEPRINT_TEXT_COLOR), (text_x, y + 15))
            
            gemmes_text = f"💎 {cout_gem} gemmes" if cout_gem > 0 else "Gratuit"
            self.screen.blit(self.font_small.render(gemmes_text, True, self.BLUEPRINT_TEXT_COLOR), (text_x, y + 50))
            
            rarete_text = self.font_small.render(f"Rareté: {rarete}", True, self.BLUEPRINT_TEXT_COLOR)
            self.screen.blit(rarete_text, (text_x, y + 75))
            
            image = self.charger_image(piece.image_path)
            if image:
                img_scaled = pygame.transform.scale(image, (100, 100))
                self.screen.blit(img_scaled, (x_base + 10, y + 10))

    def draw_menu(self):
        # ... (Logique UI du binôme : Dessine le menu) ...
        if self.menu_background_image:
            self.screen.blit(self.menu_background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        button_text = self.font_button.render("JOUER", True, self.WHITE)
        button_rect = button_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, button_rect.inflate(40, 20), border_radius=15)
        pygame.draw.rect(self.screen, self.BLUEPRINT_BACKGROUND, button_rect.inflate(40, 20), 5, border_radius=15)
        
        self.screen.blit(button_text, button_rect)
        return button_rect 
        
    def draw_rules(self):
        # ... (Logique UI du binôme : Dessine les règles) ...
        # NOTE: self.cont_button_rect est défini ici par le dessin
        rect_width = 700 
        rect_height = 780
        rect_x = (self.SCREEN_WIDTH - rect_width) // 2
        rect_y = (self.SCREEN_HEIGHT - rect_height) // 2
        
        surface = pygame.Surface((rect_width, rect_height))
        surface.set_alpha(240)
        surface.fill(self.BLUEPRINT_BACKGROUND)
        self.screen.blit(surface, (rect_x, rect_y))
        
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, (rect_x, rect_y, rect_width, rect_height), 5)

        # Contenu des règles (Reste inchangé)
        x_start = rect_x + 50
        y = rect_y + 120
        
        title = self.font_title.render("RÈGLES DU JEU", True, self.BLUEPRINT_GRID_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.SCREEN_WIDTH // 2, rect_y + 40)))
        
        self.screen.blit(self.font.render("RÈGLES", True, self.BLUEPRINT_GRID_COLOR), (x_start, y)); y += 30
        self.screen.blit(self.font.render("OBJECTIF : Atteindre l'Antichambre.", True, self.WHITE), (x_start, y)); y += 35
        self.screen.blit(self.font.render("DÉPLACEMENT : Coûte 1 Pas par salle. (Défaite si Pas = 0).", True, self.WHITE), (x_start, y)); y += 35
        self.screen.blit(self.font.render("PORTES : Certaines nécessitent une Clé ou Kit de Crochetage.", True, self.WHITE), (x_start, y)); y += 35
        self.screen.blit(self.font.render("TIRAGE : Choix 1 salle parmis 3 .", True, self.WHITE), (x_start, y)); y += 35
        self.screen.blit(self.font.render("COÛT : Salles rares nécessitent des Gemmes .", True, self.WHITE), (x_start, y)); y += 60
        
        self.screen.blit(self.font_title.render("CONTRÔLES", True, self.BLUEPRINT_GRID_COLOR), (x_start, y)); y += 40

        def draw_key_line(name, key_char, y_pos):
            key_width = 30; key_height = 30
            key_x = x_start + 450
            self.screen.blit(self.font.render(name, True, self.WHITE), (x_start, y_pos))
            key_rect = pygame.Rect(key_x, y_pos, key_width, key_height)
            pygame.draw.rect(self.screen, self.RED, key_rect, border_radius=5)
            key_text = self.font_small.render(key_char, True, self.WHITE)
            self.screen.blit(key_text, key_text.get_rect(center=key_rect.center))
            return y_pos + 45 

        y = draw_key_line("AVANCER / HAUT", "Z", y)
        y = draw_key_line("RECULER / BAS", "S", y)
        y = draw_key_line("GAUCHE", "Q", y)
        y = draw_key_line("DROITE", "D", y)

        y += 15
        self.screen.blit(self.font.render("VALIDER SÉLECTION", True, self.WHITE), (x_start, y))
        
        cont_text = self.font_button.render("FERMER", True, self.WHITE)
        cont_rect = cont_text.get_rect(center=(self.SCREEN_WIDTH // 2, rect_y + rect_height - 60))
        pygame.draw.rect(self.screen, self.BLUEPRINT_GRID_COLOR, cont_rect.inflate(30, 15), border_radius=10)
        self.screen.blit(cont_text, cont_rect)
        
        return cont_rect
    
    # --- LOGIQUE DE JEU MIGRÉE DE handle_move (Interface 1) ---

    def handle_move(self, direction_tuple):
        if self.game_over or self.aide_ouverte: return
        if self.choix_en_cours: return
        
        direction_key = {(-1, 0): "N", (1, 0): "S", (0, -1): "O", (0, 1): "E"}.get(direction_tuple)

        # L'appel à manoir.deplacer_joueur gère TOUTE la logique
        # Le retour est: (list_de_pieces | True | False | None, message)
        resultat, message = self.manoir.deplacer_joueur(direction_key)
        
        if isinstance(resultat, list):
            # CAS TIRAGE DE PIÈCES
            self.pieces_proposees = resultat
            self.choix_en_cours = True
            self.intended_dir_tuple = direction_tuple
            self.index_selection = 0
            self.message_action = message
            
        elif resultat is True:
            # CAS DÉPLACEMENT RÉUSSI (y compris Victoire)
            self.message_action = message
            if "Victoire!" in message: self.game_state = self.STATE_GAME_OVER
            
        elif resultat is False:
            # CAS MOUVEMENT BLOQUÉ (Mur, Pas épuisés, Clé manquante)
            self.message_action = message
            if "Pas épuisés" in message: self.game_state = self.STATE_GAME_OVER
            
        elif resultat is None:
            # CAS PORTE VERROUILLÉE (Ouverture tentée mais échec)
            self.message_action = message

    def place_selected_piece(self, idx):
        piece_choisie = self.pieces_proposees[idx]
        
        cout_gem = piece_choisie.cout_gem
        
        # 1. Vérification des gemmes (Pas géré dans manoir.py, on le garde ici)
        if cout_gem > self.joueur.inventaire.gem:
            self.message_action = "❌ Pas assez de gemmes pour cette pièce! 💎"
            # Annuler la sélection, mais on doit rembourser le pas consommé dans handle_move
            self.joueur.inventaire.gagner_pas(1) # Remboursement
            self.choix_en_cours = False
            self.intended_dir_tuple = None
            return False

        # 2. Déduction des gemmes
        self.joueur.inventaire.retirer_gemme(cout_gem) 
        
        dy, dx = self.intended_dir_tuple
        pos_cible = (self.joueur.position[0] + dy, self.joueur.position[1] + dx)
        
        # 3. Placement final (combine rotation, placement, et déplacement du joueur)
        
        # --- A. ROTATION ---
        angle = get_rotation_angle_for_placement(pos_cible[0], pos_cible[1])
        if angle != 0:
            # Créer un dictionnaire pour la rotation de l'image (si on ne modifie pas l'objet Salle)
            # Puisqu'on ne fait que le dessin, nous allons modifier l'objet Salle pour le dessin
            # (Note: Dans un design POO strict, on ne modifierait pas l'objet Salle ici).
            pass
            
        # --- B. PLACEMENT DANS MANOIR ---
        self.manoir.placer_salle(piece_choisie, pos_cible)
        self.manoir._creer_portes_salle(pos_cible, piece_choisie) 
        
        # 4. Mettre à jour la position du joueur (Le pas a été consommé dans handle_move)
        self.joueur.position = pos_cible
        
        # 5. Déclencher les effets (interagir)
        # Note: La méthode interagir n'est pas fournie, mais elle sera appelée ici
        # piece_choisie.interagir(self.joueur) 

        self.choix_en_cours = False
        self.intended_dir_tuple = None
        self.message_action = f"Vous avez placé {piece_choisie.nom}. {self.joueur.inventaire.pas} pas restants. 🚶"
        return True

    def run(self):
        # ... (Logique de la boucle principale avec gestion des états) ...
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # GESTION DU BOUTON QUITTER
                    if self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                # GESTION DES ÉVÉNEMENTS DU MENU
                if self.game_state == self.STATE_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.play_button_rect and self.play_button_rect.collidepoint(event.pos):
                            self.game_state = self.STATE_GAME
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_state = self.STATE_GAME

                # GESTION DES ÉVÉNEMENTS DE JEU
                elif self.game_state == self.STATE_GAME:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # GESTION DU BOUTON AIDE
                        if self.aide_ouverte:
                            if self.cont_button_rect and self.cont_button_rect.collidepoint(event.pos):
                                self.aide_ouverte = False
                        elif self.help_button_rect and self.help_button_rect.collidepoint(event.pos):
                             self.aide_ouverte = True

                    if event.type == pygame.KEYDOWN:
                        if self.game_state == self.STATE_GAME_OVER:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit(); sys.exit()
                            continue
                        
                        if event.key == pygame.K_h:
                            self.aide_ouverte = not self.aide_ouverte
                        if self.aide_ouverte: continue 
                            
                        if self.choix_en_cours:
                            # Remboursement du pas si annulation
                            if event.key == pygame.K_ESCAPE:
                                self.joueur.inventaire.gagner_pas(1) # Remboursement du pas consommé dans handle_move
                                self.choix_en_cours = False
                                self.intended_dir_tuple = None
                                self.message_action = "Sélection annulée. (Pas remboursé)."
                            
                            if event.key in (pygame.K_UP, pygame.K_z):
                                self.index_selection = (self.index_selection - 1) % len(self.pieces_proposees)
                            elif event.key in (pygame.K_DOWN, pygame.K_s):
                                self.index_selection = (self.index_selection + 1) % len(self.pieces_proposees)
                            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                self.place_selected_piece(self.index_selection)
                        else:
                            if event.key in (pygame.K_z, pygame.K_UP): self.handle_move((-1, 0))
                            elif event.key in (pygame.K_s, pygame.K_DOWN): self.handle_move((1, 0))
                            elif event.key in (pygame.K_q, pygame.K_LEFT): self.handle_move((0, -1))
                            elif event.key in (pygame.K_d, pygame.K_RIGHT): self.handle_move((0, 1))

            # --- Logique de Dessin ---
            self.screen.fill(self.BLUEPRINT_BACKGROUND)
            if self.game_state == self.STATE_MENU:
                self.play_button_rect = self.draw_menu()
            elif self.game_state == self.STATE_GAME or self.game_state == self.STATE_GAME_OVER:
                self.draw_grid()
                self.draw_inventory()
                self.draw_selection_menu()
                
                if self.aide_ouverte:
                    self.cont_button_rect = self.draw_rules()

            # L'état GAME_OVER est dessiné dans la boucle de jeu après l'appel à draw_inventory
            if self.game_state == self.STATE_GAME_OVER:
                self.screen.fill((50, 0, 0))
                game_over_text = self.font_title.render("FIN DE PARTIE!", True, self.RED)
                self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50)))
                reason_text = self.font.render(self.message_action, True, self.WHITE)
                self.screen.blit(reason_text, reason_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)))
                escape_text = self.font_small.render("Appuyez sur ECHAP pour quitter", True, self.BLUEPRINT_TEXT_COLOR)
                self.screen.blit(escape_text, escape_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100)))

            pygame.display.flip()
            self.clock.tick(30)


# --- 3. POINT D'ENTRÉE ---

if __name__ == "__main__":
    jeu_instance = Jeu()
    jeu_instance.run()