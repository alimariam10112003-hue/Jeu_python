import random
from salle import Salle 

class GenerateurAlea:
    def __init__(self):
        pass

    def verrouillage(self, rangee_destination: int) -> int:
        """
        Détermine le niveau de verrouillage (0, 1 ou 2) pour une rangée intermédiaire (1 à 7).
        La probabilité de Niveau 1 et 2 augmente à mesure que la rangée diminue (on monte).
        """
        
        # Le Manoir gère déjà les rangées fixes (0 et 8). 
        # Logique simplifiée de difficulté croissante :
        
        facteur_difficulte = 8 - rangee_destination
        
        # Poids: La rareté 0 (déverrouillée) est plus probable au début (rangee 8)
        poids_niveau_0 = 10 - facteur_difficulte 
        poids_niveau_1 = 1 + facteur_difficulte * 0.8
        poids_niveau_2 = facteur_difficulte * 1.5

        # Utilisation de random.choices pour le tirage pondéré
        choix = random.choices(
            population=[0, 1, 2], 
            weights=[
                poids_niveau_0, 
                poids_niveau_1, 
                poids_niveau_2
            ], 
            k=1
        )
        return choix[0]


    def tirer_pieces(self, catalogue_pioche: list, nombre: int) -> list:
        """
        Tire un nombre donné de pièces du catalogue en respectant la rareté et en garantissant au moins une pièce gratuite.
        """
        
        pioche_ponderee = []
        poids_cumules = []
        
        # --- 1. Calcul des poids basés sur la rareté (Section 2.3) ---
        for piece in catalogue_pioche:
            # Utilise l'attribut 'rarete' de la Salle
            poids = 1 / (3 ** piece.rarete) 
            poids_cumules.append(poids)
            pioche_ponderee.append(piece)

        pieces_proposees = []

        # --- 2. Garantie d'une pièce gratuite (coût 0) ---
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
        
        # --- 3. Tirer les pièces restantes avec pondération ---
        
        pieces_restantes = nombre - len(pieces_proposees)
        
        if pieces_restantes > 0 and pioche_ponderee:
            tirage_pondere = random.choices(
                population=pioche_ponderee, 
                weights=poids_cumules, 
                k=pieces_restantes
            )
            pieces_proposees.extend(tirage_pondere)
            
        return pieces_proposees
