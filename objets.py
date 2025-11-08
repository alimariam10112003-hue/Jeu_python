import random

# Dictionnaire de la nourriture
NOURRITURE_VALEURS = {
    "Pomme": 2,
    "Banane": 3,
    "Chocolat": 5,
    "Gâteau": 10,
    "Sandwich": 15,
    "Repas": 25,
    "Redbul": 5 
}

# Dictionnaire des objets permanents
PERMANENT_VALEURS = {
    "Pelle": "permet de creuser les trous",
    "Marteau": "ouvre les coffres sans clé",
    "Kit de Crochetage": "ouvre les portes de Niveau 1 sans clé",
    "Détecteur de Métaux": "augmente la chance de trouver des clés et des pièces",
    "Patte de Lapin": "augmente la chance de trouver tous les objets"
}

# Définition de la classe des objets du jeu (en fonction des salles)
class Objet:
    def __init__(self, nom: str, description: str):
        self.nom = nom
        self.description = description
        
    def interaction(self, joueur):
        """Intéraction du joueur avec l'objet"""
        print(f"Interaction avec l'objet : {self.nom}")

        # Définition d'abord des malus
        if self.nom == "Chapel":
            joueur.inventaire.retirer_coin(1) 
            print("Malus: Vous perdez 1 Coin.")
            
        elif self.nom == "Gymnasium":
            joueur.inventaire.depenser_pas(5)
            print("Malus: Vous perdez 5 Pas.")

        # Définition des bonus
        elif self.nom == "Bedroom":
            pas_gagnes = random.randint(1, 5) 
            joueur.inventaire.gagner_pas(pas_gagnes)
            print(f"Bonus: Vous regagnez {pas_gagnes}.")
            
        elif self.nom == "Wine cellar":
            pass
            
        elif self.nom == "Ballroom":
            joueur.inventaire.gemmes = 2
            print("Effet: Votre compte de Gemmes est réinitialisé à 2.")

        objets_a_retirer = []
        for objet in self.objets:
            if isinstance(objet, Cle):
                joueur.inventaire.gagner_clé(1)
                objets_a_retirer.append(objet)
                print(f"Objet ramassé: {objet.nom}")
                
            elif isinstance(objet, Nourriture):
                objet.utiliser(joueur)
                objets_a_retirer.append(objet)
                print(f"Nourriture utilisée: {objet.nom}")
            
            elif isinstance(objet, Permanent):
                objet.ramasser(joueur)
                objets_a_retirer.append(objet) 
                
            elif isinstance(objet, Interactif):
                print(f"Élément interactif trouvé: {objet.nom}.")
                
        self.objets = [i for i in self.objets if i not in objets_a_retirer]

class Consommable(Objet):
    """Objet rétiré de l'inventaire après son utilisation/consommation"""
    def __init__(self, nom: str, description: str):
        Objet.__init__(self, nom, description)

class Permanent(Objet):
    """Confère un avantage dans le jeu"""
    
    def __init__(self, nom: str, description: str):
        Objet.__init__(self, nom, description) 

    def ramasser(self, joueur):
        if self.nom == "Pelle":
            joueur.inventaire.possede_pelle = True
        elif self.nom == "Marteau":
            joueur.inventaire.possede_marteau = True
        elif self.nom == "Kit de Crochetage":
            joueur.inventaire.possede_kit_crochetage = True
        print(f"Objet permanent acquis: {self.nom}")

class Cle(Consommable):
    def __init__(self, type_cle: str = "Key"):
        Consommable.__init__(self, type_cle, "Ouvre une porte ou un coffre.")
        
class Gem(Consommable):
    def __init__(self):
        Consommable.__init__(self, "Gem", "Permet d'entrée dans les salles payantes.")

class Coin(Consommable):
    def __init__(self):
        Consommable.__init__(self, "Coin", "Monnaie du jeu.")

class De(Consommable):
    def __init__(self):
        Consommable.__init__(self, "Dé", "Permet de relancer le tirage de 3 salles.")

class Nourriture(Consommable):
    
    def __init__(self, nom: str, pas_rendus: int):
        Consommable.__init__(self, nom, f"Redonne {pas_rendus} Pas.")
        self.pas_rendus = pas_rendus
        
    def utiliser(self, joueur):
        joueur.inventaire.gagner_pas(self.pas_rendus)

class Interactif(Objet):
    """Éléments dans la salle avec lesquels le joueur doit/peut interagir."""
    
    def __init__(self, nom: str, description: str, est_ouvert: bool = False):
        Objet.__init__(self, nom, description)
        self.est_ouvert = est_ouvert

class CoffreCode(Interactif):
    def __init__(self, nom: str = "Coffre fort à code"):
        Interactif.__init__(self, nom, "Nécessite un code ou une clé/marteau pour être ouvert.")

class TrouACreuser(Interactif):
    def __init__(self):
        Interactif.__init__(self, "Trou à Creuser", "Peut être fouillé avec la Pelle.", est_ouvert=False)

class Vehicule(Interactif):
    def __init__(self, nom: str, recompense: str):
        Interactif.__init__(self, nom, f"Véhicule spécial. Utilisation unique pour {recompense}.")
        self.recompense = recompense
        self.utilise = False
        
        
# Objet avec lesquels le joueur peut intéragir

Tank = Vehicule("Tank", recompense="Marteau (Hammer)")
Marteau_P = Permanent("Marteau", PERMANENT_VALEURS["Marteau"]) 
Pelle_P = Permanent("Pelle", PERMANENT_VALEURS["Pelle"])
KitCrochetage_P = Permanent("Kit de Crochetage", PERMANENT_VALEURS["Kit de Crochetage"])


def lot_coins(quantite: int) -> list[Coin]:
    """Crée une liste d'instances de Coin."""
    return [Coin() for _ in range(quantite)]

def creer_nourriture_specifique(nom: str) -> Nourriture:
    """Instance de Nourriture """
    pas_rendus = NOURRITURE_VALEURS.get(nom, 0)
    
    if pas_rendus > 0:
        return Nourriture(nom, pas_rendus)
    # pomme par défaut
    return Nourriture("Pomme", 2) 

def objet_aleatoire_base():
    """Crée un objet consommable de base aléatoire (Clé, Gemme, Dé)."""
    choix = random.choice([Cle(), Gem(), De()])
    return choix

def creer_objet_aleatoire_nourriture() -> Nourriture:
    """Crée une instance d'un type de Nourriture aléatoire."""
    nom_aleatoire = random.choice(list(NOURRITURE_VALEURS.keys()))
    return creer_nourriture_specifique(nom_aleatoire)
