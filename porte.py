# Implémentation de la classe porte définissant la connexion entre deux salles du manoir.
# C'est le niveau de verrouillage d'une pièce (en fonction de la position d'apparition dans le Manoir)

class Porte:

    def __init__(self, rangee_destination: int, proba):
        """
        Initialialisation d'une nouvelle porte 

        * rangee_destination: La rangée (ligne) vers laquelle mène la porte (pour le niveau de vérouillage)
        * proba: gestion du calcul aléatoire (cf classe Aleatoire)
        """
        self.est_ouverte = False
        self.niveau_verrouillage = self.verrouillage(rangee_destination, proba)

    def verrouillage(self, rangee_destination, proba) -> int:
        """
        Détermination du niveau de verouillage aléatoirement:
        - niveau 0 : déverrouillées => 0 key
        - niveau 1 : simple tour => 1 key ou Lockpick Kit
        - niveau 2 : double tour => 1 key (Corrigé: niveau 3 -> niveau 2)
        """
        # Rangée Entrance Hall (départ) toujours de niveau 0
        if rangee_destination == 8:
            return 0
        
        # Rangée Antechamber (arrivée) toujours de niveau 2
        if rangee_destination == 0:
            return 2

        # Rangées intermédiaires => aléatoire
        return proba.verrouillage(rangee_destination)

    def ressource_ouvrir(self, joueur) -> bool:
        """
        Vérification des ressources du joueurs pour ouvrir la porte (key/Lockpick Kit)
        * joueur: instance de la classe Joueur (cf fichier Joueur)

        """

        if self.est_ouverte:
            return True
        elif self.niveau_verrouillage == 0:
            return True 
        elif self.niveau_verrouillage == 1:
            if joueur.inventaire.get_key() >= 1 or joueur.inventaire.possede_kit_crochetage(): 
                return True
            return False
        elif self.niveau_verrouillage == 2:
            if joueur.inventaire.get_key() >= 1: 
                return True
            return False
        
        return False
    
    def ouvrir(self, joueur) -> bool:
        """
        Ouverture de la porte et consommation des ressources du joueur.
        * joueur: instance de la classe Joueur 

        """
        if self.est_ouverte:
            return True
        elif self.ressource_ouvrir(joueur):
            
            if self.niveau_verrouillage == 1:
                if joueur.inventaire.possede_kit_crochetage():
                    pass 
                else:
                    joueur.inventaire.conso_cle(1)
                    
            elif self.niveau_verrouillage == 2:
                joueur.inventaire.conso_cle(1) 
                
            self.est_ouverte = True
            return True
        
        return False