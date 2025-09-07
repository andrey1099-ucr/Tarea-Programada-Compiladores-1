import ply.lex as lex

from src.utils import Error


class Lexer:
    def __init__(self, errors: list[Error], debug: bool = False):
        self.lex = None
        self.data = None
        self.debug = debug
        self.errors = errors

        # keyword map
        self.reserved_map = {
            "if": "IF",
            "else": "ELSE",
            "elif": "ELIF",
            "while": "WHILE",
            "for": "FOR",
            "break": "BREAK",
            "continue": "CONTINUE",
            "pass": "PASS",
            "def": "DEF",
            "return": "RETURN",
            "class": "CLASS",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
            "True": "TRUE",
            "False": "FALSE",
        }

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

    literal_tokens = ("INTEGER", "FLOAT", "STRING")

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
    tokens = (
        (identifier,)
        + reserved
        + literal_tokens
        + operators
        + delimiters_and_symbols
        + indentation
    )

    # Regex rules for tokens

    # Ignore spaces and tabs
    t_ignore = " \t\f\r"

    # Arithmetic
    t_POWER = r"\*\*"
    t_FLOORDIV = r"//"
    t_ADD = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_MODULE = r"%"

    # Relational
    t_EQUAL_EQUAL = r"=="
    t_NOT_EQUAL = r"!="
    t_LESS_EQUAL = r"<="
    t_GREATER_EQUAL = r">="
    t_LESS = r"<"
    t_GREATER = r">"

    # Assignment
    t_POWER_EQUAL = r"\*\*="
    t_FLOORDIV_EQUAL = r"//="
    t_PLUS_EQUAL = r"\+="
    t_MINUS_EQUAL = r"-="
    t_TIMES_EQUAL = r"\*="
    t_DIVIDE_EQUAL = r"/="
    t_MODULE_EQUAL = r"%="
    t_EQUAL = r"="

    # Delimiters & symbols
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_COLON = r":"
    t_COMMA = r","
    t_DOT = r"\."

    # Rules with some action

    def t_FLOAT(self, t):
        r"\d+\.\d+"
        t.type = "FLOAT"
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r"\d+"
        t.type = "INTEGER"
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r"[A-Za-z_][A-Za-z0-9_]*"
        t.type = self.reserved_map.get(t.value, self.identifier)  # keyword or ID
        if self.debug:
            print(f"DEBUG: {t.type}({t.value}) @ line {t.lineno}, pos {t.lexpos}")
        return t

    def t_STRING(self, t):
        r"(\"([^\\\n]|\\.)*?\"|'([^\\\n]|\\.)*?')"
        t.type = "STRING"
        return t

    # Ignore single-line comments
    def t_COMMENT(self, t):
        r"\#[^\n]*"
        pass

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        t.type = "NEWLINE"
        t.value = "\n"
        return t

    def t_error(self, t):
        self.errors.append(
            Error(
                f"Illegal character {repr(t.value[0])}",
                t.lineno,
                t.lexpos,
                "lexer",
                self.data,
            )
        )
        if self.debug:
            print(self.errors[-1])
        t.lexer.skip(1)

    # Build PLY lexer from this instance (uses t_* rules)
    def build(self, **kwargs):
        self.lex = lex.lex(module=self, reflags=0, **kwargs)

    # Load source text and reset the scanner
    def input(self, data: str):
        self.data = data
        self.lex.input(data)

    # Return next token or None on EOF
    def token(self):
        return self.lex.token()
