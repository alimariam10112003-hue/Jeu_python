class Inventaire:
    def __init__(self):
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
        if self.pas >= quantite:
            self.pas -= quantite
            return True
        return False
        
    def gagner_pas(self, quantite: int):
        self.pas += quantite

    def retirer_cle(self, quantite: int = 1) -> bool: 
        """Consomme une clé."""
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
        if self.coin >= quantite:
            self.coin -= quantite
            return True
        return False
        
    def gagner_coin(self, quantite: int = 1):
        self.coin += quantite

class Joueur:
    def __init__(self, position_depart: tuple = (8, 2)):
        self.position = position_depart
        self.inventaire = Inventaire()
        
    def deplacement(self) -> bool:
        return self.inventaire.depenser_pas(1)