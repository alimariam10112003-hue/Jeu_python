from salle import Salle

# Définition de la salle de départ du manoir qui n'a aucun coût, et 4 portes dans les 4 directions

class EntranceHall(Salle):

    def __init__(self):
        # La salle de départ n'a pas de coût, rareté ou condition de placement.
        # Elle a des portes dans les 4 directions par défaut dans le jeu original.
        Salle.__init__(
            self,
            nom="Entrance Hall",
            couleur="bleu",
            image_path="images/entrance_hall.png", 
            cout_gem=0,
            rarete=0,
            condition_placement="Premiere_Piece", 
            porte={"N": True, "S": True, "E": True, "O": True},
            objets_initiaux=[],
            effet=None,
            default_entry_direction="S" 
        )

# Définition de la salle d'arrivée => effet de victoire 

class Antechamber(Salle):
    
    def __init__(self):
        Salle.__init__(
            self,
            nom="Antechamber",
            couleur="bleu",
            image_path="images/antechamber.png", 
            cout_gem=0,
            rarete=3,
            condition_placement="Derniere_Piece", 
            porte={"N": False, "S": True, "E": False, "O": False},
            objets_initiaux=[],
            effet="Victoire",
            default_entry_direction="S"
        )