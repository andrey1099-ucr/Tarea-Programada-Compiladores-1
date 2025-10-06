from src.Parser import Parser

FILE = "./tests/input_test11.txt"

if __name__ == "__main__":
    # Build parser (and its lexer)
    parser = Parser(debug=False)
    parser.build(build_lexer=True)

    # Read source file
    with open(FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # Parse to AST
    ast = parser.parse(data)

    # Output
    print("=== AST ===")
    print(ast)

    print("\n=== ERRORS ===")
    print(len(parser.errors))
    for e in parser.errors:
        print(e)
