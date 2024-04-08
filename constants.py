import math
import string

# Strings

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

# Tokens

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_MOD = 'MOD'
TT_EQ = 'EQ'
TT_NEWLINE = 'NEWLINE'
TT_LBRACE = 'LBRACE'
TT_RBRACE = 'RBRACE'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_COLON = 'COLON'
TT_EOF = 'EOF'

KEYWORDS = [
    'var', 'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'to', 'step',
    'while', 'func', 'return', 'continue', 'break'
]
