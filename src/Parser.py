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

    # program
    def p_program(self, p):
        """program : stmt_lines_opt"""
        p[0] = ("program", p[1])

    def p_stmt_lines_opt(self, p):
        """stmt_lines_opt : stmt_lines
        | empty"""
        p[0] = p[1]  # either a list from stmt_lines or []

    def p_stmt_lines(self, p):
        """stmt_lines : stmt_lines stmt_line
        | stmt_line"""
        if len(p) == 2:
            p[0] = p[1]  # stmt_line always returns a LIST
        else:
            p[1].extend(p[2])
            p[0] = p[1]

    # One simple statement per logical line (NEWLINE). Lexer already splits on ';'
    def p_stmt_line(self, p):
        """stmt_line : simple_stmt NEWLINE"""
        p[0] = [p[1]]

    # EOF tolerance: allow the last line without a trailing NEWLINE
    def p_stmt_line_last(self, p):
        """stmt_line : simple_stmt"""
        p[0] = [p[1]]

    # Empty physical line: just a NEWLINE no statements for this line
    def p_stmt_line_empty(self, p):
        """stmt_line : NEWLINE"""
        p[0] = []

    # Simple statements
    
    def p_simple_stmt(self, p):
        """simple_stmt : assignment
        | return_stmt
        | pass_stmt
        | break_stmt
        | continue_stmt
        | expr_stmt"""
        p[0] = p[1]

    # assignment: ID op expression   (single-target for now)
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

    # return
    def p_return_stmt(self, p):
        """return_stmt : RETURN
        | RETURN expression"""
        p[0] = ("return", None) if len(p) == 2 else ("return", p[2])

    # pass
    def p_pass_stmt(self, p):
        """pass_stmt : PASS"""
        p[0] = ("pass",)

    # break / continue
    def p_break_stmt(self, p):
        """break_stmt : BREAK"""
        p[0] = ("break",)

    def p_continue_stmt(self, p):
        """continue_stmt : CONTINUE"""
        p[0] = ("continue",)

    # expression used as a statement (enables bare function calls as statements)
    def p_expr_stmt(self, p):
        """expr_stmt : expression"""
        p[0] = p[1]

    # Expressions (atoms + function calls + grouping)

    # Function call: ID '(' [args] ')'
    def p_function_call(self, p):
        """function_call : ID LPAREN opt_arglist RPAREN"""
        p[0] = ("call", ("name", p[1]), p[3])

    def p_opt_arglist(self, p):
        """opt_arglist : arglist
        | empty"""
        p[0] = p[1]  # empty returns []

    def p_arglist(self, p):
        """arglist : expression
        | arglist COMMA expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    # Compound Statements

    def p_compound_stmt(self, p):
        """compound_stmt : class_def_stmt
        | function_def_stmt
        | conditional_block_stmt
        | iterative_loop_stmt
        | conditional_loop_stmt"""
        p[0] = p[1]

    # Class definition
    def p_class_def_stmt(self, p):
        """class_def : CLASS ID COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ("class", p[2], p[6])

    # Function definition
    def p_function_def_stmt(self, p):
        """function_def_stmt : DEF ID LPAREN opt_arglist RPAREN COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ("function_def", ("name", p[2]), p[9])

    # Conditional block
    def p_conditional_block_stmt(self, p):
        """conditional_block_stmt : if_stmt
        | if_stmt elif_stmt_group
        | if_stmt elif_stmt_group else_stmt
        | if_stmt else_stmt"""

        # If statement
        if len(p) == 2:
            p[0] = ("conditional_block", p[1], [], None)
        #elif or else
        elif len(p) == 3:
            if isinstance(p[2], list):
                p[0] = ("conditional_block", p[1], p[2], None)
            else:
                p[0] = ("conditional_block", p[1], [], p[2])
        else:
            p[0] = ("conditional_block", p[1], p[2], p[3])
    
    # If statement
    def p_if_stmt(self, p):
        """if_stmt : IF if_elif_condition COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = p[1]

    # Elif statement group
    def p_elif_stmt_group(self, p):
        """elif_stmt_group : elif_stmt_group elif_stmt | elif_stmt"""
    
    # Elif statement
    def p_elif_stmt(self, p):
        """elif_stmt : ELIF if_elif_condition COLON NEWLINE INDENT stmt_lines_opt DEDENT """

    # Covers condition types for if and elif
    def p_if_elif_condition(self, p):
        """if_elif_condition : expression relation_op expression |
        expression"""

    def p_relation_op(self, p):
        """relation_op : EQUAL_EQUAL |
        NOT_EQUAL |
        LESS |
        GREATER |
        LESS_EQUAL |
        GREATER_EQUAL"""
        p[0] = p[1]

    # Negate expression
    def p_not_expression(self, p):
        """expression : NOT expression"""
        p[0] = ("not", p[2])


    # Grouping: Lowest to Highest priority

    def p_expression(self, p):
        """expression : expression_or"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("logical_op", "OR", p[1], p[3])

    def p_expression_or(self, p):
        """expression_or : expression_or OR expression_and
        | expression_and"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("logical_op", "OR", p[1], p[3])

    def p_expression_and(self, p):
        """expression_and : expression_and OR expression_not
        | expression_not"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("logical_op", "AND", p[1], p[3])

    def p_expression_and(self, p):
        """expression_not : NOT expression_not
        | expression_group
        | atom"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("logical_op", "NOT", p[2])
    
    def p_expression_group(self, p):
        """expression_group : LPAREN expression RPAREN"""
        p[0] = p[2]

    
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
    
    # Utility
    def p_empty(self, p):
        """empty :"""
        p[0] = []
