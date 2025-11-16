# Jeu_python
Projet de groupe_M1_IPS (Implémentation du jeu Blue Prince)

Ce document fournit un aperçu du projet Blue Prince, un jeu d'exploration de manoir basé sur une grille, développé en Python avec la bibliothèque Pygame. L'objectif est de trouver l'Antichambre (position en haut de la grille) avant d'être à court de ressources (pas, clés) ou d'être bloqué.

# Prérequis:
- Python (3.x),
- Bibliothèque Pygame (pour la gestion du jeu) => pip install pygame,
- Bibliothèque NumPy (pour la gestion des probabilités) => pip install numpy

# Exécution:
Pour lancer le jeu, exécutez le script principal: python main.py

# Mécaniques de Jeu:
- Blue Prince est un jeu de placement de tuiles et de gestion de ressources sur une grille de 9x5.
- Le joueur commence à la position (8, 2) (en bas) et doit atteindre la position (0, 2) (en haut).

Ressources Clés (Inventaire)
- Pas 🚶 : Dépensés pour chaque déplacement. Si épuisés, la partie est perdue.
- Gemmes 💎 : Utilisées pour acheter et placer les salles qui ont un coût.
- Clés 🔑 : Utilisées pour ouvrir les portes verrouillées (Niveaux 1 et 2).
- Kit de Crochetage : Objet permanent qui peut remplacer une clé pour les portes de Niveau 1.
- Dés 🎲 : Permettent de relancer un tirage de salle pendant la phase de sélection.

Objets Permanents :
Items uniques (Pelle, Marteau, Patte de lapin, etc.) qui confèrent des avantages durables.

Mouvement et Portes:
- Vise une direction (ZQSD/Flèches), puis appuyer sur Espace pour confirmer.Chaque mouvement coûte 1 Pas.

Le niveau de verrouillage de la porte dépend de la rangée de destination :
- Niveau 0 (Facile) : Ouvert.
- Niveau 1 (Moyen) : Nécessite 1 Clé OU un Kit de Crochetage.
- Niveau 2 (Difficile) : Nécessite 1 Clé uniquement.

Sélection et Placement de Salles:
Lorsqu'un joueur ouvre une porte vers une case vide :
- Tirage : 3 Salles sont sélectionnées aléatoirement dans le catalogue, avec une pondération.
- Choix : Le joueur sélectionne une salle et paie le coût en Gemmes.
- Rotation Automatique : La salle choisie est automatiquement tournée pour assurer la connexion physique des portes dans le Manoir.
- Effets : Le joueur entre dans la nouvelle salle, déclenchant le ramassage d'objets ou les effets spéciaux.

Conditions de Fin de Partie
- Défaite :Les Pas tombent à zéro ou le joueur est complètement bloqué (pas d'issues ouvertes et pas de ressources pour ouvrir les portes verrouillées restantes).
- Victoire : Atteindre l'Antichambre à la position (0, 2).

# Contrôles (Clavier):
- Viseur HAUT : Z ou Flèche Haut (Jeu en cours),
- Viseur BAS : S ou Flèche Bas (Jeu en cours),
- Viseur GAUCHE : Q ou Flèche Gauche (Jeu en cours),
- Viseur DROITE : D ou Flèche Droite (Jeu en cours),
- Confirmer/Déplacer : Espace (Jeu en cours, après avoir visé),
- Navigation Menu : Flèche Haut ou Flèche Bas (Menu de sélection de pièce),
- Confirmer Choix : Entrée (Menu de sélection de pièce),
- Relancer Tirage : R (Menu de sélection, coûte 1 Dé),
- Annuler Sélection : Échap (Menu de sélection de pièce),
- Quitter/Rejouer : Entrée ou Échap (Écran de Menu/Fin de partie).
- Bouton cliquable JOUER, QUITTER, AIDE

# Structure du projet:
- main.py: ùmoteur Pygame, boucle de jeu, gestion des états, affichage et logique d'interaction,
- joueur.py: classes Joueur et Inventaire,
- salle.py: classe Salle (propriétés communes des salles),
- objets.py: classes pour les items (Nourriture, Cle, Permanent, etc.),
- aleatoire.py: classe GenerateurAlea (probabilités, tirage pondéré, verrouillage),
- catalogue_salle.py: Fonctions de création des différentes collections de salles,
- salles_speciales.py: Définition des salles fixes (EntranceHall, Antechamber),
- Dossier img: les images du jeu (salles, écran de verouillage etc).