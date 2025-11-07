# Objectif: Création de la classe "Salle" qui définit les propriétes communes des salles
# Module random pour les mécanismes aléatoire (tirage pièce, statut porte, présences objets ect.)

import random 

class Salle:
    """
    Initialisation de la classe "Salle" permettant de définir les propriétes communes des salles.
    Utilité: regrouper les variables pour décrire une pièce et le traitement associé aux pièces.
    """
    
    def __init__(self, nom: str, couleur: str,image_path: str, cout_gem: int, rarete: int, condition_placement: str, porte: dict, objets_initiaux: list = None, effet: str = None):
        """
        Initialisation d'une salle
        
        * nom: nom de la pièce
        * couleur: couleur de la pièce (jaune,verte,violette,orange,rouge,bleu)
        * image_path: chemin de l'image de la pièce
        * cout_gem: coût en gemme de de la pièce 
        * rarete: rareté de la pièce (entier entre 0 et 3)
        * condition_placement: condition sur le placement de la pièce dans le mamoir si besoin
        * porte: porte disponible (ou non) dans la pièce
        * objets initiaux: objets contenu dans la pièce
        * effet: effet spécial de la pièce
        """
        
        self.nom = nom
        self.couleur = couleur
        self.image_path = image_path
        self.cout_gem = cout_gem
        self.rarete = rarete
        self.condition_placement = condition_placement
        self.porte = porte
        self.objets_initiaux = objets_initiaux if objets_initiaux is not None else []
        self.effet = effet

        self.position = None