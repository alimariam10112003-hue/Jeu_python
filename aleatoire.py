import random
from salle import Salle 

class GenerateurAlea:
    def __init__(self):
        pass

    def verrouillage(self, rangee_destination: int) -> int:
        """
        Niveau de vérouillage des portes selon leur emplacement dans la map (dans le manoir).
        Plus on monte vers la salle d'arrivée plus la difficulté augmente
        """
        if rangee_destination == 8:
            return 0
        if rangee_destination == 0:
            return 2
        
        diff = 8 - rangee_destination
        
        niveau_0 = 1 + (10 - diff)
        niveau_1 = 1 + (diff * 0.8)
        niveau_2 = 1 + (diff * 1.5)

        # random.choices => tirage pondéré
        choix = random.choices(population=[0, 1, 2], weights=[niveau_0, niveau_1, niveau_2], k=1)
        return choix[0]


    def tirer_pieces(self, catalogue_pioche: list, nombre: int) -> list:
        """
        Tirage des pièces par rareté en ayant au moins une pièce gratuite.
        """
        
        pioche_ponderee = []
        poids_cumules = []

        for piece in catalogue_pioche:
            # Assurez-vous que piece.rarete existe
            poids = 1 / (3 ** piece.rarete) 
            poids_cumules.append(poids)
            pioche_ponderee.append(piece)

        pieces_proposees = []

        # CORRECTION : Utilise piece.cout_gem pour la vérification
        pieces_gratuites = [p for p in pioche_ponderee if p.cout_gem == 0]
        
        if pieces_gratuites:
            piece_gratuite = random.choice(pieces_gratuites)
            pieces_proposees.append(piece_gratuite)
            
            # Retirer cette instance de la pioche pour ne pas la tirer deux fois
            try:
                index_a_retirer = pioche_ponderee.index(piece_gratuite)
                pioche_ponderee.pop(index_a_retirer)
                poids_cumules.pop(index_a_retirer)
            except ValueError:
                pass 
        
        pieces_restantes = nombre - len(pieces_proposees)
        
        if pieces_restantes > 0 and pioche_ponderee:
            tirage_pondere = random.choices(population=pioche_ponderee, weights=poids_cumules, k=pieces_restantes)
            pieces_proposees.extend(tirage_pondere)
            
        return pieces_proposees
