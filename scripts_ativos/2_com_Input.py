import keyboard
import subprocess
import tkinter as tk
from tkinter import simpledialog

def get_input_and_run():
    # Cria uma janela invisível apenas para mostrar o diálogo
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True) # Garante que fique na frente de tudo
    
    user_input = simpledialog.askstring("Claude Quick Command", "O que o Claude deve fazer?")
    
    if user_input:
        subprocess.run(f'start cmd /k "claude --dangerously-skip-permissions {user_input}"', shell=True)
    root.destroy()

print("Sistema ativo. Pressione F10 em qualquer lugar...")
keyboard.add_hotkey('F10', get_input_and_run)
keyboard.wait()