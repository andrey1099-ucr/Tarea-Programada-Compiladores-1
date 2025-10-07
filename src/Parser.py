import ply.yacc as yacc

from src.Lexer import Lexer
from src.utils import Error

class Parser:
    # Expose the token list from the lexer
    tokens = Lexer.tokens

    def __init__(self, debug=False):
        self.errors = []
        self.data = None
        self.debug = debug
        self.lexer = Lexer(self.errors, debug=self.debug)
        self._parser = None

    def build(self, build_lexer=True):
        if build_lexer:
            self.lexer.build()
        self._parser = yacc.yacc(module=self, start="program", debug=self.debug)

    def parse(self, data):
        self.data = data
        self.lexer.input(data)  # feed text to PLY's internal lexer
        return self._parser.parse(input=data, lexer=self.lexer, tracking=True)

    # Error handling
    def p_error(self, token):
        if token is None:
            self.errors.append(Error("Unexpected end of input", 0, 0, "parser", self.data))
        else:
            self.errors.append(
                Error(f"Syntax error on '{token.value}'", token.lineno, token.lexpos, "parser", self.data)
            )

        # Grammar

    # zero-or-more lines of assignments
    def p_program(self, p):
        """program : stmt_lines_opt"""
        p[0] = ("program", p[1])

    def p_stmt_lines_opt(self, p):
        """stmt_lines_opt : stmt_lines
        | empty"""
        p[0] = p[1]

    def p_stmt_lines(self, p):
        """stmt_lines : stmt_lines stmt_line
        | stmt_line"""
        if len(p) == 2:
            p[0] = p[1]  # stmt_line always returns a list
        else:
            p[1].extend(p[2])
            p[0] = p[1]

    # One statement per logical line (NEWLINE). Lexer turns ';' into NEWLINE.
    def p_stmt_line(self, p):
        """stmt_line : assignment NEWLINE"""
        p[0] = [p[1]]

    # EOF tolerance: last line without trailing NEWLINE
    def p_stmt_line_last_single(self, p):
        """stmt_line : assignment"""
        p[0] = [p[1]]

    # Empty line (just a NEWLINE) -> no statements for this line
    def p_stmt_line_empty(self, p):
        """stmt_line : NEWLINE"""
        p[0] = []

    # Assignment
    def p_assignment(self, p):
        """assignment : ID assign_op expression"""
        target = ("name", p[1])
        op = p[2]
        rhs = p[3]
        p[0] = ("assign", op, [target], rhs)

    def p_assign_op(self, p):
        """assign_op : EQUAL
        | PLUS_EQUAL
        | MINUS_EQUAL
        | TIMES_EQUAL
        | DIVIDE_EQUAL
        | MODULE_EQUAL
        | FLOORDIV_EQUAL
        | POWER_EQUAL"""
        p[0] = "=" if p.slice[1].type == "EQUAL" else p.slice[1].type

    # Expressions
    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_name(self, p):
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

    def p_empty(self, p):
        """empty :"""
        p[0] = []
