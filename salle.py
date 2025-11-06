# Objectif: Création de la classe "Salle" qui définit les propriétes communes des salles
# Module random pour les mécanismes aléatoire (tirage pièce, statut porte, présences objets ect.)

import random 

class Salle:
    """
    Initialisation de la classe "Salle" permettant de définir les propriétes communes des salles.
    Utilité: regrouper les variables pour décrire une pièce et le traitement associé aux pièces.
    """
    
    def __init__(self, nom: str, couleur: str,image_path: str, cout: int, rarete: int, porte: dict, objet: list = None, effet: str = None):
        """
        Initialisation d'une salle
        
        * nom: nom de la pièce
        * couleur: couleur de la pièce (jaune,verte,violette,orange,rouge,bleu)
        * cout: coût en gemme de de la pièce 
        * rarete: rareté de la pièce (entier entre 0 et 3)
        * porte: porte disponible (ou non) dans la pièce
        * objet: objet contenu dans la pièce
        * effet: effet spécial de la pièce
        """
        
        self.nom = nom
        self.couleur = couleur
        self.cout = cout
        self.rarete = rarete
        self.porte = porte
        self.objet = objet if objet is not None else []
        self.effet = effet
        self.position = None 

    def objets(self):
        """
        Détermine aléatoirement si il a des objets ou non dans la pièce.
        """

        pass
            
    def interagir(self, joueur):
        """
        Gestion effets spéciaux et intération avec des objets
        """
        print(f"Interaction dans la salle: {self.nom} (Couleur: {self.couleur})")
        pass
        
    def __str__(self):
        """Caractéristique de chaque salle"""
        return f"Salle: {self.nom} | Couleur: {self.couleur} | Coût: {self.cout_gemmes} | Rareté: {self.rarete}"