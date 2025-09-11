import ply.lex as lex
import re

from src.utils import Error


class Lexer:
    def __init__(self, errors: list[Error], debug: bool = False):
        self.lex = None
        self.data = None
        self.debug = debug
        self.errors = errors
        self.indent_stack = [0]
        self.pending_tokens = []
        self.indent_size = 4
        self.may_indent = False
        self.bracket_level = 0

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
            "in": "IN",
            "range": "RANGE",
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
        "IN",
        "RANGE",
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
    t_ignore = " \t"

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
        # Validate allowed escapes: \n, \t, \\, \", \'
        self.validate_string_escapes(t)
        t.type = "STRING"
        return t

    # Ignore single-line comments
    def t_COMMENT(self, t):
        r"\#[^\n]*"
        pass

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        must_indent = False
        
        if self.bracket_level > 0:
            return None

        newline_token = self.make_token("NEWLINE", "\n", t.lexer.lineno, t.lexpos)
        if self.may_indent == True:
            must_indent = True

        # Count spaces in next line:
        remaining = t.lexer.lexdata[t.lexer.lexpos :]
        match = re.match(r"[ ]*", remaining)
        spaces = len(match.group(0)) if match else 0
        last_level = self.indent_stack[-1]
        next_char = remaining[spaces : spaces + 1]

        # Checks to ensure next line is not empty or a comment to proceed
        if next_char in {"", "\n", "#"}:
            return None

        # Adds indentation level
        if spaces > last_level:
            if must_indent:
                self.indent_stack.append(spaces)
                # Adds to pending stack
                indent_token = self.make_token("INDENT", "", t.lexer.lineno, t.lexpos)
                self.pending_tokens.append(indent_token)
            # Indentation error
            else:
                self.errors.append(
                    Error(
                        "BAD_INDENT: indent does not match any previous indentation level",
                        t.lexer.lineno,
                        t.lexer.lexpos + spaces,
                        "lexer",
                        self.data,
                    )
                )
        elif spaces < last_level:
            # Produces and returns multiple dedent tokens if needed
            while self.indent_stack and spaces < self.indent_stack[-1]:
                self.indent_stack.pop()
                # Adds to pending stack
                dedent_token = self.make_token(
                    "DEDENT", "", t.lexer.lineno, t.lexpos)
                self.pending_tokens.append(dedent_token)
            # Dedent error:
            if spaces != self.indent_stack[-1]:
                self.errors.append(
                    Error(
                        "BAD_DEDENT: dedent does not match any previous indentation level",
                        t.lexer.lineno,
                        t.lexer.lexpos + spaces,
                        "lexer",
                        self.data,
                    )
                )
        # Reset may indent
        self.may_indent = False
        return newline_token

    # Aux function to manually create tokens
    def make_token(self, type, value, lineno, lexpos):
        t = lex.LexToken()
        t.type = type
        t.value = value
        t.lineno = lineno
        t.lexpos = lexpos
        return t

    def handle_remaining_dedents(self):
        # Dedents at eof:
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            # Adds to pending stack
            dedent_token = self.make_token(
                "DEDENT", "", self.lex.lineno, self.lex.lexpos)
            self.pending_tokens.append(dedent_token)

        # Return all dedents:
        if self.pending_tokens:
            return self.pending_tokens.pop(0)

        return None

    # Report invalid escape sequences inside a string literal.
    def validate_string_escapes(self, t):
        allowed_escapes = {"n", "t", "\\", '"', "'"}
        literal = t.value  # full literal including quotes
        index = 1  # start after opening quote
        closing_index = len(literal) - 1  # position of the closing quote

        while index < closing_index:
            if literal[index] == "\\":
                # Backslash at the very end before the closing quote -> invalid
                if index + 1 >= closing_index:
                    self.errors.append(
                        Error(
                            "Invalid escape sequence: trailing backslash in string",
                            t.lineno,
                            t.lexpos + index,
                            "lexer",
                            self.data,
                        )
                    )
                    break

                next_char = literal[index + 1]
                if next_char not in allowed_escapes:
                    self.errors.append(
                        Error(
                            f"Invalid escape sequence \\{next_char}",
                            t.lineno,
                            t.lexpos + index,
                            "lexer",
                            self.data,
                        )
                    )
                index += 2  # skip backslash + escaped char
            else:
                index += 1

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
        # Return pending token if needed
        if self.pending_tokens:
            return self.pending_tokens.pop(0)

        t = self.lex.token()
        # indentation check
        if t:
            if t.type in {"LPAREN", "LBRACKET", "LBRACE"}:
                self.bracket_level += 1
            elif t.type in {"RPAREN", "RBRACKET", "RBRACE"}:
                if self.bracket_level > 0:
                    self.bracket_level -= 1
                    
            if t.type == "COLON" and self.bracket_level == 0:
                self.may_indent = True
            else:
                self.may_indent = False
        else:
            return self.handle_remaining_dedents()
        return t
