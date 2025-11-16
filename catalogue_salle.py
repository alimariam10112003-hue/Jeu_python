from salle import Salle
from salles_speciales import EntranceHall, Antechamber

"""
    Crée et retourne une liste d'instances de la classe Salle pour toutes les pièces 
    de couleur 'bleue' du manoir.

    Chaque instance de Salle est configurée avec ses attributs spécifiques : 
    nom, niveau de rareté, coût en gemmes, configuration des portes 
    (portes disponibles en N, S, E, O), et effets initiaux (objets_initiaux) 
    qui seront traités lors de l'entrée dans la salle.
    
    :return: Une liste [Salle, Salle, ...] représentant toutes les pièces bleues disponibles dans la pioche.
    """

def creer_salles_bleues():
    salles_bleues = [
        # 5 de niveau de rareté 0
        Salle(
            nom="Spare Room",
            couleur="bleue",
            image_path="img/spare_room.png", 
            cout_gem = 0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Pomme", "Gem", "Key"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Parlor",
            couleur="bleue",
            image_path="img/parlor.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Gem", "Dé", "Gem"], 
            effet=None, 
            default_entry_direction="S"),

        Salle(
            nom="Closet",
            couleur="bleue",
            image_path="img/closet.png", 
            cout_gem=0,
            rarete=0,
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Banane", "Key", "Gem"],
            effet=None, 
            default_entry_direction="S"),

        
        Salle(
            nom="Storeroom",
            couleur="bleue",
            image_path="img/Storeroom.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Key", "Gem", "Dé"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Pantry",
            couleur="bleue",
            image_path="img/pantry.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["4 Coins", "Random Food", "Gem"], 
            effet=None, 
            default_entry_direction="S"),
        
        # 4 de rareté 1
        Salle(
            nom="Laboratory",
            couleur="bleue",
            image_path="img/laboratory.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Redbul", "Gem", "Gem"],
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Rumpus Room",
            couleur="bleue",
            image_path="img/rumpus.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["8 Coins", "Gem"], 
            effet=None, 
            default_entry_direction="S"),

        
        Salle(
            nom="Laboratory",
            couleur="bleue",
            image_path="img/laboratory.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Redbul", "Key", "Gem"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Walk-in Closet",
            couleur="bleue",
            image_path="img/walk_in_closet.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key", "Gem", "Chocolat"], 
            effet=None, 
            default_entry_direction="S"),

        # 5 de rareté 2
        Salle(
            nom="Room 8",
            couleur="bleue",
            image_path="img/room_8.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Key", "Gem"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Rotunda",
            couleur="bleue",
            image_path="img/rotunda.png", 
            cout_gem=3,
            rarete=2, 
            condition_placement="Centrale",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Gem", "Gem", "Gem"], 
            effet=None, 
            default_entry_direction="S"),

        Salle(
            nom="Attic",
            couleur="bleue",
            image_path="img/attic.png", 
            cout_gem=3,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key", "Key", "Gem", "Sandwich"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Trophy Room",
            couleur="bleue",
            image_path="img/trophy_room.png", 
            cout_gem=5,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["10 Coins", "Gem", "Gem", "Gâteau"], 
            effet=None, 

            default_entry_direction="S"),

        Salle(
            nom="Vault",
            couleur="bleue",
            image_path="img/vault.png", 
            cout_gem=3,
            rarete=2, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["40 Coins"], 
            effet=None, 
            default_entry_direction="S"),
        
        # 4 de rareté 3
        Salle(
            nom="Conference Room",
            couleur="bleue",
            image_path="img/conference_room.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Gem", "Gem", "Key", "Repas"], 
            effet=None, 
            default_entry_direction="S"),

        Salle(
            nom="Garage",
            couleur="bleue",
            image_path="img/garage.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Marteau"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Conference Room",
            couleur="bleue",
            image_path="img/conference_room.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Gem", "Key", "Key", "Repas"], 
            effet=None, 
            default_entry_direction="S"),


        Salle(
            nom="Wine cellar",
            couleur="bleue",
            image_path="img/wine_cellar.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["10 Coins", "Sandwich"], 
            effet=None, 
            default_entry_direction="S"),
    ]
    return salles_bleues


