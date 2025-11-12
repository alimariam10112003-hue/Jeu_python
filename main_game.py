import pygame
import sys
from random import choice
from joueur import Joueur, Inventaire
from salle import Salle
from catalogue_salle import (
    EntranceHall, Antechamber,
    creer_salles_bleues, 
    creer_salles_verte,
    creer_salles_viollette, 
    creer_salles_orange,
    creer_salles_jaune, 
    creer_salles_rouge
)

# --- Constantes Pygame ---
TAILLE_GRILLE = (5, 9)
TAILLE_SALLE = 80  # plus petite taille
COTE_GRILLE_X = TAILLE_GRILLE[0] * TAILLE_SALLE
COTE_GRILLE_Y = TAILLE_GRILLE[1] * TAILLE_SALLE
TAILLE_FENETRE = (COTE_GRILLE_X + 500, COTE_GRILLE_Y + 100)
COULEUR_FOND = (20, 20, 30)
COULEUR_VIDE = (50, 50, 50)
COULEUR_LIGNE = (80, 80, 80)
EPAISSEUR_LIGNE = 2


# --- Classe Manoir ---
class Manoir:
    def __init__(self):
        self.grille = [[None for _ in range(TAILLE_GRILLE[0])] for _ in range(TAILLE_GRILLE[1])]
        # Position départ : au milieu de la ligne du bas
        self.joueur = Joueur(position_depart=(TAILLE_GRILLE[1] - 1, TAILLE_GRILLE[0] // 2))
        self.pos_y, self.pos_x = self.joueur.position

        # Crée la salle d’entrée
        entrance_hall = EntranceHall()
        self.placer_salle(entrance_hall, self.pos_y, self.pos_x)
        self.pioche_salles = self.creer_pioche_initiale()

    def creer_pioche_initiale(self):
        pioche = []
        pioche.extend(creer_salles_bleues())
        pioche.extend(creer_salles_verte())
        pioche.extend(creer_salles_viollette())
        pioche.extend(creer_salles_orange())
        pioche.extend(creer_salles_jaune())
        pioche.extend(creer_salles_rouge())
        return pioche

    def placer_salle(self, salle: Salle, y: int, x: int):
        salle.position = (y, x)
        self.grille[y][x] = salle

    def get_salle_actuelle(self) -> Salle:
        return self.grille[self.pos_y][self.pos_x]

    def tenter_deplacement(self, direction: str):
        delta = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        if direction not in delta:
            return

        dy, dx = delta[direction]
        new_y = self.pos_y + dy
        new_x = self.pos_x + dx

        # Vérifie les limites
        if 0 <= new_y < TAILLE_GRILLE[1] and 0 <= new_x < TAILLE_GRILLE[0]:
            self.pos_y, self.pos_x = new_y, new_x
            self.joueur.position = (new_y, new_x)

            # Crée une nouvelle salle si vide
            if self.grille[new_y][new_x] is None and self.pioche_salles:
                nouvelle_salle = self.pioche_salles.pop(0)
                self.placer_salle(nouvelle_salle, new_y, new_x)
        else:
            print("❌ Mouvement impossible : bord du manoir atteint.")


# --- Fonctions d'affichage ---
def dessiner_grille(fenetre, manoir: Manoir):
    start_x = 50
    start_y = 50
    for y in range(TAILLE_GRILLE[1]):
        for x in range(TAILLE_GRILLE[0]):
            rect = pygame.Rect(start_x + x * TAILLE_SALLE, start_y + y * TAILLE_SALLE, TAILLE_SALLE, TAILLE_SALLE)
            salle = manoir.grille[y][x]

            if salle is None:
                pygame.draw.rect(fenetre, COULEUR_VIDE, rect)
            else:
                couleurs = {"bleue": (100, 100, 255), "verte": (50, 200, 50), "rouge": (255, 50, 50),
                            "jaune": (255, 255, 0), "viollette": (150, 50, 150), "orange": (255, 165, 0)}
                couleur_salle = couleurs.get(getattr(salle, "couleur", "orange").lower(), (150, 150, 150))
                pygame.draw.rect(fenetre, couleur_salle, rect)

            pygame.draw.rect(fenetre, COULEUR_LIGNE, rect, EPAISSEUR_LIGNE)
            if y == manoir.pos_y and x == manoir.pos_x:
                pygame.draw.rect(fenetre, (255, 255, 255), rect, 3)


def dessiner_inventaire(fenetre, manoir: Manoir, font):
    inv = manoir.joueur.inventaire
    x_offset = 50 + COTE_GRILLE_X + 30
    y_start = 60
    line_height = 35

    titre = font.render("INVENTAIRE DU JOUEUR", True, (255, 255, 255))
    fenetre.blit(titre, (x_offset, y_start))
    y_start += line_height + 10

    consommables = [
        ("Pas", getattr(inv, "pas", 0), (255, 100, 100)),
        ("Coins", getattr(inv, "coin", 0), (255, 255, 0)),
        ("Gemmes", getattr(inv, "gem", 0), (0, 255, 255)),
        ("Clés", getattr(inv, "cles", 0), (200, 200, 200)),
        ("Dés", getattr(inv, "des", 0), (150, 150, 255)),
    ]
    for nom, valeur, couleur in consommables:
        texte = font.render(f"{nom}: {valeur}", True, couleur)
        fenetre.blit(texte, (x_offset, y_start))
        y_start += line_height


# --- Boucle principale ---
def run_game():
    pygame.init()
    fenetre = pygame.display.set_mode(TAILLE_FENETRE, pygame.RESIZABLE)
    pygame.display.set_caption("Blue Prince - Version Simplifiée")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    manoir = Manoir()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    manoir.tenter_deplacement("N")
                elif event.key == pygame.K_s:
                    manoir.tenter_deplacement("S")
                elif event.key == pygame.K_q:
                    manoir.tenter_deplacement("O")
                elif event.key == pygame.K_d:
                    manoir.tenter_deplacement("E")

        fenetre.fill(COULEUR_FOND)
        dessiner_grille(fenetre, manoir)
        dessiner_inventaire(fenetre, manoir, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_game()
