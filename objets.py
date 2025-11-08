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

# --- CORRECTION DE LA LOGIQUE DANS CETTE FONCTION ---
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
