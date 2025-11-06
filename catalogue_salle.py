from salle import Salle
from salles_speciales import EntranceHall, Antechamber

def creer_salles_bleues():
    salles_bleues = [
        # 5 de niveau de rareté 0
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
            objets=["4 Coins", "Random Food"], 
            effet="Contient 4 Coins et 1 objet Nourriture.",)
        
        # 5 de rareté 1
        Salle(
            nom="Laboratoryr",
            couleur="bleue",
            image_path="img/laboratory.png", 
            cout=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Redbul"], 
            effet=None,)

        
        Salle(
            nom="Rumpus Room",
            couleur="bleue",
            image_path="img/rumpus_room.png", 
            cout=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["8 coins"], 
            effet="Alzara: 1 coin contre une prédiction sur l'avenir ",)

        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        
        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        # 5 de rareté 2
        Salle(
            nom="Room 8",
            couleur="bleue",
            image_path="img/room_8.png", 
            cout=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets=["Key"], 
            effet=None,)

        Salle(
            nom="Rotunda",
            couleur="bleue",
            image_path="img/rotunda.png", 
            cout=3,
            rarete=2, 
            condition_placement="Centrale",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Rotation de la pièce",)

        Salle(
            nom="Attic",
            couleur="bleue",
            image_path="img/attic.png", 
            cout=3,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["8 items random"], 
            effet="Contient 8 objets aléatoire",)

        
        Salle(
            nom="Trophy Room",
            couleur="bleue",
            image_path="img/trophy_room.png", 
            cout=5,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[], 
            effet="Récompense en fonction du nombre de trophées collectés."",)

        Salle(
            nom="Vault",
            couleur="bleue",
            image_path="img/vault.png", 
            cout=3,
            rarete=2, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["40 coins"], 
            effet="Contient des coffres",)
        
        # 5 de rareté 3
        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        
        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)

        Salle(
            nom="",
            couleur="",
            image_path="img/.png", 
            cout=,
            rarete=, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[""], 
            effet="",)