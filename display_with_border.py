# from colorama import Fore, Back, Style
import textwrap


########## COLORS (ANSI) #############
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

frame_width = 128
content_width = frame_width - 4
frame_color = C.GREEN


# Define helping functions for color printing, errors etc.
def fprint(text, color=C.GREEN):
    paragraphs = text.splitlines()
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            print(frame_color + f"║{" " * (frame_width - 2)}║{C.RESET}")
            continue
        lines = textwrap.wrap(paragraph, width=content_width)
        for line in lines:
            print(f"{frame_color}║ {color}{line.ljust(content_width)}{frame_color} ║{C.RESET}")

def cprint(text, color=C.CYAN):
    print(f"{color}{text}{C.RESET}")


def frame_bottom():
    print(f"{frame_color}╚{"═" * (frame_width - 2)}╝{C.RESET}\n")

def frame_top():
    print(f"\n{frame_color}╔{"═" * (frame_width - 2)}╗{C.RESET}")

#    print(f"{color}{text}{C.RESET}")


def cinput(prompt, color=C.CYAN):
    return input(f"{color}{prompt}{C.RESET}")


def error(msg):
    cprint(f"Error: {msg}", C.RED + C.BOLD)


def success(msg):
    cprint(msg, C.BLUE)


def info(msg):
    cprint(msg, C.YELLOW)


