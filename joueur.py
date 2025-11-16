class Inventaire:
    def __init__(self):
        """
        Initialise l'Inventaire du joueur avec les ressources de départ et les objets permanents.

        Les ressources consommables sont :
        - [cite_start]pas (initialement à 70) [cite: 47]
        - [cite_start]coin (Pièces d'or, initialement à 0) [cite: 48]
        - [cite_start]gem (Gemmes, initialement à 2) [cite: 49]
        - [cite_start]cles (Clés, initialement à 0) [cite: 50]
        - [cite_start]des (Dés, initialement à 0) [cite: 51]
        
        Les attributs 'possede_...' sont des indicateurs d'objets permanents rares.
        """
        self.pas = 70 
        self.coin = 0 
        self.gem = 2 
        self.cles = 0 
        self.des = 0 
        self.possede_pelle = False 
        self.possede_marteau = False 
        self.possede_kit_crochetage = False 
        self.possede_detecteur_metaux = False
        self.possede_patte_lapin = False 

    def get_cles(self) -> int: 
        """Nombre de clés"""
        return self.cles

    def possede_kit_crochetage(self) -> bool: 
        """Si le joueur possède le Kit de Crochetage."""
        return self.possede_kit_crochetage 

    def depenser_pas(self, quantite: int = 1) -> bool:
        """
        Déduit le nombre de pas spécifié. [cite_start]Est appelé à chaque déplacement entre pièces (perte de 1 pas). [cite: 47]

        :param quantite: Nombre de pas à dépenser (défaut: 1).
        :return: True si le joueur avait suffisamment de pas pour la dépense, False sinon.
        """
        if self.pas >= quantite:
            self.pas -= quantite
            return True
        return False
        
    def gagner_pas(self, quantite: int):
        self.pas += quantite

    def retirer_cle(self, quantite: int = 1) -> bool: 
        """Consomme une clé.
        :param quantite: Nombre de clés à retirer (défaut: 1).
        :return: True si la dépense est réussie, False sinon (clés insuffisantes).
        """
        if self.cles >= quantite:
            self.cles -= quantite
            return True
        return False
        
    def gagner_cle(self, quantite: int = 1):
        self.cles += quantite
        
    def retirer_gemme(self, quantite: int = 1) -> bool: 
        if self.gem >= quantite:
            self.gem -= quantite
            return True
        return False
        
    def gagner_gemme(self, quantite: int = 1):
        self.gem += quantite
        
    def retirer_coin(self, quantite: int = 1) -> bool:
        """
        Déduit le nombre de pièces d'or spécifié. [cite_start]Utilisé pour dépenser de l'or dans les magasins. [cite: 48, 98]

        :param quantite: Nombre de pièces d'or à retirer (défaut: 1).
        :return: True si la dépense est réussie, False sinon (pièces d'or insuffisantes).
        """
        if self.coin >= quantite:
            self.coin -= quantite
            return True
        return False
        
    def gagner_coin(self, quantite: int = 1):
        """Ajoute des pièces d'or à l'inventaire du joueur."""
        self.coin += quantite

class Joueur:
    """
    Représente l'entité du joueur dans le jeu. 
    Contient l'inventaire (Inventaire) et la position actuelle dans la grille du manoir.
    """
    def __init__(self, position_depart: tuple = (8, 2)):
        """
        Initialise le joueur à la position de départ par défaut (l'Entrance Hall)
        et crée son inventaire.

        :param position_depart: Tuple (ligne, colonne) de la position initiale du joueur.
        """
        self.position = position_depart
        self.inventaire = Inventaire()
        
    def deplacement(self) -> bool:
        """
        Tente de consommer un pas via l'inventaire pour effectuer un mouvement.

        :return: True si le pas a été dépensé avec succès, False si les pas sont épuisés.
        """
        return self.inventaire.depenser_pas(1)