def creer_salles_verte():
    salles_verte = [
        Salle(
            nom="Terrace",
            couleur="verte",
            image_path="img/terrace.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Kit de Crochetage", "Patte de Lapin", "Gem"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Patio",
            couleur="verte",
            image_path="img/patio.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Coin", "Coin", "Coin"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Courtyard",
            couleur="verte",
            image_path="img/courtyard.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Gem", "Key", "Pomme"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Cloister",
            couleur="verte",
            image_path="img/cloister.png", 
            cout_gem=4,
            rarete=3, 
            condition_placement="Centre du Manoir",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Dé", "Repas"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Veranda",
            couleur="verte",
            image_path="img/veranda.png", 
            cout_gem=2,
            rarete=3, 
            condition_placement="",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Détecteur de Métaux", "Gem"], 
            effet=None,
            default_entry_direction="S"),] 
    return salles_verte

def creer_salles_viollette():
    salles_viollette = [
        Salle(
            nom="Bedroom",
            couleur="viollette",
            image_path="img/bedroom.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Random Food"], 
            effet="Gagne aléatoirement 1 à 5 pas.",
            default_entry_direction="S"),

        Salle(
            nom="Boudoir",
            couleur="viollette",
            image_path="img/boudoir.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Gem", "Gem"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Guest Bedroom",
            couleur="viollette",
            image_path="img/guest_bedroom.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Random Food", "Dé"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout_gem=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key", "Random Food"], 
            effet="Gagne aléatoirement 1 à 5 pas.",
            default_entry_direction="S"),

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout_gem=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key", "Random Food"], 
            effet="Gagne aléatoirement 1 à 5 pas.",
            default_entry_direction="S"),
        
        Salle(
            nom="Guest Bedroom",
            couleur="viollette",
            image_path="img/guest_bedroom.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Random Food", "Dé"], 
            effet=None,
            default_entry_direction="S"),
        
        ] 
    return salles_viollette

def creer_salles_orange():
    salles_orange = [
        Salle(
            nom="Hallway",
            couleur="orange",
            image_path="img/hallway.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Pomme"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="West Wing Hall",
            couleur="orange",
            image_path="img/west_wing_hall.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Chocolat"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Corridor",
            couleur="orange",
            image_path="img/corridor.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Banane"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Passageway",
            couleur="orange",
            image_path="img/passageway.png", 
            cout_gem=2,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Key", "Random Food"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Great Hall",
            couleur="orange",
            image_path="img/great_hall.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Gem", "Gem", "Key", "Sandwich"], 
            effet=None,
            default_entry_direction="S"),] 
    return salles_orange

def creer_salles_jaune():
    salles_jaune = [
        Salle(
            nom="Commissary",
            couleur="jaune",
            image_path="img/commissary.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Key", "Sandwich"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Kitchen",
            couleur="jaune",
            image_path="img/kitchen.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Repas", "Pomme"], 
            effet=None,
            default_entry_direction="S"),

        
        Salle(
            nom="Locksmith",
            couleur="jaune",
            image_path="img/locksmith.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key", "Kit de Crochetage"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Showroom",
            couleur="jaune",
            image_path="img/showroom.png", 
            cout_gem=2,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["10 Coins", "Gem", "Gem"], 
            effet=None,
            default_entry_direction="S"),

        Salle(
            nom="Bookshop",
            couleur="jaune",
            image_path="img/bookshop.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Dé", "Dé", "Gem"], 
            effet=None,
            default_entry_direction="S"),] 
    return salles_jaune

def creer_salles_rouge():
    salles_rouge = [
        Salle(
            nom="Lavatory",
            couleur="rouge",
            image_path="img/lavatory.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Pomme"], 
            effet="Perte de 2 pas",
            default_entry_direction="S"),

        Salle(
            nom="Chapel",
            couleur="rouge",
            image_path="img/chapel.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Perte de 1 coin", 
            default_entry_direction="S"),

        
        Salle(
            nom="Gymnasium",
            couleur="rouge",
            image_path="img/gymnasium.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Perte de 5 pas", 
            default_entry_direction="S"),

        Salle(
            nom="Weight Room",
            couleur="rouge",
            image_path="img/weight_room.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Perte de 8 pas",
            default_entry_direction="S"),

        Salle(
            nom="Furnace",
            couleur="rouge",
            image_path="img/furnace.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[], 
            effet="Perte de 1 Gem", 
            default_entry_direction="S"),] 
    return salles_rouge