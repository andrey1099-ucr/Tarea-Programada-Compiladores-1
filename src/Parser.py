import ply.yacc as yacc

from src.Lexer import Lexer
from src.utils import Error

class Parser:
    # Reuse tokens defined by the lexer
    tokens = Lexer.tokens

    def __init__(self, debug=False):
        self.errors = []
        self.data = None
        self.debug = debug
        # Dedicated lexer instance (shares the same error list)
        self.lexer = Lexer(self.errors, debug=self.debug)
        self.parser = None

    def build(self, build_lexer=True):
        if build_lexer:
            self.lexer.build()
        # Explicit start symbol
        self.parser = yacc.yacc(module=self, start="module", debug=self.debug)

    def parse(self, data):
        self.data = data
        # Feed the same input to the underlying PLY lexer object
        self.lexer.input(data)
        # Parse using the same lexer
        return self.parser.parse(input=data, lexer=self.lexer.lex, tracking=True)

    # Error handling
    def p_error(self, p):
        if not p:
            self.errors.append(
                Error("Unexpected end of input", 0, 0, "parser", self.data)
            )
        else:
            self.errors.append(
                Error(
                    f"Syntax error on '{p.value}'",
                    p.lineno,
                    p.lexpos,
                    "parser",
                    self.data,
                )
            )
