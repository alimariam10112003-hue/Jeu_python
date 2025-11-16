import random
import numpy as np

class GenerateurAlea:
    """
    Gère les mécanismes aléatoires du jeu : tirage de pièces pondéré et niveau de verrouillage des portes.
    Utilité: Centraliser la logique de probabilité et de sélection pour garantir la progression
    et la difficulté des salles/portes.
    """
    def __init__(self):
        """Initialise la classe GenerateurAlea (aucun attribut spécifique requis pour l'instant)."""
        pass
        
    def tirer_niveau_verrouillage(self, row: int) -> int:
        """
        Détermine le niveau de verrouillage (0, 1 ou 2) en fonction de la rangée (row) de la salle de destination.
        Le niveau de difficulté augmente à mesure que la rangée diminue (plus on monte vers la sortie).
        
        * row: La rangée de la salle de destination (0 = haut, 8 = bas).
        
        Retourne le niveau de verrouillage (0, 1 ou 2).
        
        Nouveau Barème Fixe (9 rangées, numérotées 8 à 0 du bas vers le haut) :
        - Rangées 8, 7, 6, 5, 4 (row >= 4) : Niveau 0 (Déverrouillé)
        - Rangées 3, 2 (4 > row >= 2)     : Niveau 1 (Verrouillé simple, clé ou crochetage)
        - Rangées 1, 0 (row < 2)          : Niveau 2 (Double tour, clé uniquement)
        """
        ROWS = 9 
        
        # Rangées 8, 7, 6, 5, 4 (row >= 4) : Niveau 0 (Déverrouillé)
        if row >= ROWS - 5:
            return 0 
        
        # Rangées 3, 2 (row >= 2) : Niveau 1 (Verrouillage simple)
        if row >= ROWS - 7: # Simplifie la condition '4 > row >= 2'
            return 1
        
        # Rangées 1, 0 (row < 2) : Niveau 2 (Verrouillage double tour)
        return 2

    def tirer_pieces(self, catalogue: list, n=3, dir_cible=None):
        """
        Tirage des pièces (salles), en appliquant une pondération basée sur la rareté
        et un 'boost' si la pièce possède la porte dans la direction cible (`dir_cible`).
        Garantit qu'au moins une pièce gratuite et stratégique (si possible) est proposée.
        
        * catalogue: La liste des objets Salle disponibles (la pioche).
        * n: Le nombre de pièces à tirer (par défaut 3).
        * dir_cible: La direction souhaitée pour le déplacement (ex: 'N' pour la progression).
        
        Retourne une liste de `n` objets Salle proposés.
        """
        pieces_list = []; poids_list = []
        
        # Facteur de boost appliqué aux pièces qui ont la porte recherchée (très élevé pour forcer la progression)
        BOOST_FACTOR = 500 
        
        # 1. Préparation de la pioche pondérée
        for piece in catalogue:
            if piece is None: continue
            
            # Récupération des attributs de la pièce (compatible avec objets ou dictionnaires)
            if hasattr(piece, 'rarete'):
                rarete = piece.rarete; cout_gem = piece.cout_gem; porte = piece.porte
            else:
                rarete = piece.get("rarete", 0); cout_gem = piece.get("cout_gem", 0)
                porte = piece.get("porte", {})
                
            # Calcul du poids : Les pièces plus rares (rarete élevée) ont un poids plus faible.
            poids = 1.0 / (3 ** rarete)
            
            # Logique de BOOST : Multiplie le poids si la pièce contient la porte de la direction cible
            if dir_cible and porte.get(dir_cible) is True:
                poids *= BOOST_FACTOR
                
            pieces_list.append(piece); poids_list.append(poids)
            
        if not pieces_list: return []
        
        pieces_proposees = []
        
        # =================================================================
        # 2. LOGIQUE DE GARANTIE : SÉLECTIONNER ET RETIRER LA PIÈCE GRATUITE STRATÉGIQUE
        # =================================================================
        
        # Filtrer les pièces gratuites (coût en gemme = 0)
        pieces_gratuites_disponibles = [p for p in pieces_list if (hasattr(p, 'cout_gem') and p.cout_gem == 0) or (isinstance(p, dict) and p.get("cout_gem", 0) == 0)]
        
        piece_garantie = None
        
        if pieces_gratuites_disponibles:
            # Priorité 1: Pièce Gratuite NORD/SUD si l'on vise le NORD (pour assurer la continuité)
            if dir_cible == 'N':
                pieces_gratuites_NORD_PROGRESSION = []
                for p in pieces_gratuites_disponibles:
                    # La pièce doit avoir une porte NORD et SUD pour garantir une sortie
                    porte = p.porte if hasattr(p, 'porte') else p.get('porte', {})
                    if porte.get('N') is True and porte.get('S') is True:
                        pieces_gratuites_NORD_PROGRESSION.append(p)
                
                if pieces_gratuites_NORD_PROGRESSION:
                    # Tirage pondéré parmi ces pièces stratégiques
                    indices_progression = [pieces_list.index(p) for p in pieces_gratuites_NORD_PROGRESSION]
                    poids_progression = [poids_list[i] for i in indices_progression]
                    
                    if sum(poids_progression) > 0:
                        piece_garantie = random.choices(pieces_gratuites_NORD_PROGRESSION, weights=poids_progression, k=1)[0]
                    else:
                        piece_garantie = random.choice(pieces_gratuites_NORD_PROGRESSION)
            
            # Priorité 2: Si aucune pièce stratégique n'a pu être sélectionnée, choisir n'importe quelle pièce gratuite
            if piece_garantie is None:
                piece_garantie = random.choice(pieces_gratuites_disponibles)
                
        # Si une pièce est garantie, l'ajouter aux propositions et la retirer de la pioche temporaire pour le tirage final
        if piece_garantie:
            pieces_proposees.append(piece_garantie)
            
            try:
                # Retirer la pièce et son poids des listes pour le tirage pondéré restant
                index_a_retirer = pieces_list.index(piece_garantie)
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
                # Normalisation des poids pour le tirage numpy
                poids_norm = np.array(poids_list) / poids_total
                
                try:
                    # Utilise numpy.random.choice pour le tirage pondéré (sans remplacement si possible)
                    tirage_pondere = np.random.choice(
                        pieces_list, 
                        size=pieces_restantes_a_tirer, 
                        p=poids_norm, 
                        replace=False if len(pieces_list) >= pieces_restantes_a_tirer else True
                    ).tolist()
                    pieces_proposees.extend(tirage_pondere)
                except Exception as e:
                    # Fallback en cas d'erreur dans le tirage pondéré
                    print(f"Erreur de tirage pondéré final: {e}")
                    pieces_proposees.extend(random.sample(pieces_list, min(pieces_restantes_a_tirer, len(pieces_list))))
            else:
                # Fallback: Tirage aléatoire sans pondération si les poids sont tous nuls
                pieces_proposees.extend(random.sample(pieces_list, min(pieces_restantes_a_tirer, len(pieces_list))))

        return pieces_proposees[:n]