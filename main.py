import os
from src.Parser import Parser
from pprint import pformat

FILE = "./tests/test_OOP.py"

if __name__ == "__main__":
    # Build parser (and its lexer)
    parser = Parser(debug=False)
    parser.build(build_lexer=True)

    # Read source file
    with open(FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # Parse to AST
    ast = parser.parse(data)

    # Output to console
    print("=== AST ===")
    print(ast)

    print("\n=== ERRORS ===")
    print(len(parser.errors))
    for e in parser.errors:
        print(e)

    # Save AST to a .txt file next to the input
    out_path = os.path.splitext(FILE)[0] + ".ast.txt"
    with open(out_path, "w", encoding="utf-8") as outf:
        outf.write(pformat(ast, width=1000))
        outf.write("\n")

    print(f"\nAST saved to: {out_path}")
