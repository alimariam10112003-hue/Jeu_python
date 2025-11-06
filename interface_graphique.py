import pygame
import sys
import random
import os

# === CONFIGURATION ===
ROWS, COLS = 9, 5  # Dimensions correctes du manoir
TILE_SIZE = 100
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
INVENTORY_WIDTH = 300
SCREEN_WIDTH = WIDTH + INVENTORY_WIDTH
SCREEN_HEIGHT = HEIGHT

# === COULEURS ===
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
BLACK = (0, 0, 0)

PIECE_COLORS = {
    "bleue": (100, 100, 255),
    "verte": (100, 200, 100),
    "violette": (180, 100, 180),
    "orange": (255, 165, 0),
    "rouge": (255, 100, 100),
    "jaune": (255, 255, 100),
}

# === INITIALISATION ===
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Interface")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# === CHARGEMENT DES IMAGES ===
# (utilise un dossier "images" dans le même répertoire que ton script)
def charger_image(nom_fichier):
    chemin = os.path.join("images", nom_fichier)
    if os.path.exists(chemin):
        return pygame.image.load(chemin)
    return None  # Si le fichier n’existe pas, on évite une erreur

images_pieces = {
    "Vault": charger_image("vault.png"),
    "Veranda": charger_image("veranda.png"),
    "Bedroom": charger_image("bedroom.png"),
    "Corridor": charger_image("corridor.png"),
    "Chapel": charger_image("chapel.png"),
    "Pantry": charger_image("pantry.png"),
    "Entrance Hall": charger_image("entrance_hall.png")
}

# === ÉTAT DU JEU ===
player_pos = [4, 2]  # milieu visuel de la grille
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
grid[player_pos[0]][player_pos[1]] = {"nom": "Entrance Hall", "couleur": "bleue"}

inventory = {
    "Pas": 70,
    "Gemmes": 2,
    "Clés": 0,
    "Dés": 0,
    "Pelle": False,
    "Crochetage": False,
    "Détecteur": False,
    "Patte de lapin": False
}

choix_en_cours = False
index_selection = 0
pieces_proposees = []

# === CATALOGUE DE PIÈCES ===
catalogue_pieces = [
    {"nom": "Vault", "couleur": "bleue", "gemmes": 3, "rarete": 3},
    {"nom": "Veranda", "couleur": "verte", "gemmes": 2, "rarete": 2},
    {"nom": "Bedroom", "couleur": "violette", "gemmes": 1, "rarete": 1},
    {"nom": "Corridor", "couleur": "orange", "gemmes": 0, "rarete": 0},
    {"nom": "Chapel", "couleur": "rouge", "gemmes": 0, "rarete": 1},
    {"nom": "Pantry", "couleur": "bleue", "gemmes": 0, "rarete": 0},
]

# === FONCTIONS ===
def tirer_pieces(catalogue, n=3):
    pieces_disponibles = []
    for piece in catalogue:
        poids = 1 / (3 ** piece["rarete"])
        pieces_disponibles.append((piece, poids))

    tirage = random.choices(
        [p[0] for p in pieces_disponibles],
        weights=[p[1] for p in pieces_disponibles],
        k=n
    )

    if not any(p["gemmes"] == 0 for p in tirage):
        tirage[random.randint(0, n - 1)] = random.choice(
            [p for p in catalogue if p["gemmes"] == 0]
        )

    return tirage

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

            piece = grid[row][col]
            if piece:
                image = images_pieces.get(piece["nom"])
                if image:
                    image_scaled = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    screen.blit(image_scaled, (x, y))
                else:
                    color = PIECE_COLORS.get(piece["couleur"], GRAY)
                    pygame.draw.rect(screen, color, rect)
                    text = font.render(piece["nom"], True, BLACK)
                    screen.blit(text, (x + 5, y + 5))

            if [row, col] == player_pos:
                pygame.draw.rect(screen, RED, rect, 3)

def draw_inventory(inv):
    x = WIDTH + 20
    y = 20
    screen.fill(WHITE, pygame.Rect(WIDTH, 0, INVENTORY_WIDTH, SCREEN_HEIGHT))
    screen.blit(font.render("Inventaire", True, BLACK), (x, y))
    y += 30
    for key, value in inv.items():
        val = "✔️" if isinstance(value, bool) and value else value
        text = font.render(f"{key}: {val}", True, BLACK)
        screen.blit(text, (x, y))
        y += 25

def draw_selection_menu():
    if not choix_en_cours:
        return

    x_base = WIDTH + 20
    y_base = 250
    for i, piece in enumerate(pieces_proposees):
        y = y_base + i * 120
        rect = pygame.Rect(x_base, y, 260, 100)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, RED if i == index_selection else BLACK, rect, 2)

        image = images_pieces.get(piece["nom"])
        if image:
            img_scaled = pygame.transform.scale(image, (80, 80))
            screen.blit(img_scaled, (x_base + 10, y + 10))

        nom = font.render(piece["nom"], True, BLACK)
        gemmes = font.render(f"{piece['gemmes']} gemmes", True, BLACK)
        rarete = font.render(f"Rareté: {piece['rarete']}", True, BLACK)

        screen.blit(nom, (x_base + 100, y + 10))
        screen.blit(gemmes, (x_base + 100, y + 35))
        screen.blit(rarete, (x_base + 100, y + 60))

def move_player(dx, dy):
    new_row = player_pos[0] + dy
    new_col = player_pos[1] + dx
    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
        player_pos[0], player_pos[1] = new_row, new_col
        if grid[new_row][new_col] is None:
            grid[new_row][new_col] = {"nom": "Corridor", "couleur": "orange"}

# === BOUCLE PRINCIPALE ===
while True:
    screen.fill(WHITE)
    draw_grid()
    draw_inventory(inventory)
    draw_selection_menu()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if choix_en_cours:
                if event.key == pygame.K_UP:
                    index_selection = (index_selection - 1) % 3
                elif event.key == pygame.K_DOWN:
                    index_selection = (index_selection + 1) % 3
                elif event.key == pygame.K_RETURN:
                    piece_choisie = pieces_proposees[index_selection]
                    print(f"Tu as choisi : {piece_choisie['nom']}")
                    choix_en_cours = False
                    grid[player_pos[0]][player_pos[1]] = piece_choisie
            else:
                if event.key == pygame.K_z: move_player(0, -1)
                elif event.key == pygame.K_s: move_player(0, 1)
                elif event.key == pygame.K_q: move_player(-1, 0)
                elif event.key == pygame.K_d: move_player(1, 0)
                elif event.key == pygame.K_SPACE:
                    pieces_proposees = tirer_pieces(catalogue_pieces)
                    choix_en_cours = True
                    index_selection = 0

    clock.tick(30)
