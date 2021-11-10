import ply.lex as lex

reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'print' : 'PRINT',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'boolean' : 'BOOLEAN',
    'if' : 'IF',
    'else' : 'ELSE',
    'elif' : 'ELIF'
}

tokens = list(reserved.values()) + [
    'PLUS',
    'MINUS',
    'MULT',
    'DIVIDE',
    'EXP',
    'ASSIGN',
    'EQUAL',
    'NOTEQUAL',
    'GTHAN',
    'LTHAN',
    'GEQTHAN',
    'LEQTHAN',
    'INUM',
    'FNUM',
    'ID',
    'COLON',
    'LPTHESES',
    'RPTHESES',
    'LCURLY',
    'RCURLY'
]

# Regex
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GEQTHAN = r'>='
t_LEQTHAN = r'<='
t_ASSIGN = r'='
t_GTHAN = r'>'
t_LTHAN = r'<'
t_FNUM = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_INUM = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'\/'
t_EXP = r'\^'
t_COLON = r'\;'
t_LPTHESES = r'\('
t_RPTHESES = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print(f'Unexpected character {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

program = """
int a=3;
string b=4.5+6;
float c=4.5-6;
boolean d=4.5/6;

int e=4.5*6;

if(a>5){
    a>=5;
    a<5;
    a<=5;
    a==4;
    a!=4;
    a=5^2;
}
"""

lexer.input(program)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f'({tok.type}, {tok.value})')