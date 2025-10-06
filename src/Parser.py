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

        # Grammar

    # module : zero or more statement lines
    def p_module(self, p):
        """module : stmt_lines_opt"""
        body = p[1] if p[1] is not None else []
        p[0] = ("module", body)

    def p_stmt_lines_opt(self, p):
        """stmt_lines_opt : stmt_lines
        | empty"""
        p[0] = p[1] if len(p) == 2 else []

    def p_stmt_lines(self, p):
        """stmt_lines : stmt_lines stmt_line
        | stmt_line"""
        if len(p) == 2:
            # stmt_line may return a single stmt or a list of stmts
            p[0] = p[1] if isinstance(p[1], list) else [p[1]]
        else:
            seq = p[1]
            if isinstance(p[2], list):
                seq.extend(p[2])
            else:
                seq.append(p[2])
            p[0] = seq

    # A statement line always ends with a NEWLINE.
    # It can be a single assignment, or a SEMI-separated list of assignments.
    def p_stmt_line(self, p):
        """stmt_line : assignment NEWLINE
        | assign_list NEWLINE"""
        p[0] = p[1]

    def p_assign_list(self, p):
        """assign_list : assignment
        | assign_list SEMI assignment"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    # Assignments (simple and augmented)
    def p_assignment(self, p):
        """assignment : ID EQUAL expression
        | ID PLUS_EQUAL expression
        | ID MINUS_EQUAL expression
        | ID TIMES_EQUAL expression
        | ID DIVIDE_EQUAL expression
        | ID MODULE_EQUAL expression
        | ID FLOORDIV_EQUAL expression
        | ID POWER_EQUAL expression"""
        target = ("name", p[1])
        if p.slice[2].type == "EQUAL":
            op = "="
        else:
            op = p.slice[2].type  # e.g., 'PLUS_EQUAL', 'POWER_EQUAL', etc.
        p[0] = ("assign", op, [target], p[3])

    # Minimal expressions to serve as RHS for assignments

    # Parenthesized expression
    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    # Atoms as expressions (keep it minimal for this branch)
    def p_expression_id(self, p):
        """expression : ID"""
        p[0] = ("name", p[1])

    def p_expression_number(self, p):
        """expression : INTEGER
        | FLOAT"""
        p[0] = ("num", p[1])

    def p_expression_string(self, p):
        """expression : STRING"""
        p[0] = ("str", p[1])

    def p_expression_bool(self, p):
        """expression : TRUE
        | FALSE"""
        p[0] = ("bool", True if p.slice[1].type == "TRUE" else False)

    # empty production
    def p_empty(self, p):
        """empty :"""
        p[0] = None
