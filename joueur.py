# Classes Inventaire et Joueur pour gérer les ressources et la position du joueur

class Inventaire:

    """
    Initialisation de la classe "Inventaire" permettant de suivre les ressources
    et objets possédés par le joueur.
    Utilité: Regrouper les variables de l'inventaire et les fonctions associées
    pour gérer les gains et dépenses de ressources.
    """

    def __init__(self):
        
        """
        Initialisation des attributs de l'inventaire.
        
        * pas: nombre de pas/mouvements restants (initialisé à 70)
        * coin: nombre de pièces/monnaie (initialisé à 0)
        * gem: nombre de gemmes (initialisé à 2)
        * cles: nombre de clés (initialisé à 0)
        * des: nombre de dés (initialisé à 0)
        * possede_pelle: statut de possession de la pelle (booléen)
        * possede_marteau: statut de possession du marteau (booléen)
        * possede_kit_crochetage: statut de possession du kit de crochetage (booléen)
        * possede_detecteur_metaux: statut de possession du détecteur de métaux (booléen)
        * possede_patte_lapin: statut de possession de la patte de lapin (booléen)
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
        """Retourne le nombre actuel de clés."""
        return self.cles

    def possede_kit_crochetage(self) -> bool: 
        """Si le joueur possède le Kit de Crochetage."""
        return self.possede_kit_crochetage 

    def depenser_pas(self, quantite: int = 1) -> bool:
        """
        Tente de dépenser un certain nombre de pas.
        Retourne True si la dépense est réussie, False sinon.
        """
        if self.pas >= quantite:
            self.pas -= quantite
            return True
        return False
        
    def gagner_pas(self, quantite: int):
        """Ajoute un certain nombre de pas à l'inventaire."""
        self.pas += quantite

    def retirer_cle(self, quantite: int = 1) -> bool: 
        """
        Tente de consommer une ou plusieurs clés.
        Retourne True si la consommation est réussie, False sinon.
        """
        if self.cles >= quantite:
            self.cles -= quantite
            return True
        return False
        
    def gagner_cle(self, quantite: int = 1):
        """Ajoute une ou plusieurs clés à l'inventaire."""
        self.cles += quantite
        
    def retirer_gemme(self, quantite: int = 1) -> bool: 
        """
        Tente de dépenser une ou plusieurs gemmes.
        Retourne True si la dépense est réussie, False sinon.
        """
        if self.gem >= quantite:
            self.gem -= quantite
            return True
        return False
        
    def gagner_gemme(self, quantite: int = 1):
        """Ajoute une ou plusieurs gemmes à l'inventaire."""
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
        self.inventaire = Inventaire() # Crée une instance de l'inventaire
        
    def deplacement(self) -> bool:
        """
        Tente de consommer un pas via l'inventaire pour effectuer un mouvement.

        :return: True si le pas a été dépensé avec succès, False si les pas sont épuisés.
        """
        return self.inventaire.depenser_pas(1)