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

    """
    Classe de base pour tous les objets du jeu.
    Utilité: Définit les propriétés communes (nom, description) et la méthode
    principale d'interaction avec le joueur, y compris les effets de salle.
    """

    def __init__(self, nom: str, description: str):
        
        """
        Initialisation d'un objet.
        
        * nom: Nom de l'objet ou de l'élément de salle (ex: "Clé", "Chapel").
        * description: Description de l'objet/élément.
        """

        self.nom = nom
        self.description = description
        
    def interaction(self, joueur):
        
        """
        Gère l'interaction du joueur avec l'objet ou l'effet de salle.
        Cette méthode contient la logique pour les malus/bonus de certaines salles
        ainsi que la logique de ramassage des objets présents dans la salle.
        
        * joueur: L'objet Joueur interagissant.
        """
        
        print(f"Interaction avec l'objet : {self.nom}")

        # Définition d'abord des malus (logique spécifique aux noms de salles)
        if self.nom == "Chapel":
            joueur.inventaire.retirer_coin(1) 
            print("Malus: Vous perdez 1 Coin.")
            
        elif self.nom == "Gymnasium":
            joueur.inventaire.depenser_pas(5)
            print("Malus: Vous perdez 5 Pas.")

        # Définition des bonus (logique spécifique aux noms de salles)
        elif self.nom == "Bedroom":
            pas_gagnes = random.randint(1, 5) 
            joueur.inventaire.gagner_pas(pas_gagnes)
            print(f"Bonus: Vous regagnez {pas_gagnes}.")
            
        elif self.nom == "Wine cellar":
            # Effet à définir, actuellement neutre
            pass 
            
        elif self.nom == "Ballroom":
            joueur.inventaire.gem = 2
            print("Effet: Votre compte de Gemmes est réinitialisé à 2.")

        # --- Logique de ramassage des objets dans la salle ---
        
        # Initialisation de la liste des objets à retirer de la salle
        objets_a_retirer = []
        
        # Vérification si l'attribut self.objets existe (i.e., si self est une instance de Salle)
        if hasattr(self, 'objets'):
            for objet in self.objets:
                # 1. Gestion des consommables (Clé, Gemme, Coin, Nourriture)
                if isinstance(objet, Cle):
                    joueur.inventaire.gagner_cle(1)
                    objets_a_retirer.append(objet)
                    print(f"Objet ramassé: {objet.nom}")
                    
                elif isinstance(objet, Nourriture):
                    objet.utiliser(joueur)
                    objets_a_retirer.append(objet)
                    print(f"Nourriture utilisée: {objet.nom}")
                    
                elif isinstance(objet, Gem):
                    joueur.inventaire.gagner_gemme(1)
                    objets_a_retirer.append(objet)
                    print(f"Objet ramassé: {objet.nom}")

                elif isinstance(objet, Coin):
                    joueur.inventaire.gagner_coin(1)
                    objets_a_retirer.append(objet)
                    print(f"Objet ramassé: {objet.nom}")
                    
                # 2. Objets Permanents
                elif isinstance(objet, Permanent):
                    objet.ramasser(joueur)
                    objets_a_retirer.append(objet) 
                    
                # 3. Éléments Interactifs (simplement notés)
                elif isinstance(objet, Interactif):
                    print(f"Élément interactif trouvé: {objet.nom}.")
            
            # Mise à jour de la liste des objets de la salle: retire ceux qui ont été ramassés
            self.objets = [i for i in self.objets if i not in objets_a_retirer]


class Consommable(Objet):
    """
    Sous-classe d'Objet. Représente les objets qui sont retirés de l'inventaire 
    (ou de la salle) après leur utilisation/consommation.
    """
    def __init__(self, nom: str, description: str):
        Objet.__init__(self, nom, description)

class Permanent(Objet):
    """
    Sous-classe d'Objet. Représente les objets qui confèrent un avantage permanent 
    au joueur une fois ramassés.
    """
    
    def __init__(self, nom: str, description: str):
        Objet.__init__(self, nom, description) 

    def ramasser(self, joueur):
        """
        Met à jour l'inventaire du joueur pour indiquer la possession de l'objet permanent.
        """
        if self.nom == "Pelle":
            joueur.inventaire.possede_pelle = True
        elif self.nom == "Marteau":
            joueur.inventaire.possede_marteau = True
        elif self.nom == "Kit de Crochetage":
            joueur.inventaire.possede_kit_crochetage = True
        # Ajouter ici la logique pour Détecteur de Métaux et Patte de Lapin
        print(f"Objet permanent acquis: {self.nom}")

