import ply.lex as lex


class Lexer:

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

    literals = ("INTEGER", "FLOAT", "STRING")

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
