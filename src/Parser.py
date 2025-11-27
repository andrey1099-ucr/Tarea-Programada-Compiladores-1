import ply.yacc as yacc

from src.Lexer import Lexer
from src.utils import Error
from src.ast_nodes import (
    Program,
    ClassDef,
    FunctionDef,
    Param,
    Name,
    Constant,
    Assign,
    Return,
    Pass,
    Break,
    Continue,
    If,
    ElifClause,
    While,
    For,
    BinaryOp,
    UnaryOp,
    Call,
    Attribute,
    Index,
    ListLiteral,
    TupleLiteral,
    DictLiteral,
    KeyValue,
)


class Parser:
    # Expose token list from the lexer
    tokens = Lexer.tokens

    def __init__(self, debug: bool = False):
        self.errors = []
        self.data = None
        self.debug = debug
        self.lexer = Lexer(self.errors, debug=self.debug)
        self._parser = None

    def build(self, build_lexer: bool = True):
        if build_lexer:
            self.lexer.build()
        self._parser = yacc.yacc(module=self, start="program", debug=self.debug)

    def parse(self, data: str):
        self.data = data
        self.lexer.input(data)
        return self._parser.parse(input=data, lexer=self.lexer, tracking=True)

    # ---------- Error handling ----------

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

    # ---------- Program / logical lines ----------

    def p_program(self, p):
        """program : stmt_lines_opt"""
        p[0] = Program(body=p[1])

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

    # ---------- Simple statements ----------

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
        """assignment : primary assign_op expression"""
        p[0] = Assign(target=p[1], op=p[2], value=p[3])

    def p_assign_op(self, p):
        """assign_op : EQUAL
        | PLUS_EQUAL
        | MINUS_EQUAL
        | TIMES_EQUAL
        | DIVIDE_EQUAL
        | MODULE_EQUAL
        | FLOORDIV_EQUAL
        | POWER_EQUAL"""
        # Normalize '=' but keep compound assignment names
        p[0] = "=" if p.slice[1].type == "EQUAL" else p.slice[1].type

    def p_return_stmt(self, p):
        """return_stmt : RETURN
        | RETURN expression"""
        if len(p) == 2:
            p[0] = Return(None)
        else:
            p[0] = Return(p[2])

    def p_pass_stmt(self, p):
        """pass_stmt : PASS"""
        p[0] = Pass()

    def p_break_stmt(self, p):
        """break_stmt : BREAK"""
        p[0] = Break()

    def p_continue_stmt(self, p):
        """continue_stmt : CONTINUE"""
        p[0] = Continue()

    def p_expr_stmt(self, p):
        """expr_stmt : expression"""
        p[0] = p[1]

    # ---------- Compound statements (class / def / if / for / while) ----------

    def p_compound_stmt(self, p):
        """compound_stmt : class_def_stmt
        | function_def_stmt
        | if_stmt
        | for_stmt
        | while_stmt"""
        p[0] = p[1]

    # ---------- Class definitions (with optional inheritance) ----------

    # class A:
    def p_class_def_simple(self, p):
        """class_def_stmt : CLASS ID COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ClassDef(name=Name(p[2]), bases=[], body=p[6])

    # class B(A, C):
    def p_class_def_inheritance(self, p):
        """class_def_stmt : CLASS ID LPAREN base_list RPAREN COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = ClassDef(name=Name(p[2]), bases=p[4], body=p[9])

    def p_base_list_single(self, p):
        """base_list : ID"""
        p[0] = [Name(p[1])]

    def p_base_list_many(self, p):
        """base_list : base_list COMMA ID"""
        p[1].append(Name(p[3]))
        p[0] = p[1]

    # ---------- Function definitions (with optional/default params) ----------

    def p_function_def_stmt(self, p):
        """function_def_stmt : DEF ID LPAREN opt_paramlist RPAREN COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = FunctionDef(name=Name(p[2]), params=p[4], body=p[9])

    def p_opt_paramlist(self, p):
        """opt_paramlist : param_list
        | empty"""
        p[0] = p[1]  # [] if empty

    def p_param_list_single(self, p):
        """param_list : parameter"""
        p[0] = [p[1]]

    def p_param_list_many(self, p):
        """param_list : param_list COMMA parameter"""
        p[1].append(p[3])
        p[0] = p[1]

    # parameter can be "x" or "x = expression"
    def p_parameter_name(self, p):
        """parameter : ID"""
        p[0] = Param(name=Name(p[1]), default=None)

    def p_parameter_default(self, p):
        """parameter : ID EQUAL expression"""
        p[0] = Param(name=Name(p[1]), default=p[3])

    # ---------- if / elif / else ----------

    def p_if_stmt(self, p):
        """if_stmt : IF condition COLON NEWLINE INDENT stmt_lines_opt DEDENT elif_list_opt else_opt"""
        p[0] = If(condition=p[2], body=p[6], elifs=p[8], orelse=p[9])

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
        p[0] = ElifClause(condition=p[2], body=p[6])

    def p_else_opt(self, p):
        """else_opt : ELSE COLON NEWLINE INDENT stmt_lines_opt DEDENT
        | empty"""
        if len(p) == 2:
            p[0] = []  # no else body
        else:
            p[0] = p[5]

    # ---------- for and while ----------

    # for name in expression:
    def p_for_stmt(self, p):
        """for_stmt : FOR ID IN expression COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = For(target=Name(p[2]), iterable=p[4], body=p[8])

    # while condition:
    def p_while_stmt(self, p):
        """while_stmt : WHILE condition COLON NEWLINE INDENT stmt_lines_opt DEDENT"""
        p[0] = While(condition=p[2], body=p[6])

    # ---------- Conditions / relations ----------

    def p_condition_binary(self, p):
        """condition : expression relation_op expression"""
        p[0] = BinaryOp(op=p[2], left=p[1], right=p[3])

    def p_condition_expr(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_relation_op(self, p):
        """relation_op : EQUAL_EQUAL
        | NOT_EQUAL
        | LESS
        | GREATER
        | LESS_EQUAL
        | GREATER_EQUAL"""
        p[0] = p.slice[1].type

    # ---------- Expressions ----------

    def p_expression(self, p):
        """expression : expression_or"""
        p[0] = p[1]

    def p_expression_or(self, p):
        """expression_or : expression_or OR expression_and
        | expression_and"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(op="OR", left=p[1], right=p[3])

    def p_expression_and(self, p):
        """expression_and : expression_and AND expression_not
        | expression_not"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(op="AND", left=p[1], right=p[3])

    def p_expression_not(self, p):
        """expression_not : NOT expression_not
        | expression_cmp"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = UnaryOp(op="NOT", operand=p[2])

    # Allows comparisons inside arithmetic expressions
    def p_expression_cmp(self, p):
        """expression_cmp : expression_add_sub relation_op expression_add_sub
        | expression_add_sub"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(op=p[2], left=p[1], right=p[3])

    # ---------- Arithmetic expression levels ----------

    def p_expression_add_sub(self, p):
        """expression_add_sub : expression_add_sub ADD expression_ops
        | expression_add_sub MINUS expression_ops
        | expression_ops"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            op = p.slice[2].type  # ADD or MINUS
            p[0] = BinaryOp(op=op, left=p[1], right=p[3])

    def p_expression_ops(self, p):
        """expression_ops : expression_ops TIMES expression_power
        | expression_ops DIVIDE expression_power
        | expression_ops FLOORDIV expression_power
        | expression_ops MODULE expression_power
        | expression_power"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            op = p.slice[2].type  # TIMES, DIVIDE, etc.
            p[0] = BinaryOp(op=op, left=p[1], right=p[3])

    def p_expression_power(self, p):
        """expression_power : expression_power POWER primary
                            | MINUS expression_power
                            | primary"""
        if len(p) == 2:
            # Primary
            p[0] = p[1]

        elif len(p) == 3 and p.slice[1].type == "MINUS":
            # MINUS expression_power
            p[0] = UnaryOp(op="NEG", operand=p[2])

        else:
            # Expression_power POWER primary
            op = p.slice[2].type  # POWER
            p[0] = BinaryOp(op=op, left=p[1], right=p[3])


    # ---------- Primaries: calls, attributes, indexing, atoms ----------

    def p_primary_call(self, p):
        """primary : primary LPAREN opt_arglist RPAREN"""
        p[0] = Call(func=p[1], args=p[3])

    def p_primary_attribute(self, p):
        """primary : primary DOT ID"""
        p[0] = Attribute(value=p[1], attr=Name(p[3]))

    def p_primary_index(self, p):
        """primary : primary LBRACKET expression RBRACKET"""
        p[0] = Index(value=p[1], index=p[3])

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

    # ---------- List literals ----------

    def p_list(self, p):
        """atom : LBRACKET opt_list_cont RBRACKET"""
        p[0] = ListLiteral(elements=p[2])

    def p_opt_list_cont(self, p):
        """opt_list_cont : list_cont
        | empty"""
        p[0] = p[1]

    def p_list_cont(self, p):
        """list_cont : expression
        | list_cont COMMA expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    # ---------- Tuple literals and grouped expressions ----------

    def p_atom_group(self, p):
        """atom : LPAREN expression RPAREN"""
        # Parenthesized expression, not a tuple.
        p[0] = p[2]

    def p_atom_tuple(self, p):
        """atom : LPAREN expression COMMA opt_tuple_cont RPAREN"""
        # (a, b, c) or (a,) -> tuple literal
        elements = [p[2]] + p[4]
        p[0] = TupleLiteral(elements=elements)

    def p_opt_tuple_cont(self, p):
        """opt_tuple_cont : tuple_cont
        | empty"""
        p[0] = p[1]

    def p_tuple_cont(self, p):
        """tuple_cont : expression
        | tuple_cont COMMA expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    # ---------- Dictionary literals ----------

    def p_dictionary(self, p):
        """atom : LBRACE opt_dict_cont RBRACE"""
        p[0] = DictLiteral(pairs=p[2])

    def p_opt_dict_cont(self, p):
        """opt_dict_cont : dict_cont
        | empty"""
        p[0] = p[1]

    def p_dict_cont(self, p):
        """dict_cont : keyvalue
        | dict_cont COMMA keyvalue"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_keyvalue(self, p):
        """keyvalue : expression COLON expression"""
        p[0] = KeyValue(key=p[1], value=p[3])

    # ---------- Atoms ----------

    def p_atom_name(self, p):
        """atom : ID"""
        p[0] = Name(p[1])

    def p_atom_number(self, p):
        """atom : INTEGER
        | FLOAT"""
        p[0] = Constant(p[1])

    def p_atom_string(self, p):
        """atom : STRING"""
        p[0] = Constant(p[1])

    def p_atom_bool(self, p):
        """atom : TRUE
        | FALSE"""
        value = True if p.slice[1].type == "TRUE" else False
        p[0] = Constant(value)

    # ---------- Utility ----------

    def p_empty(self, p):
        """empty :"""
        p[0] = []
