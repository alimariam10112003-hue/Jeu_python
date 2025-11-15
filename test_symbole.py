import os, pygame, sys
from pygame import freetype

pygame.init()

# Chemins à vérifier — adapte si ton fichier s'appelle différemment
candidates = [
    "fonts/Symbola.ttf",
    "fonts/NotoColorEmoji.ttf",
    "C:/Windows/Fonts/seguiemj.ttf",   # Windows emoji font
    "C:/Windows/Fonts/seguiemj.ttf"
]

print("Vérification des fichiers de police candidats :")
for p in candidates:
    print(p, "->", os.path.exists(p))

# Choisis ici la police que tu veux tester (met le chemin qui existe)
font_path = None
for p in candidates:
    if os.path.exists(p):
        font_path = p
        break

print("Police choisie pour test :", font_path)
if not font_path:
    print("Aucune police trouvée. Place Symbola.ttf dans fonts/ et relance.")
    pygame.quit()
    sys.exit(1)

# Essai avec pygame.font
try:
    pf = pygame.font.Font(font_path, 48)
    surf = pf.render("🚶 💎 🔑 🎲 🪙", True, (0,0,0))
    pygame.image.save(surf, "test_emoji_pygame_font.png")
    print("Image test enregistrée: test_emoji_pygame_font.png (pygame.font)")
except Exception as e:
    print("Erreur pygame.font:", e)

# Essai avec pygame.freetype
try:
    ff = freetype.Font(font_path, 48)
    surf2, rect = ff.render("🚶 💎 🔑 🎲 🪙", (0,0,0))
    pygame.image.save(surf2, "test_emoji_freetype.png")
    print("Image test enregistrée: test_emoji_freetype.png (pygame.freetype)")
except Exception as e:
    print("Erreur freetype:", e)

pygame.quit()
