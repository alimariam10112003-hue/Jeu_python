# Importations de toutes les classes logiques
from salle import Salle
from porte import Porte 
from joueur import Joueur
from aleatoire import GenerateurAlea 
from salles_speciales import EntranceHall, Antechamber 
from catalogue_salle import (
    creer_salles_bleues, creer_salles_verte, creer_salles_viollette,
    creer_salles_orange, creer_salles_jaune, creer_salles_rouge
)

class Manoir:
    # Constantes
    LIGNES = 9
    COLONNES = 5
    POS_DEPART = (LIGNES - 1, COLONNES // 2)  # (8, 2)
    POS_ARRIVEE = (0, COLONNES // 2)          # (0, 2)

    def __init__(self, joueur: Joueur, generateur_alea: GenerateurAlea):
        """
        Initialise le manoir avec la grille 9x5, le joueur, et la pioche de salles.
        """
        self.joueur = joueur
        self.generateur = generateur_alea 
        self.catalogue_pioche = self._assembler_catalogue()
        
        # Grille de jeu: une liste de listes stockant des objets Salle (ou None)
        self.grille = [[None for _ in range(self.COLONNES)] for _ in range(self.LIGNES)]
        
        # Dictionnaire pour stocker les objets Porte (liaison spatiale)
        self.portes = {} 

        # Initialisation du jeu
        self._initialiser_pieces_fixes()

    def _assembler_catalogue(self):
        """ Assemble et retourne le catalogue complet des salles à piocher. """
        catalogue = []
        catalogue.extend(creer_salles_bleues())
        catalogue.extend(creer_salles_verte())
        catalogue.extend(creer_salles_viollette())
        catalogue.extend(creer_salles_orange())
        catalogue.extend(creer_salles_jaune())
        catalogue.extend(creer_salles_rouge())
        return catalogue

    def _initialiser_pieces_fixes(self):
        """ Place l'Entrance Hall et l'Antichambre sur la grille aux positions fixes. """
        
        # 1. Salle de départ (Entrance Hall)
        entree = EntranceHall()
        
        self.placer_salle(entree, self.POS_DEPART)
        self.joueur.position = self.POS_DEPART 
        
        # 2. Salle d'arrivée (Antichambre)
        arrivee = Antechamber()
                        
        self.placer_salle(arrivee, self.POS_ARRIVEE)
        
        # 3. Crée les portes initiales de la salle de départ
        self._creer_portes_salle(self.POS_DEPART, entree)

    def _creer_portes_salle(self, pos, salle: Salle):
        """ Crée les objets Porte pour les directions actives d'une salle. """
        r, c = pos
        directions_coords = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        
        for direction, (dr, dc) in directions_coords.items():
            if salle.porte.get(direction, False):
                r_voisin, c_voisin = r + dr, c + dc
                
                # Vérifie que la position voisine est dans la grille
                if 0 <= r_voisin < self.LIGNES and 0 <= c_voisin < self.COLONNES:
                    cle_porte = tuple(sorted(((r, c), (r_voisin, c_voisin))))
                    
                    if cle_porte not in self.portes:
                        # Crée l'objet Porte en utilisant la rangée de destination
                        # Note: rangee_destination est r_voisin
                        self.portes[cle_porte] = Porte(r_voisin, self.generateur)

    def placer_salle(self, piece: Salle, position: tuple):
        """ Place une pièce sur la grille et la retire du catalogue. """
        r, c = position
        self.grille[r][c] = piece
        piece.position = position
        
        # Retirer la pièce de la pioche si elle y était
        try:
            self.catalogue_pioche.remove(piece)
        except ValueError:
            pass 


    def tirer_pieces_au_sort(self) -> list:
        """ Retourne 3 salles tirées de la pioche (délégation à GenerateurAlea). """
        return self.generateur.tirer_pieces(self.catalogue_pioche, 3)

    def deplacer_joueur(self, direction: str):
        """ Gère le mouvement, l'ouverture de porte et le lancement du tirage. """
        r_actu, c_actu = self.joueur.position
        directions_map = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        
        if direction not in directions_map: return False, "Direction invalide."

        dr, dc = directions_map[direction]
        r_nouv, c_nouv = r_actu + dr, c_actu + dc
        pos_nouv = (r_nouv, c_nouv)
        
        if not (0 <= r_nouv < self.LIGNES and 0 <= c_nouv < self.COLONNES):
            return False, "Déplacement hors limite (mur)."

        current_room = self.grille[r_actu][c_actu]

        # Vérifie si une porte existe dans la salle actuelle
        if not current_room or not current_room.porte.get(direction, False):
             return False, "Mur interne : La salle n'a pas de porte dans cette direction."
        
        cle_porte = tuple(sorted((self.joueur.position, pos_nouv)))
        porte = self.portes.get(cle_porte)
        
        if porte is None: return False, "Erreur logique: Porte non trouvée."


        salle_destination = self.grille[r_nouv][c_nouv]
        
        # CAS 1: Nouvelle Salle à Placer (Déclenchement du Tirage)
        if salle_destination is None:
            
            # Tente d'ouvrir la porte
            if not porte.est_ouverte:
                succes, message = porte.ouvrir(self.joueur)
                if not succes:
                    # Retourne None pour indiquer l'échec et le message (la boucle de jeu le gérera)
                    return None, message 

            # Si la porte est ouverte (ou vient de l'être), on tire les cartes
            return self.tirer_pieces_au_sort(), "Menu de tirage de salle activé."


        # CAS 2: Salle Déjà Placée (Déplacement simple)
        else:
            if not porte.est_ouverte:
                # Vérifie si la porte existante peut être ouverte si elle était verrouillée
                succes, message = porte.ouvrir(self.joueur) 
                if not succes:
                    return False, "Porte verrouillée. Clé manquante."

            if not self.joueur.deplacement(): # Coût de 1 pas (méthode de Joueur)
                return False, "Pas épuisés. Fin de partie."
            
            self.joueur.position = pos_nouv
            salle_destination.interagir(self.joueur) # Déclenchement des effets de la salle
            
            if salle_destination.effet == "Victoire":
                return True, "Victoire!"
                
            return True, f"Déplacement vers {salle_destination.nom} réussi."