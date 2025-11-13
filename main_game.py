import tkinter as tk
from tkinter import font

root = tk.Tk()
fonts = list(font.families())

print("Noto Color Emoji" in fonts)
print("Number of fonts found:", len(fonts))
