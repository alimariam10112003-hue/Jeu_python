from salle import Salle
from salles_speciales import EntranceHall, Antechamber

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
            objets_initiaux=[], 
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
            objets_initiaux=["Wind-up Key"], 
            effet="Puzzle: Gagne 3 gemmes en résolvant le puzzle",
            default_entry_direction="S"),

        Salle(
            nom="Closet",
            couleur="bleue",
            image_path="img/closet.png", 
            cout_gem=0,
            rarete=0,
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Banane", "Key"],
            effet="Contient 2 objets aléatoire",
            default_entry_direction="S"),

        
        Salle(
            nom="Storeroom",
            couleur="bleue",
            image_path="img/Storeroom.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Key", "Gem", "Coin"], 
            effet="Contient 1 key, 1 gem et 1 coin",
            default_entry_direction="S"),

        Salle(
            nom="Pantry",
            couleur="bleue",
            image_path="img/pantry.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["4 Coins", "Random Food"], 
            effet="Contient 4 Coins et 1 objet Nourriture.",
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
            objets_initiaux=["Redbul"], 
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
            objets_initiaux=["8 coins"], 
            effet="Alzara: 1 coin contre une prédiction sur l'avenir ",
            default_entry_direction="S"),

        
        Salle(
            nom="Laboratory",
            couleur="bleue",
            image_path="img/laboratory.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Redbul"], 
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
            objets_initiaux=["Casiers"], 
            effet="Casiers avec des consommables. Risque élevé de perdre 10 pas à l'entrée",
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
            objets_initiaux=["Key"], 
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
            objets_initiaux=[], 
            effet="Rotation de la pièce",
            default_entry_direction="S"),

        Salle(
            nom="Attic",
            couleur="bleue",
            image_path="img/attic.png", 
            cout_gem=3,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["8 items random"], 
            effet="Contient 8 objets aléatoire",
            default_entry_direction="S"),

        
        Salle(
            nom="Trophy Room",
            couleur="bleue",
            image_path="img/trophy_room.png", 
            cout_gem=5,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[], 
            effet="Récompense en fonction du nombre de trophées collectés.",
            default_entry_direction="S"),

        Salle(
            nom="Vault",
            couleur="bleue",
            image_path="img/vault.png", 
            cout_gem=3,
            rarete=2, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["40 coins"], 
            effet="Contient des coffres",
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
            objets_initiaux=[], 
            effet="Les objets dispercées dans le Manoir sont regroupés ici à la place",
            default_entry_direction="S"),

        Salle(
            nom="Garage",
            couleur="bleue",
            image_path="img/garage.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Tank"], 
            effet="L'utilisation du véhicule donne un hammer mais coûte des pas",
            default_entry_direction="S"),

        
        Salle(
            nom="Conference Room",
            couleur="bleue",
            image_path="img/conference_room.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Les objets dispercées dans le Manoir sont regroupés ici à la place",
            default_entry_direction="S"),


        Salle(
            nom="Wine cellar",
            couleur="bleue",
            image_path="img/wine_cellar.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Wine bottles"], 
            effet="Le joueur peut consommer du vin. Chaque consommation côut 3 pas et donne 1 coin",
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
            objets_initiaux=["Items random"], 
            effet="Rend toutes les salles vertes gratuites à tirer.",
            default_entry_direction="S"),

        Salle(
            nom="Patio",
            couleur="verte",
            image_path="img/patio.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Trou à Creuser"], 
            effet="Disperse 3 coins aléatoirement dans des salles découvertes",
            default_entry_direction="S"),

        
        Salle(
            nom="Courtyard",
            couleur="verte",
            image_path="img/courtyard.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Trou à Creuser","Items random"], 
            effet="Permet d'échnange 1 coin contre 1 gemme avec l'arrosoir",
            default_entry_direction="S"),

        Salle(
            nom="Cloister",
            couleur="verte",
            image_path="img/cloister.png", 
            cout_gem=4,
            rarete=3, 
            condition_placement="Centre du Manoir",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Puzzle"], 
            effet="Coût réduit à 9 si la pièce Terrace est présente",
            default_entry_direction="S"),

        Salle(
            nom="Veranda",
            couleur="verte",
            image_path="img/veranda.png", 
            cout_gem=2,
            rarete=3, 
            condition_placement="",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Items random"], 
            effet="Augmente la probabilité de trouver des objets dans les pièces vertes suivante",
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
            objets_initiaux=["Items food random"], 
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
            objets_initiaux=["Coffre fort à code"], 
            effet="Ouverture du coffre fort donne des gems aléatoirement entre 1 et 3",
            default_entry_direction="S"),

        
        Salle(
            nom="Guest Bedroom",
            couleur="viollette",
            image_path="img/guest_bedroom.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Items food random"], 
            effet="Permet de gagner un dé à l'entrée",
            default_entry_direction="S"),

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout_gem=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Gagne aléatoirement des pas",
            default_entry_direction="S"),

        Salle(
            nom="Nursery",
            couleur="viollette",
            image_path="img/nursery.png", 
            cout_gem=1,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Gagne aléatoirement des pas",
            default_entry_direction="S"),] 
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
            objets_initiaux=[], 
            effet="Les portes sont toujours déverrouillées",
            default_entry_direction="S"),

        Salle(
            nom="West Wing Hall",
            couleur="orange",
            image_path="img/west_wing_hall.png", 
            cout_gem=0,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Les portes sont toujours déverrouillées",
            default_entry_direction="S"),

        
        Salle(
            nom="Corridor",
            couleur="orange",
            image_path="img/corridor.png", 
            cout_gem=0,
            rarete=0, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=[], 
            effet="les pièces sont toujours déverrouillées",
            default_entry_direction="S"),

        Salle(
            nom="Passageway",
            couleur="orange",
            image_path="img/passageway.png", 
            cout_gem=2,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=["Key ou Nourriture"], 
            effet="Les portes sont toujours déverrouillées",
            default_entry_direction="S"),

        Salle(
            nom="Great Hall",
            couleur="orange",
            image_path="img/great_hall.png", 
            cout_gem=0,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": True, "O": True}, 
            objets_initiaux=[], 
            effet="Contient 7 portes toujours verouillées. Toutes les portes sont déverouillées si le Foyer est dans le Manoir",
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
            objets_initiaux=["Vente de key et item"], 
            effet="Permet d'aquérir des items ou keys contre des coins",
            default_entry_direction="S"),

        Salle(
            nom="Kitchen",
            couleur="jaune",
            image_path="img/kitchen.png", 
            cout_gem=1,
            rarete=1, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Vente food"], 
            effet="Permet d'aquérir des items food contre des coins",
            default_entry_direction="S"),

        
        Salle(
            nom="Locksmith",
            couleur="jaune",
            image_path="img/locksmith.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Vente key et lockpick kits"], 
            effet="Permet d'aquérir des keys ou des kits de crochetage",
            default_entry_direction="S"),

        Salle(
            nom="Showroom",
            couleur="jaune",
            image_path="img/showroom.png", 
            cout_gem=2,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": True, "S": True, "E": False, "O": False}, 
            objets_initiaux=["Vente items permanents"], 
            effet="Permet d'aquérir des items permanents",
            default_entry_direction="S"),

        Salle(
            nom="Bookshop",
            couleur="jaune",
            image_path="img/bookshop.png", 
            cout_gem=1,
            rarete=3, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Vente books"], 
            effet="Permet d'acquérir des livres",
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
            objets_initiaux=["Random key ou food item"], 
            effet="Peut donner des pas ou des dés",
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
            effet="Perd 1 coin à chaque entrée. Briser l'hôtel permets de récupérer les coins perdus (usage unique) ",
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
            effet="Perte de 5 pas à chaque entrée dans la salle. Peut contenir une key ou un dé",
            default_entry_direction="S"),

        Salle(
            nom="Weight Room",
            couleur="rouge",
            image_path="img/weight_room.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=[], 
            effet="Permet d'échanger 5 pas cpntre 1 dé. Perte de la moitié des pas",
            default_entry_direction="S"),

        Salle(
            nom="Furnace",
            couleur="rouge",
            image_path="img/furnace.png", 
            cout_gem=0,
            rarete=2, 
            condition_placement="Aucune",
            porte={"N": False, "S": True, "E": False, "O": True}, 
            objets_initiaux=["Vente books"], 
            effet="Augmente la probabilité de tirer d'autres salles rouge",
            default_entry_direction="S"),] 
    return salles_rouge