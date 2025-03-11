import tkinter as tk
from tkinter import ttk
import sv_ttk

# Funkcja do ustawienia motywu (działa na Windows i Linux)
def apply_theme():
    sv_ttk.set_theme("dark")  # Możesz zmienić na "light", jeśli chcesz

# UI
window = tk.Tk()

button = ttk.Button(window, text="Kliknij mnie!")
button.pack()

# Zastosowanie motywu
apply_theme()

window.mainloop()
