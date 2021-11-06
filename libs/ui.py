from sys import platform
from os import system


def clear_terminal():
    """
        Limpa o ecrã independentemente do Sistema Operativo
    """
    if platform in ["linux", "linux2", "darwin"]:
        system("clear")
    elif platform == "win32":
        system("cls")
    else:
        print("\n\n")


def render_screen(msg_history: list, username: str):
    clear_terminal()
    for msg in msg_history:
        print(msg, flush=True)
    print(username+": ", end="", flush=True)