class Cle(Consommable):
    """Représente une clé, utilisée pour ouvrir portes et coffres."""
    def __init__(self, type_cle: str = "Key"):
        Consommable.__init__(self, type_cle, "Ouvre une porte ou un coffre.")
        
class Gem(Consommable):
    """Représente une gemme, utilisée pour accéder aux salles payantes."""
    def __init__(self):
        Consommable.__init__(self, "Gem", "Permet d'entrée dans les salles payantes.")

class Coin(Consommable):
    """Représente une pièce, monnaie principale du jeu."""
    def __init__(self):
        Consommable.__init__(self, "Coin", "Monnaie du jeu.")

class De(Consommable):
    """Représente un dé, utilisé pour relancer un tirage de salles."""
    def __init__(self):
        Consommable.__init__(self, "Dé", "Permet de relancer le tirage de 3 salles.")

class Nourriture(Consommable):
    """Représente les items de nourriture qui redonnent des Pas au joueur."""
    
    def __init__(self, nom: str, pas_rendus: int):
        Consommable.__init__(self, nom, f"Redonne {pas_rendus} Pas.")
        self.pas_rendus = pas_rendus
        
    def utiliser(self, joueur):
        """Ajoute le nombre de Pas rendus à l'inventaire du joueur."""
        joueur.inventaire.gagner_pas(self.pas_rendus)

class Interactif(Objet):
    """
    Sous-classe d'Objet. Représente les éléments de la salle avec lesquels le 
    joueur doit/peut interagir, mais qui ne sont pas ramassés directement (ex: coffre, trou).
    """
    
    def __init__(self, nom: str, description: str, est_ouvert: bool = False):
        Objet.__init__(self, nom, description)
        self.est_ouvert = est_ouvert

class CoffreCode(Interactif):
    """Un coffre à code qui nécessite un code, une clé ou un marteau pour s'ouvrir."""
    def __init__(self, nom: str = "Coffre fort à code"):
        Interactif.__init__(self, nom, "Nécessite un code ou une clé/marteau pour être ouvert.")

class TrouACreuser(Interactif):
    """Un trou dans le sol qui peut être fouillé avec la Pelle."""
    def __init__(self):
        Interactif.__init__(self, "Trou à Creuser", "Peut être fouillé avec la Pelle.", est_ouvert=False)

class Vehicule(Interactif):
    """Un véhicule spécial qui offre une récompense unique une fois utilisé."""
    def __init__(self, nom: str, recompense: str):
        Interactif.__init__(self, nom, f"Véhicule spécial. Utilisation unique pour {recompense}.")
        self.recompense = recompense
        self.utilise = False
        
        
#Instances d'objets Permanents et Véhicules (on utilise pas tout finalement)

Tank = Vehicule("Tank", recompense="Marteau (Hammer)")
Marteau_P = Permanent("Marteau", PERMANENT_VALEURS["Marteau"]) 
Pelle_P = Permanent("Pelle", PERMANENT_VALEURS["Pelle"])
KitCrochetage_P = Permanent("Kit de Crochetage", PERMANENT_VALEURS["Kit de Crochetage"])


#Fonctions utilitaires pour la création d'objets 

def lot_coins(quantite: int) -> list[Coin]:
    """Crée et retourne une liste d'instances de Coin en fonction de la quantité spécifiée."""
    return [Coin() for _ in range(quantite)]

def creer_nourriture_specifique(nom: str) -> Nourriture:
    """
    Crée une instance de Nourriture spécifique basée sur son nom.
    Si le nom n'existe pas, retourne une pomme par défaut.
    """
    pas_rendus = NOURRITURE_VALEURS.get(nom, 0)
    
    if pas_rendus > 0:
        return Nourriture(nom, pas_rendus)
    # pomme par défaut
    return Nourriture("Pomme", 2) 

def objet_aleatoire_base():
    """Crée et retourne un objet consommable de base aléatoire (Clé, Gemme, Dé)."""
    choix = random.choice([Cle(), Gem(), De()])
    return choix

def creer_objet_aleatoire_nourriture() -> Nourriture:
    """Crée et retourne une instance d'un type de Nourriture choisi aléatoirement."""
    nom_aleatoire = random.choice(list(NOURRITURE_VALEURS.keys()))
    return creer_nourriture_specifique(nom_aleatoire)