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

# Define helping functions for color printing, errors etc.
def cprint(text, color=""):
    print(f"{color}{text}{C.RESET}")

def cinput(prompt, color=C.CYAN):
    return input(f"{color}{prompt}{C.RESET}")

def error(msg):
    cprint(f"Error: {msg}", C.RED + C.BOLD)

def success(msg):
    cprint(msg, C.BLUE)

def info(msg):
    cprint(msg, C.YELLOW)

###########################################
# Main functions

def print_title(title):
    """Prints a title"""
    cprint(f'{"*" * 10} {title} {"*" * 10}', C.CYAN + C.BOLD)
    
def main():
    print_title("Welcome to the colors!")

if __name__ == "__main__":
    main()