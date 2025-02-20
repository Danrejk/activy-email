import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def runAVD():
    try:
        result = subprocess.run(
            "emulator -avd activyPDW",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else str(e)

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Failed to start emulator:\n{error_message}")
