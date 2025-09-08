from src.Lexer import Lexer
from src.utils import Error

FILE = "./tests/input_errors_demo.txt"

if __name__ == "__main__":
    # Create shared error list and lexer
    errors: list[Error] = []
    lx = Lexer(errors, debug=False)
    lx.build()

    # Read source file and feed it to the lexer
    with open(FILE, "r", encoding="utf-8") as f:
        lx.input(f.read())

    # Tokenize and print tokens
    while True:
        tok = lx.token()
        if not tok:
            break  # no more input
        print(f"{tok.lineno:4d}  {tok.type:<16} {repr(tok.value)}")

    print("FINAL")
    print("Errors:", len(errors))
    if errors:
        for e in errors:
            print(e)
