import keyboard
import subprocess
import os

def open_claude_terminal():
    # Abre novo terminal do Claude Code diretamente
    subprocess.run('start cmd /k "claude"', shell=True)

print("Sistema ativo. Pressione F10 em qualquer lugar...")
keyboard.add_hotkey('F10', open_claude_terminal)
keyboard.wait()