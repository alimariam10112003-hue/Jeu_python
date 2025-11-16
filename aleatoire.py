import random
import numpy as np

class GenerateurAlea:
    """
    Gère les mécanismes aléatoires du jeu : tirage de pièces pondéré et niveau de verrouillage des portes.
    """
    def __init__(self):
        pass
        
    def tirer_niveau_verrouillage(self, row: int) -> int:
        """
        Détermine le niveau de verrouillage (0, 1 ou 2) en fonction de la rangée (row) de manière déterministe.
        
        Nouveau Barème Fixe (9 rangées, numérotées 8 à 0 du bas vers le haut) :
        - Rangées 8, 7, 6, 5, 4 (row >= 4) : Niveau 0 (Déverrouillé)
        - Rangées 3, 2 (4 > row >= 2)     : Niveau 1 (Verrouillé simple)
        - Rangées 1, 0 (row < 2)          : Niveau 2 (Double tour)
        """
        ROWS = 9 
        
        # Rangées 8, 7, 6, 5, 4 (5 premières, du bas) : Niveau 0
        if row >= ROWS - 5:
            return 0 
        
        # Rangées 3, 2 : Niveau 1
        # La condition est implicite : 4 > row >= 2
        if row >= ROWS - 7: # row >= 2 (car si row >= 4 c'est Niveau 0)
            return 1
        
        # Rangées 1, 0 (2 dernières, du haut) : Niveau 2
        # La condition est implicite : row < 2
        return 2

    # Le reste de la classe (tirer_pieces) reste inchangé
    def tirer_pieces(self, catalogue: list, n=3, dir_cible=None):
        """
        Tirage des pièces, favorisant les pièces avec une porte dans la direction cible (dir_cible)
        et garantissant une pièce gratuite stratégique si besoin pour la progression NORD.
        """
        pieces_list = []; poids_list = []
        
        # Facteur de boost appliqué aux pièces qui ont la porte recherchée
        BOOST_FACTOR = 500 
        
        # 1. Préparation de la pioche pondérée
        for piece in catalogue:
            if piece is None: continue
            
            # Standardisation de l'accès aux attributs
            if hasattr(piece, 'rarete'):
                rarete = piece.rarete; cout_gem = piece.cout_gem; porte = piece.porte
            else:
                rarete = piece.get("rarete", 0); cout_gem = piece.get("cout_gem", 0)
                porte = piece.get("porte", {})
                
            poids = 1.0 / (3 ** rarete)
            
            # Logique de BOOST
            if dir_cible and porte.get(dir_cible) is True:
                poids *= BOOST_FACTOR
                
            pieces_list.append(piece); poids_list.append(poids)
            
        if not pieces_list: return []
        
        pieces_proposees = []
        
        # =================================================================
        # 2. LOGIQUE DE GARANTIE : SÉLECTIONNER ET RETIRER LA PIÈCE GRATUITE STRATÉGIQUE
        # =================================================================
        
        # Filtrer les pièces gratuites
        pieces_gratuites_disponibles = [p for p in pieces_list if (hasattr(p, 'cout_gem') and p.cout_gem == 0) or (isinstance(p, dict) and p.get("cout_gem", 0) == 0)]
        
        piece_garantie = None
        
        if pieces_gratuites_disponibles:
            # Priorité 1: Pièce Gratuite NORD/SUD si l'on vise le NORD
            if dir_cible == 'N':
                pieces_gratuites_NORD_PROGRESSION = []
                for p in pieces_gratuites_disponibles:
                    # S'assurer que les portes N et S sont ouvertes pour permettre de continuer
                    porte = p.porte if hasattr(p, 'porte') else p.get('porte', {})
                    if porte.get('N') is True and porte.get('S') is True:
                        pieces_gratuites_NORD_PROGRESSION.append(p)
                
                if pieces_gratuites_NORD_PROGRESSION:
                    # Tirage pondéré parmi les pièces NORD/SUD
                    indices_progression = [pieces_list.index(p) for p in pieces_gratuites_NORD_PROGRESSION]
                    poids_progression = [poids_list[i] for i in indices_progression]
                    
                    if sum(poids_progression) > 0:
                        piece_garantie = random.choices(pieces_gratuites_NORD_PROGRESSION, weights=poids_progression, k=1)[0]
                    else:
                        piece_garantie = random.choice(pieces_gratuites_NORD_PROGRESSION)
            
            # Priorité 2: N'importe quelle pièce gratuite
            if piece_garantie is None:
                piece_garantie = random.choice(pieces_gratuites_disponibles)
                
        # Si une pièce est garantie, l'ajouter aux propositions et la retirer de la pioche
        if piece_garantie:
            pieces_proposees.append(piece_garantie)
            
            try:
                # Trouver l'index de la pièce garantie dans la pioche initiale
                index_a_retirer = pieces_list.index(piece_garantie)
                
                # Retirer l'élément et son poids de la liste
                pieces_list.pop(index_a_retirer)
                poids_list.pop(index_a_retirer)
            except ValueError:
                pass 

        # =================================================================
        # 3. TIRAGE ALÉATOIRE PONDÉRÉ DU RESTE DES PIÈCES
        # =================================================================
        
        pieces_restantes_a_tirer = n - len(pieces_proposees)
        
        if pieces_restantes_a_tirer > 0 and pieces_list:
            poids_total = sum(poids_list)
            if poids_total > 0:
                poids_norm = np.array(poids_list) / poids_total
                
                try:
                    # Tirage pondéré des pièces restantes (sans remplacement)
                    tirage_pondere = np.random.choice(pieces_list, size=pieces_restantes_a_tirer, p=poids_norm, 
                                                     replace=False if len(pieces_list) >= pieces_restantes_a_tirer else True).tolist()
                    pieces_proposees.extend(tirage_pondere)
                except Exception as e:
                    print(f"Erreur de tirage pondéré final: {e}")
                    pieces_proposees.extend(random.sample(pieces_list, min(pieces_restantes_a_tirer, len(pieces_list))))
            else:
                # Fallback: Tirage aléatoire sans pondération si les poids sont tous nuls
                pieces_proposees.extend(random.sample(pieces_list, min(pieces_restantes_a_tirer, len(pieces_list))))

        return pieces_proposees[:n]