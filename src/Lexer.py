import ply.lex as lex


from src.utils import Error
class Lexer:
    def __init__(self, errors: list[Error], debug=False):
        self.lex = None
        self.data = None
        self.debug = debug
        self.reserved_map = {}
        self.errors = errors  # to use the same list of errors that the parser uses
        for r in self.reserved:
            self.reserved_map[r.lower()] = r

    # Python's reserved words
    reserved = (
        "IF",
        "ELSE",
        "ELIF",
        "WHILE",
        "FOR",
        "BREAK",
        "CONTINUE",
        "PASS",
        "DEF",
        "RETURN",
        "CLASS",
        "TRUE",
        "FALSE",
        "AND",
        "OR",
        "NOT",
    )

    # Token for variables,functions and class names
    identifier = "ID"

    literals = (
        "INTEGER",
        "FLOAT",
        "STRING"
    )

    operators = (
        # Arithmetic Operators
        "ADD",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "FLOORDIV",
        "MODULE",
        "POWER",
        # Relation Operators
        "EQUAL_EQUAL",
        "NOT_EQUAL",
        "LESS",
        "GREATER",
        "LESS_EQUAL",
        "GREATER_EQUAL",
        # Assignment Operators
        "EQUAL",
        "PLUS_EQUAL",
        "MINUS_EQUAL",
        "TIMES_EQUAL",
        "DIVIDE_EQUAL",
        "MODULE_EQUAL",
        "FLOORDIV_EQUAL",
        "POWER_EQUAL",
    )

    delimiters_and_symbols = (
        "LPAREN",
        "RPAREN",
        "LBRACKET",
        "RBRACKET",
        "LBRACE",
        "RBRACE",
        "COLON",
        "COMMA",
        "DOT",
    )

    indentation = ("INDENT", "DEDENT", "NEWLINE")

    # All tokens
    tokens = reserved + literals + operators + delimiters_and_symbols + indentation
    
    # Regular expression rules for simple tokens
    
    # Ignore spaces and tabs
    t_ignore = "\t"

    t_ADD = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_FLOORDIV = r"//"
    t_MODULE = r"%"
    t_POWER = r"\*\*"

    t_EQUAL_EQUAL = r"=="
    t_NOT_EQUAL = r"!="
    t_LESS = r"<"
    t_GREATER = r">"
    t_LESS_EQUAL = r"<="
    t_GREATER_EQUAL = r'>='

    t_EQUAL = r'='
    t_PLUS_EQUAL = r'\+='
    t_MINUS_EQUAL = r'-='
    t_TIMES_EQUAL = r'\*='
    t_DIVIDE_EQUAL = r'/='
    t_MODULE_EQUAL = r'%='
    t_FLOORDIV_EQUAL = r'//='
    t_POWER_EQUAL = r'\*\*='

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'\.'

    # Functions for tokens
    def t_COMMENT(self, t):
        r"\#[^\n]*"
        pass
