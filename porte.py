# porte.py

class Porte:

    def __init__(self, rangee_destination: int, proba):
        # ... (initialisation inchangée) ...
        self.est_ouverte = False
        self.niveau_verrouillage = self.verrouillage(rangee_destination, proba)

    def verrouillage(self, rangee_destination, proba) -> int:
        # ... (logique inchangée) ...
        if rangee_destination == 8:
            return 0
        if rangee_destination == 0:
            return 2
        return proba.verrouillage(rangee_destination)

    def ressource_ouvrir(self, joueur) -> bool:
        """
        Vérification des ressources du joueurs pour ouvrir la porte (key/Lockpick Kit)
        """
        if self.est_ouverte or self.niveau_verrouillage == 0:
            return True
        elif self.niveau_verrouillage == 1:
            # Correction: Utiliser 'cles' et 'possede_kit_crochetage'
            if joueur.inventaire.cles >= 1 or joueur.inventaire.possede_kit_crochetage: 
                return True
            return False
        elif self.niveau_verrouillage == 2:
            # Correction: Utiliser 'cles'
            if joueur.inventaire.cles >= 1: 
                return True
            return False
        
        return False
    
    def ouvrir(self, joueur) -> bool:
        """
        Ouverture de la porte et consommation des ressources du joueur.
        """
        if self.est_ouverte:
            return True
        elif self.ressource_ouvrir(joueur):
            
            if self.niveau_verrouillage == 1:
                # Correction: Utiliser 'possede_kit_crochetage'
                if joueur.inventaire.possede_kit_crochetage:
                    pass 
                else:
                    # Correction: Utiliser 'retirer_cle'
                    joueur.inventaire.retirer_cle(1)
                    
            elif self.niveau_verrouillage == 2:
                # Correction: Utiliser 'retirer_cle'
                joueur.inventaire.retirer_cle(1) 
                
            self.est_ouverte = True
            return True
        
        return False