# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "keyboard",
#     "plyer",  # Opcional - para notificações visuais no Windows
# ]
# ///

"""
Claude Code Command Launcher - Hotkey F8
========================================

Script de automação que:
1. Aguarda hotkey F8 ser pressionado (global hook)
2. Exibe interface UI com lista de slash commands disponíveis
3. Permite selecionar e executar comando no Claude Code CLI
4. Oferece opção de mudar pasta padrão dos commands
5. Exibe notificações visuais durante operação

Autor: Automation System
Versão: 1.2.0
"""

import os
import sys
import subprocess
import threading
import time

# Configura UTF-8 para stdout/stderr no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import keyboard
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional

try:
    from plyer import notification
    HAS_NOTIFICATION = True
except ImportError:
    HAS_NOTIFICATION = False


def show_notification(title: str, message: str, duration: int = 3):
    """
    Exibe notificação visual no Windows.

    Args:
        title: Título da notificação
        message: Mensagem a exibir
        duration: Duração em segundos
    """
    if HAS_NOTIFICATION:
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Claude Code",
                timeout=duration
            )
        except Exception:
            pass  # Fallback silencioso se notificação falhar


class CommandLauncher:
    """Gerenciador principal do launcher de comandos Claude Code."""

    def __init__(self, default_commands_dir: str = r"C:\Users\Lofrey\test\.claude\commands"):
        self.default_commands_dir = Path(default_commands_dir)
        self.current_commands_dir = self.default_commands_dir
        self.commands_cache: List[str] = []
        self.ui_window: Optional[tk.Tk] = None
        self.is_ui_open: bool = False
        self.dir_label: Optional[ttk.Label] = None

    def scan_commands_directory(self) -> List[str]:
        """
        Escaneia diretório de commands e retorna lista de arquivos .md ou .txt.

        Returns:
            Lista de nomes de arquivos de comando encontrados
        """
        commands = []

        if not self.current_commands_dir.exists():
            print(f"⚠ Diretório não encontrado: {self.current_commands_dir}", flush=True)
            return commands

        # Busca arquivos de comando (.md, .txt, ou sem extensão)
        try:
            for file_path in self.current_commands_dir.iterdir():
                if file_path.is_file() and file_path.suffix in ['.md', '.txt', '']:
                    commands.append(file_path.stem)  # Nome sem extensão
        except PermissionError as e:
            print(f"⚠ Sem permissão para acessar diretório: {e}", flush=True)

        return sorted(commands)

    def execute_command(self, command_name: str) -> None:
        """
        Executa o Claude Code CLI com o comando selecionado.

        Args:
            command_name: Nome do slash command (sem o prefixo /)
        """
        try:
            print()
            print("=" * 60, flush=True)
            print(f"[EXECUTANDO] Comando: /{command_name}", flush=True)
            print("=" * 60, flush=True)

            # Notificação visual
            show_notification(
                "Claude Code",
                f"Executando comando: /{command_name}",
                duration=2
            )

            # Comando para abrir nova janela do terminal e executar Claude Code
            # Usa 'claude' com flag --dangerously-skip-permissions para execução direta
            cmd = f'start "Claude Code - {command_name}" cmd /k claude --dangerously-skip-permissions /{command_name}'

            # Executa no diretório de trabalho atual
            subprocess.run(
                cmd,
                shell=True,
                cwd=os.getcwd(),
                check=True
            )

            print(f"✓ Comando '/{command_name}' enviado ao Claude Code", flush=True)
            print("=" * 60, flush=True)
            print()

        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao executar comando: {e}", flush=True)
            show_notification("Erro", f"Falha ao executar comando: {e}")
        except FileNotFoundError:
            print("✗ Erro: Claude Code CLI não encontrado. Verifique se está instalado.", flush=True)
            show_notification("Erro", "Claude Code CLI não encontrado")
        except Exception as e:
            print(f"✗ Erro inesperado: {e}", flush=True)
            show_notification("Erro", f"Erro: {e}")

    def change_commands_directory(self) -> None:
        """Abre diálogo para selecionar novo diretório de commands."""
        new_dir = filedialog.askdirectory(
            title="Selecione diretório de slash commands",
            initialdir=str(self.current_commands_dir)
        )

        if new_dir:
            self.current_commands_dir = Path(new_dir)
            self.refresh_commands_list()
            # Atualiza o label do diretório
            if self.dir_label:
                self.dir_label.config(text=f"Diretório: {self.current_commands_dir}")
            print(f"✓ Diretório alterado para: {self.current_commands_dir}", flush=True)

    def refresh_commands_list(self) -> None:
        """Atualiza lista de comandos na UI."""
        self.commands_cache = self.scan_commands_directory()

        if hasattr(self, 'command_listbox') and self.command_listbox:
            self.command_listbox.delete(0, tk.END)

            for cmd in self.commands_cache:
                self.command_listbox.insert(tk.END, f"/{cmd}")

            if self.commands_cache:
                self.command_listbox.selection_set(0)

    def on_double_click(self, event) -> None:
        """Manuseia duplo clique na lista de comandos."""
        self.on_execute_command()

    def on_execute_command(self) -> None:
        """Executa comando selecionado e fecha UI."""
        if not hasattr(self, 'command_listbox') or not self.command_listbox:
            return

        selection = self.command_listbox.curselection()

        if not selection:
            messagebox.showwarning("Aviso", "Selecione um comando primeiro.")
            return

        index = selection[0]  # curselection retorna uma tupla, pegamos o primeiro elemento
        command_name = self.commands_cache[index]

        # Fecha UI antes de executar
        self.close_ui()

        # Executa comando
        self.execute_command(command_name)

    def close_ui(self) -> None:
        """Fecha a janela UI de forma segura."""
        if self.ui_window:
            try:
                self.ui_window.destroy()
            except tk.TclError:
                pass
            finally:
                self.ui_window = None
                self.is_ui_open = False
                print()
                print("[UI FECHADA] Aguardando próximo trigger (F8)...", flush=True)
                print("-" * 60, flush=True)

                # Notificação de fechamento
                show_notification(
                    "Claude Code",
                    "Seletor fechado. Pressione F8 para reabrir.",
                    duration=2
                )

    def show_ui(self) -> None:
        """Exibe interface UI de seleção de comandos."""
        # Evita abrir múltiplas janelas
        if self.is_ui_open:
            if self.ui_window:
                try:
                    self.ui_window.lift()
                    self.ui_window.focus_force()
                except tk.TclError:
                    self.is_ui_open = False
            return

        self.is_ui_open = True

        # Atualiza cache de comandos
        self.commands_cache = self.scan_commands_directory()

        # Cria janela principal
        self.ui_window = tk.Tk()
        self.ui_window.title("Claude Code - Command Launcher")
        self.ui_window.geometry("500x400")
        self.ui_window.resizable(True, True)

        # Callback para quando janela é fechada
        self.ui_window.protocol("WM_DELETE_WINDOW", self.close_ui)

        # Centraliza janela na tela
        self.ui_window.eval('tk::PlaceWindow . center')

        # Frame principal
        main_frame = ttk.Frame(self.ui_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configura expansão
        self.ui_window.columnconfigure(0, weight=1)
        self.ui_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Row da lista expande

        # Título (row 0)
        title_label = ttk.Label(
            main_frame,
            text="Selecione um Slash Command",
            font=("Segoe UI", 12, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Info do diretório atual (row 1)
        self.dir_label = ttk.Label(
            main_frame,
            text=f"Diretório: {self.current_commands_dir}",
            font=("Consolas", 9),
            foreground="gray"
        )
        self.dir_label.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)

        # Lista de comandos (row 2)
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Listbox
        self.command_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            activestyle='dotbox'
        )
        self.command_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.command_listbox.yview)

        # Popula lista
        for cmd in self.commands_cache:
            self.command_listbox.insert(tk.END, f"/{cmd}")

        # Seleciona primeiro item
        if self.commands_cache:
            self.command_listbox.selection_set(0)
            self.command_listbox.focus_set()

        # Evento de duplo clique
        self.command_listbox.bind('<Double-Button-1>', self.on_double_click)

        # Frame de botões (row 3)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(0, 10))

        # Botão mudar diretório
        change_dir_btn = ttk.Button(
            button_frame,
            text="📁 Mudar Diretório",
            command=self.change_commands_directory
        )
        change_dir_btn.grid(row=0, column=0, padx=(0, 10))

        # Botão atualizar
        refresh_btn = ttk.Button(
            button_frame,
            text="🔄 Atualizar",
            command=self.refresh_commands_list
        )
        refresh_btn.grid(row=0, column=1, padx=(0, 10))

        # Botão executar
        execute_btn = ttk.Button(
            button_frame,
            text="▶ Executar",
            command=self.on_execute_command
        )
        execute_btn.grid(row=0, column=2)

        # Label de instruções (row 4)
        info_label = ttk.Label(
            main_frame,
            text="Pressione ENTER ou duplo clique para executar • ESC para cancelar",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        info_label.grid(row=4, column=0, pady=(5, 0))

        # Bind de teclas
        self.ui_window.bind('<Return>', lambda e: self.on_execute_command())
        self.ui_window.bind('<Escape>', lambda e: self.close_ui())

        # Foco na listbox
        self.command_listbox.focus_set()

        # Loop principal da UI
        self.ui_window.mainloop()

        # Garante que o estado seja resetado após fechar
        self.is_ui_open = False


def main():
    """Função principal - inicia o sistema de hotkey."""
    print("=" * 60, flush=True)
    print("Claude Code Command Launcher - Hotkey F8", flush=True)
    print("=" * 60, flush=True)
    print()
    print("✓ Script iniciado em background", flush=True)
    print("✓ Pressione F8 para abrir o seletor de comandos", flush=True)
    print("✓ Pressione CTRL+C para encerrar", flush=True)
    print()
    print("=" * 60, flush=True)
    print(">>> SISTEMA PRONTO!", flush=True)
    print(">>> Pressione [F8] em qualquer programa para abrir o seletor de comandos.", flush=True)
    print("=" * 60, flush=True)

    # Notificação inicial
    show_notification(
        "Claude Code",
        "Sistema pronto! Pressione F8 para abrir comandos.",
        duration=3
    )

    # Inicia launcher
    launcher = CommandLauncher()

    # Callback do hotkey (executa em thread separada para não bloquear)
    def on_f8_pressed():
        """Callback executado quando F8 é pressionado."""
        print()
        print("=" * 60, flush=True)
        print("[ATIVADO] Abrindo seletor de comandos...", flush=True)
        print("=" * 60, flush=True)

        # Notificação visual
        show_notification(
            "Claude Code",
            "Seletor de comandos aberto!",
            duration=2
        )

        # Tkinter deve rodar na thread principal, então agendamos via after
        # Mas como keyboard roda em thread separada, usamos threading
        ui_thread = threading.Thread(target=launcher.show_ui, daemon=True)
        ui_thread.start()

    # Registra hotkey global
    keyboard.add_hotkey('f8', on_f8_pressed, suppress=False)

    print()
    print("Aguardando trigger (F8)...", flush=True)
    print("-" * 60, flush=True)

    # Mantém script rodando em background
    try:
        keyboard.wait()  # Bloqueia até CTRL+C
    except KeyboardInterrupt:
        print("\n✓ Script encerrado pelo usuário", flush=True)
        keyboard.unhook_all()
        sys.exit(0)


if __name__ == "__main__":
    main()