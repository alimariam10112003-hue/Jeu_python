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
            effet="Récompense en fonction du nombre de trophées collectés.",)

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
            effet="",)]


def creer_salles_verte():
    salles_bleues = [
        Salle(
            nom="Terrace",
            couleur="verte",
            image_path="img/terrace.png", 
            cout=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Items random"], 
            effet="Rend toutes les salles vertes gratuites à tirer.",)

        Salle(
            nom="Patio",
            couleur="verte",
            image_path="img/patio.png", 
            cout=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Trou à Creuser"], 
            effet="Disperse 3 coins aléatoirement dans des salles découvertes",)

        
        Salle(
            nom="Courtyard",
            couleur="verte",
            image_path="img/courtyard.png", 
            cout=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Trou à Creuser","Items random"], 
            effet="Permet d'échnange 1 coin contre 1 gemme avec l'arrosoir",)

        Salle(
            nom="Cloister",
            couleur="verte",
            image_path="img/cloister.png", 
            cout=4,
            rarete=3, 
            condition_placement="Centre du Manoir",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Puzzle"], 
            effet="Coût réduit à 9 si la pièce Terrace est présente",)

        Salle(
            nom="Veranda",
            couleur="verte",
            image_path="img/veranda.png", 
            cout=2,
            rarete=3, 
            condition_placement="",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Items random"], 
            effet="Augmente la probabilité de trouver des objets dans les pièces vertes suivante",)]  
    ]

def creer_salles_viollette():
    salles_bleues = [
        Salle(
            nom="Bedroom",
            couleur="viollette",
            image_path="img/bedroom.png", 
            cout=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Items food random"], 
            effet="Gagne aléatoirement 1 à 5 pas.",)

        Salle(
            nom="Boudoir",
            couleur="viollette",
            image_path="img/boudoir.png", 
            cout=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Coffre fort à code"], 
            effet="Ouverture du coffre fort donne des gems aléatoirement entre 1 et 3",)

        
        Salle(
            nom="Guest Bedroom",
            couleur="viollette",
            image_path="img/guest_bedroom.png", 
            cout=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Items food random"], 
            effet="Permet de gagner un dé à l'entrée",)

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Gagne aléatoirement des pas",)

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Gagne aléatoirement des pas",)]  
    
def creer_salles_orange():
    salles_bleues = [
        Salle(
            nom="Hallway",
            couleur="orange",
            image_path="img/hallway.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Les portes sont toujours déverrouillées",)

        Salle(
            nom="West Wing Hall",
            couleur="orange",
            image_path="img/west_wing_hall.png", 
            cout=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Les portes sont toujours déverrouillées",)

        
        Salle(
            nom="Corridor",
            couleur="orange",
            image_path="img/corridor.png", 
            cout=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=[], 
            effet="les pièces sont toujours déverrouillées",)

        Salle(
            nom="Passageway",
            couleur="orange",
            image_path="img/passageway.png", 
            cout=2,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Les portes sont toujours déverrouillées",)

        Salle(
            nom="Great Hall",
            couleur="orange",
            image_path="img/great_hall.png", 
            cout=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Contient 7 portes toujours verouillées. Toutes les portes sont déverouillées si le Foyer est dans le Manoir",)]  