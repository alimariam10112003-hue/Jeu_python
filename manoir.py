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
    
    """
    Classe principale représentant le plateau de jeu (le Manoir).
    Elle gère la grille des salles, les portes entre elles, la position
    du joueur et la logique de déplacement/placement des salles.
    """

    LIGNES = 9  # Nombre de rangées dans la grille
    COLONNES = 5  # Nombre de colonnes dans la grille
    POS_DEPART = (LIGNES - 1, COLONNES // 2)  # Position initiale du joueur (en bas, au centre)
    POS_ARRIVEE = (0, COLONNES // 2)         # Position de l'objectif (en haut, au centre)      

    def __init__(self, joueur: Joueur, generateur_alea: GenerateurAlea):
        
        """
        Initialise le manoir avec la grille 9x5, le joueur, et la pioche de salles.
        
        * joueur: L'instance du Joueur.
        * generateur_alea: L'instance gérant les mécanismes aléatoires (tirage, verrouillage).
        """

        self.joueur = joueur
        self.generateur = generateur_alea 
        self.catalogue_pioche = self._assembler_catalogue() # Liste des salles non encore placées
        
        self.grille = [[None for _ in range(self.COLONNES)] for _ in range(self.LIGNES)] # Grille 2D des salles
        self.portes = {} # Dictionnaire pour stocker les instances de Porte {(pos1, pos2): Porte}
        self._initialiser_pieces_fixes()

    def _assembler_catalogue(self):
        """ 
        Assemble et retourne le catalogue complet (la pioche) des salles. 
        Toutes les salles sont chargées depuis le module catalogue_salle.
        """
        catalogue = []
        catalogue.extend(creer_salles_bleues())
        catalogue.extend(creer_salles_verte())
        catalogue.extend(creer_salles_viollette())
        catalogue.extend(creer_salles_orange())
        catalogue.extend(creer_salles_jaune())
        catalogue.extend(creer_salles_rouge())
        return catalogue

    def _initialiser_pieces_fixes(self):
        """ Place l'Entrance Hall (départ) et l'Antichambre (arrivée) sur la grille aux positions fixes. """
        
        # 1. Salle de départ (Entrance Hall)
        entree = EntranceHall()
        self.placer_salle(entree, self.POS_DEPART)
        self.joueur.position = self.POS_DEPART # Met à jour la position du joueur
        
        # 2. Salle d'arrivée (Antichambre)
        arrivee = Antechamber()
        self.placer_salle(arrivee, self.POS_ARRIVEE)
        
        # 3. Crée les objets Porte pour la salle de départ
        self._creer_portes_salle(self.POS_DEPART, entree)

    def _creer_portes_salle(self, pos, salle: Salle):
        """ 
        Crée les objets Porte pour les directions actives d'une salle à une position donnée. 
        Les portes sont stockées dans le dictionnaire `self.portes`.
        """
        r, c = pos
        directions_coords = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        
        for direction, (dr, dc) in directions_coords.items():
            # Vérifie si la salle actuelle possède une porte dans cette direction
            if salle.porte.get(direction, False):
                r_voisin, c_voisin = r + dr, c + dc
                
                # Vérifie que la position voisine est dans les limites de la grille
                if 0 <= r_voisin < self.LIGNES and 0 <= c_voisin < self.COLONNES:
                    # Définit une clé de porte unique basée sur les coordonnées des deux salles
                    cle_porte = tuple(sorted(((r, c), (r_voisin, c_voisin))))
                    
                    if cle_porte not in self.portes:
                        # Crée l'objet Porte, son niveau de verrouillage dépend de la rangée de destination (r_voisin)
                        self.portes[cle_porte] = Porte(r_voisin, self.generateur)

    def placer_salle(self, piece: Salle, position: tuple):
        """ 
        Place une pièce sur la grille à la position spécifiée et la retire de la pioche. 
        """
        r, c = position
        self.grille[r][c] = piece
        piece.position = position # Met à jour la position de la salle elle-même
        
        # Retirer la pièce de la pioche si elle y était (les pièces fixes sont ignorées ici)
        try:
            self.catalogue_pioche.remove(piece)
        except ValueError:
            pass 


    def tirer_pieces_au_sort(self) -> list:
        """ 
        Délègue au GenerateurAlea la tâche de sélectionner 3 salles aléatoires 
        parmi le catalogue restant.
        Retourne la liste des 3 salles tirées.
        """
        return self.generateur.tirer_pieces(self.catalogue_pioche, 3)

    def deplacer_joueur(self, direction: str):
        """ 
        Gère la tentative de mouvement du joueur : vérifie les limites, l'existence de la porte, 
        l'ouverture de porte/consommation de ressources, et le déclenchement du tirage ou du déplacement. 
        
        Retourne:
        - (list, str) si un tirage doit être effectué (Nouvelle salle)
        - (bool, str) si un déplacement simple a lieu (Salle déjà placée) ou en cas d'erreur
        """
        r_actu, c_actu = self.joueur.position
        directions_map = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        
        if direction not in directions_map: return False, "Direction invalide."

        dr, dc = directions_map[direction]
        r_nouv, c_nouv = r_actu + dr, c_actu + dc
        pos_nouv = (r_nouv, c_nouv)
        
        if not (0 <= r_nouv < self.LIGNES and 0 <= c_nouv < self.COLONNES):
            return False, "Déplacement hors limite (mur)."

        current_room = self.grille[r_actu][c_actu]

        # Vérifie si une porte est définie dans la salle actuelle pour cette direction
        if not current_room or not current_room.porte.get(direction, False):
            return False, "Mur interne : La salle n'a pas de porte dans cette direction."
        
        cle_porte = tuple(sorted((self.joueur.position, pos_nouv)))
        porte = self.portes.get(cle_porte)
        
        if porte is None: return False, "Erreur logique: Porte non trouvée."


        salle_destination = self.grille[r_nouv][c_nouv]
        
        # CAS 1: Nouvelle Salle à Placer (Déclenchement du Tirage)
        if salle_destination is None:
            
            # Tente d'ouvrir la porte (et de consommer les ressources si nécessaire)
            succes_ouverture = porte.ouvrir(self.joueur)
            if not succes_ouverture:
                # La méthode ouvrir gère déjà la consommation ou l'échec
                # On retourne un échec de type 'None' pour indiquer le mode "tirage échoué"
                return None, "Ressources insuffisantes (Clé ou Kit de Crochetage manquant)." 

            # Si la porte est ouverte (ou vient de l'être), on déclenche le tirage des cartes
            return self.tirer_pieces_au_sort(), "Menu de tirage de salle activé."


        # CAS 2: Salle Déjà Placée (Déplacement simple)
        else:
            # Si la porte n'est pas ouverte (verrouillée), on tente de l'ouvrir/déverrouiller
            if not porte.est_ouverte:
                succes_ouverture = porte.ouvrir(self.joueur) 
                if not succes_ouverture:
                    return False, "Porte verrouillée. Clé manquante."

            # Consomme 1 Pas pour le déplacement effectif
            if not self.joueur.deplacement(): 
                return False, "Pas épuisés. Fin de partie."
            
            self.joueur.position = pos_nouv # Met à jour la position
            # Déclenche l'interaction de la salle (malus/bonus, ramassage d'objets)
            salle_destination.interagir(self.joueur) 
            
            # Vérification de la condition de victoire
            if salle_destination.effet == "Victoire":
                return True, "Victoire!"
                
            return True, f"Déplacement vers {salle_destination.nom} réussi."