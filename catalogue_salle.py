from salle import Salle
from salles_speciales import EntranceHall, Antechamber

def creer_salles_bleues():
    salles_bleues = [
        # 5 de rareté 0
        Salle(
            nom="Spare Room",
            couleur="bleue",
            image_path="img/spare_room.png", 
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objet=[], 
            effet=None),

        Salle(
            nom="Parlor",
            couleur="bleue",
            image_path="img/parlor.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Wind-up Key"], 
            effet="Puzzle: Gagne 3 gemmes en résolvant le puzzle",)

        Salle(
            nom="Closet",
            couleur="bleue",
            image_path="img/closet.png", 
            cout=0,
            rarete=0,
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets=["Banane", "Key"],
            effet="Contient 2 objets aléatoire"),

        Salle(
            nom="Laboratoryr",
            couleur="bleue",
            image_path="img/laboratory.png", 
            cout=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Redbul"], 
            effet=None,)

        Salle(
            nom="Room 8",
            couleur="bleue",
            image_path="img/room_8.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Key"], 
            effet=None,)
        
        Salle(
            nom="Storeroom",
            couleur="bleue",
            image_path="img/Storeroom.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Key", "Gem", "Coin"], 
            effet="Contient 1 key, 1 gem et 1 coin",)

        Salle(
            nom="Pantry",
            couleur="bleue",
            image_path="img/pantry.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Key", "Gem", "Coin"], 
            effet="Contient 1 key, 1 gem et 1 coin",)

    porte={"N": True, "S": False, "E": True, "O": False}, 
    objets_initiaux=["4 Coins", "Random Food"], 
    effet="Contient 4 Coins et 1 objet Nourriture."
),