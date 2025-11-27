 # Programmed Task — Compilers 1
 
 This project implements the a simple transpiler for a restricted subset of Python called **“Fangless Python.”**  
 The pipeline is:
 
 - **Lexical analysis (lexer)** with **PLY**, including indentation handling (`INDENT`/`DEDENT`), skipping single-line comments, validating basic string escape sequences, and robust lexical error reporting.
 - **Syntactic analysis (parser)** that builds an **AST** (see `ast_nodes.py`) for constructs such as functions, classes (structure only), `if`/`elif`/`else`, `while`, `for`, expressions, and container literals.
 - **C++ transpiler** (`cpp_transpiler.py`) that walks the AST and generates **C++17** code.
 - A small **runtime** in C++ (`runtime.hpp`) that provides dynamic values (`PyValue`), basic arithmetic and comparisons, dynamic containers (list, dict, tuple, set), and helpers like `py_print`, `py_len`, `py_getitem`, etc.
 
 The generated C++ code can then be compiled and executed to run Fangless Python programs, and is used to compare performance against the original Python version and a hand-written C++ implementation for some benchmarks (e.g., Fibonacci, bubble sort).
 
 ---
 
 ## 1. Create virtual environment
 
 ```bash
 py -m venv venv
 ```
 
 ## 2. Activate virtual environment
 
 ```bash
 venv\Scripts\activate
 ```
 
 You should see the environment name `(venv)` at the beginning of the command prompt.
 
 ## 3. Install required libraries
 
 Inside the active environment:
 
 ```bash
 pip install -r requirements.txt
 ```
 
 This will install **PLY** and any other dependencies needed by the lexer, parser and transpiler.
 
 ---
 
 ## Running the project (overview)
 
 The entry point is `main.py`, which:
 
 - Invokes the **lexer** and **parser** to build the AST for a Fangless Python input.
 - Uses the **CppTranspiler** to generate a `.cpp` file that includes `runtime.hpp`.
 - (Optionally) runs some performance experiments with Python vs generated C++ vs hand-written C++.
 
 Typical usage from the virtual environment:
 
 ```bash
 python main.py
 ```
 
 The exact input program and output paths can be adjusted inside `main.py` (for example, to test bubble sort, recursive Fibonacci, matrix traversal, etc.).
 
 ---
 
 ## Deactivate virtual environment
 
 When you finish working:
 
 ```bash
 deactivate
 ```
 
 ---
 
 ## Best practices
 
 Generate an updated `requirements.txt` after installing new libraries:
 
 ```bash
 pip freeze > requirements.txt
 ```
 
 This keeps the environment reproducible for the lexer/parser/transpiler and any tools you add later.
 
 ---
 
 ## Useful commands
 
 ### View packages installed in the environment
 
 ```bash
 pip list
 ```
 
 ### Check Python and pip versions
 
 ```bash
 python --version
 pip --version
 ```
