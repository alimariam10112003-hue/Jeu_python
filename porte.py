# Classe Porte

class Porte:

    """
    Initialisation de la classe "Porte" permettant de définir l'état
    et le niveau de verrouillage d'une porte entre deux salles.
    Utilité: Gérer la logique d'accès à une salle et la consommation
    de ressources pour l'ouverture.
    """

    def __init__(self, rangee_destination: int, proba):
        
        """
        Initialisation d'une porte.
        
        * rangee_destination: La rangée de la salle de destination (influence le verrouillage).
        * proba: L'objet ou module de probabilité utilisé pour déterminer le niveau de verrouillage.
        """

        # ... (initialisation inchangée) ...
        self.est_ouverte = False  # État initial de la porte (fermée)
        self.niveau_verrouillage = self.verrouillage(rangee_destination, proba)

    def verrouillage(self, rangee_destination, proba) -> int:
        
        """
        Détermine le niveau de verrouillage de la porte (0 = ouvert, 1 = clé ou crochetage, 2 = clé).
        
        * rangee_destination: La rangée de la salle de destination.
        * proba: L'objet ou module de probabilité.
        
        Retourne le niveau de verrouillage (int).
        """

        # ... (logique inchangée) ...
        # Les rangées spécifiques peuvent avoir un niveau de verrouillage fixe
        if rangee_destination == 8:
            return 0  # Rangée 8 (probablement la sortie ou une zone de départ) est toujours ouverte
        if rangee_destination == 0:
            return 2  # Rangée 0 (probablement une zone spéciale/fin) nécessite une clé (niveau 2)
        
        # Pour les autres rangées, utilise la logique probabiliste
        return proba.verrouillage(rangee_destination)

    def ressource_ouvrir(self, joueur) -> bool:
        """
        Vérifie si le joueur possède les ressources nécessaires pour ouvrir la porte.
        Ne consomme pas les ressources.
        
        * joueur: L'objet Joueur dont on vérifie l'inventaire.
        
        Retourne True si le joueur peut l'ouvrir, False sinon.
        """
        if self.est_ouverte or self.niveau_verrouillage == 0:
            # Porte déjà ouverte ou pas de verrouillage
            return True
        elif self.niveau_verrouillage == 1:
            # Nécessite 1 clé OU le kit de crochetage
            if joueur.inventaire.cles >= 1 or joueur.inventaire.possede_kit_crochetage: 
                return True
            return False
        elif self.niveau_verrouillage == 2:
            # Nécessite 1 clé (le kit de crochetage ne fonctionne pas ici)
            if joueur.inventaire.cles >= 1: 
                return True
            return False
        
        return False
    
    def ouvrir(self, joueur) -> bool:
        """
        Tente d'ouvrir la porte. Si possible, consomme les ressources du joueur et ouvre la porte.
        
        * joueur: L'objet Joueur qui tente l'ouverture.
        
        Retourne True si la porte est ouverte (ou déjà ouverte), False sinon.
        """
        if self.est_ouverte:
            # Déjà ouverte, succès immédiat
            return True
        elif self.ressource_ouvrir(joueur):
            # Le joueur possède les ressources pour l'ouvrir
            
            if self.niveau_verrouillage == 1:
                # Niveau 1 : priorité au kit de crochetage (sans consommation)
                if joueur.inventaire.possede_kit_crochetage:
                    pass  # Ouverture sans consommation
                else:
                    # Sinon, retire une clé
                    joueur.inventaire.retirer_cle(1)
                    
            elif self.niveau_verrouillage == 2:
                # Niveau 2 : retire toujours une clé
                joueur.inventaire.retirer_cle(1) 
                
            self.est_ouverte = True
            return True
        
        # Le joueur ne peut pas ouvrir la porte
        return False