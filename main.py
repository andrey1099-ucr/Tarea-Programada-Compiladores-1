import os
from pprint import pformat

from src.Parser import Parser
from src.cpp_transpiler import CppTranspiler

# Input Fangless Python source file
FILE = "./tests/test_transpile_basic.py"


if __name__ == "__main__":
    # Build parser (and its lexer)
    parser = Parser(debug=False)
    parser.build(build_lexer=True)

    # Read source file
    with open(FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # Parse to AST
    ast = parser.parse(data)

    # Report parser errors (if any) and stop before code generation
    print("\n=== ERRORS ===")
    print(len(parser.errors))
    for e in parser.errors:
        print(e)

    if parser.errors:
        # Do not attempt to transpile if the program has syntax errors
        raise SystemExit("Aborting: parser reported errors.")

    # Print AST to console
    print("=== AST ===")
    print(ast)

    # Save AST to a .txt file next to the input
    ast_out_path = os.path.splitext(FILE)[0] + ".ast.txt"
    with open(ast_out_path, "w", encoding="utf-8") as outf:
        outf.write(pformat(ast, width=1000))
        outf.write("\n")

    print(f"\nAST saved to: {ast_out_path}")

    # Transpile AST to C++ using the simple CppTranspiler
    transpiler = CppTranspiler()
    cpp_code = transpiler.transpile(ast)

    # Save generated C++ file next to the input, changing extension to .cpp
    cpp_out_path = os.path.splitext(FILE)[0] + ".cpp"
    with open(cpp_out_path, "w", encoding="utf-8") as cppf:
        cppf.write(cpp_code)

    print(f"C++ code saved to: {cpp_out_path}")
    print("You can compile it with something like:")
    print(f"  g++ -std=c++17 {cpp_out_path} -o program")
