import ply.yacc as yacc

from src.Lexer import Lexer
from src.utils import Error


class Parser:
    # Expose token list from the lexer
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
        self.lexer.input(data)
        return self._parser.parse(input=data, lexer=self.lexer, tracking=True)

    # Error handling
    def p_error(self, token):
        if token is None:
            self.errors.append(
                Error("Unexpected end of input", 0, 0, "parser", self.data)
            )
        else:
            self.errors.append(
                Error(
                    f"Syntax error on '{token.value}'",
                    token.lineno,
                    token.lexpos,
                    "parser",
                    self.data,
                )
            )

    # Program / logical lines
    def p_program(self, p):
        """program : stmt_lines_opt"""
        p[0] = ("program", p[1])

    def p_stmt_lines_opt(self, p):
        """stmt_lines_opt : stmt_lines
        | empty"""
        p[0] = p[1]  # list or []

    def p_stmt_lines(self, p):
        """stmt_lines : stmt_lines stmt_line
        | stmt_line"""
        if len(p) == 2:
            p[0] = p[1]  # stmt_line always returns a LIST
        else:
            p[1].extend(p[2])
            p[0] = p[1]

    # One statement per logical line (lexer maps ';' -> NEWLINE)
    def p_stmt_line(self, p):
        """stmt_line : simple_stmt NEWLINE
        | simple_stmt
        | compound_stmt
        | NEWLINE"""
        if len(p) == 2:
            # Either compound_stmt or empty NEWLINE
            if p.slice[1].type == "NEWLINE":
                p[0] = []
            else:
                p[0] = [p[1]]  # wrap node into list
        else:
            p[0] = [p[1]]

    # Simple statements
    def p_simple_stmt(self, p):
        """simple_stmt : assignment
        | return_stmt
        | pass_stmt
        | break_stmt
        | continue_stmt
        | expr_stmt"""
        p[0] = p[1]

    # assignment
    def p_assignment(self, p):
        """assignment : ID assign_op expression"""
        p[0] = ("assign", p[2], ("name", p[1]), p[3])

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

    def p_return_stmt(self, p):
        """return_stmt : RETURN
        | RETURN expression"""
        p[0] = ("return", None) if len(p) == 2 else ("return", p[2])

    def p_pass_stmt(self, p):
        """pass_stmt : PASS"""
        p[0] = ("pass",)

    def p_break_stmt(self, p):
        """break_stmt : BREAK"""
        p[0] = ("break",)

    def p_continue_stmt(self, p):
        """continue_stmt : CONTINUE"""
        p[0] = ("continue",)

    def p_expr_stmt(self, p):
        """expr_stmt : expression"""
        p[0] = p[1]

    # Compound statements (class / def / if / for / while)
    def p_compound_stmt(self, p):
        """compound_stmt : class_def_stmt
        | function_def_stmt
        | if_stmt
        | for_stmt
        | while_stmt"""
        p[0] = p[1]

    # class NAME: NEWLINE INDENT body DEDENT
    def p_class_def_stmt(self, p):
        """class_def_stmt : CLASS ID COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ("class", p[2], p[6])

    # def NAME '(' [params] ')' : NEWLINE INDENT body DEDENT
    def p_function_def_stmt(self, p):
        """function_def_stmt : DEF ID LPAREN opt_paramlist RPAREN COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ("def", ("name", p[2]), p[4], p[9])

    def p_opt_paramlist(self, p):
        """opt_paramlist : paramlist
        | empty"""
        p[0] = p[1]  # [] if empty

    def p_paramlist(self, p):
        """paramlist : ID
        | paramlist COMMA ID"""
        if len(p) == 2:
            p[0] = [("name", p[1])]
        else:
            p[1].append(("name", p[3]))
            p[0] = p[1]

    # if/elif/else
    def p_if_stmt(self, p):
        """if_stmt : IF condition COLON NEWLINE INDENT stmt_lines_opt DEDENT elif_list_opt else_opt"""
        p[0] = ("if", p[2], p[6], p[8], p[9])

    def p_elif_list_opt(self, p):
        """elif_list_opt : elif_list
        | empty"""
        p[0] = p[1]

    def p_elif_list(self, p):
        """elif_list : elif_list elif_clause
        | elif_clause"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[2])
            p[0] = p[1]

    def p_elif_clause(self, p):
        """elif_clause : ELIF condition COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ("elif", p[2], p[6])

    def p_else_opt(self, p):
        """else_opt : ELSE COLON NEWLINE INDENT stmt_lines_opt DEDENT
        | empty"""
        if len(p) == 2:
            p[0] = []  # empty
        else:
            p[0] = ("else", p[5])

    # for and while

    # for NAME in expression: NEWLINE INDENT body DEDENT
    def p_for_stmt(self, p):
        """for_stmt : FOR ID IN expression COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        # ('for', ('name', target), iterable_expr, body)
        p[0] = ("for", ("name", p[2]), p[4], p[8])

    # while condition: NEWLINE INDENT body DEDENT
    def p_while_stmt(self, p):
        """while_stmt : WHILE condition COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        # ('while', condition, body)
        p[0] = ("while", p[2], p[6])

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    # Expressions (OR > AND > NOT > primary)
    def p_expression(self, p):
        """expression : expression_or"""
        p[0] = p[1]

    def p_expression_or(self, p):
        """expression_or : expression_or OR expression_and
        | expression_and"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("or", p[1], p[3])

    def p_expression_and(self, p):
        """expression_and : expression_and AND expression_not
        | expression_not"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("and", p[1], p[3])

    # logical NOT sits above comparisons
    def p_expression_not(self, p):
        """expression_not : NOT expression_not
        | rel_expr"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("not", p[2])

    # Primary: calls, grouping, atoms
    def p_primary_call(self, p):
        """primary : ID LPAREN opt_arglist RPAREN"""
        p[0] = ("call", ("name", p[1]), p[3])

    def p_primary_group(self, p):
        """primary : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_primary_atom(self, p):
        """primary : atom"""
        p[0] = p[1]

    # Call arglist (positional only)
    def p_opt_arglist(self, p):
        """opt_arglist : arglist
        | empty"""
        p[0] = p[1]

    def p_arglist(self, p):
        """arglist : expression
        | arglist COMMA expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    # Atoms
    def p_atom_name(self, p):
        """atom : ID"""
        p[0] = ("name", p[1])

    def p_atom_number(self, p):
        """atom : INTEGER
        | FLOAT"""
        p[0] = ("num", p[1])

    def p_atom_string(self, p):
        """atom : STRING"""
        p[0] = ("str", p[1])

    def p_atom_bool(self, p):
        """atom : TRUE
        | FALSE"""
        p[0] = ("bool", True if p.slice[1].type == "TRUE" else False)

    # Arithmetic ( ** > unary +/- > *,/,//,% > +,- )

    # add/sub (left-assoc)
    def p_arith_add(self, p):
        """arith_add : arith_add ADD arith_mul
        | arith_add MINUS arith_mul
        | arith_mul"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            op = "+" if p.slice[2].type == "ADD" else "-"
            p[0] = (op, p[1], p[3])

    # mul/div/floordiv/mod (left-assoc)
    def p_arith_mul(self, p):
        """arith_mul : arith_mul TIMES arith_unary
        | arith_mul DIVIDE arith_unary
        | arith_mul FLOORDIV arith_unary
        | arith_mul MODULE arith_unary
        | arith_unary"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            t = p.slice[2].type
            op = {"TIMES": "*", "DIVIDE": "/", "FLOORDIV": "//", "MODULE": "%"}[t]
            p[0] = (op, p[1], p[3])

    # power (right-assoc) left side is a primary (no unary),
    # right side can include unary (like Python)
    def p_arith_pow(self, p):
        """arith_pow : arith_primary POWER arith_pow
        | arith_primary"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("**", p[1], p[3])

    # unary +/- bind tighter than mul/div but looser than power
    def p_arith_unary(self, p):
        """arith_unary : MINUS arith_unary
        | ADD arith_unary
        | arith_pow"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p.slice[1].type == "MINUS":
                p[0] = ("neg", p[2])  # unary minus
            else:
                p[0] = ("pos", p[2])  # unary plus

    # bridge to existing 'primary' (calls, grouping, atoms)
    def p_arith_primary(self, p):
        """arith_primary : primary"""
        p[0] = p[1]

    # Binary comparisons
    def p_rel_expr(self, p):
        """rel_expr : arith_add
        | arith_add EQUAL_EQUAL arith_add
        | arith_add NOT_EQUAL arith_add
        | arith_add LESS arith_add
        | arith_add GREATER arith_add
        | arith_add LESS_EQUAL arith_add
        | arith_add GREATER_EQUAL arith_add"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            op = {
                "EQUAL_EQUAL": "==",
                "NOT_EQUAL": "!=",
                "LESS": "<",
                "GREATER": ">",
                "LESS_EQUAL": "<=",
                "GREATER_EQUAL": ">=",
            }[p.slice[2].type]
            p[0] = ("cmp", op, p[1], p[3])

    # Utility
    def p_empty(self, p):
        """empty :"""
        p[0] = []
