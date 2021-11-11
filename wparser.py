from wlexer import tokens
import argparse
import ply.yacc as yacc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
abstractTree = []

def p_statement_declare_int(p):
    '''statement : INT ID is_assing
    '''
    if type(p[3]) == float:
        print('No pudes asignar flotantes a enteros')
    else:
        names[p[2]] = { "type": "INT", "value":p[3]}

def p_statement_declare_float(p):
    'statement : FLOAT ID is_assing'
    names[p[2]] = { "type": "FLOAT", "value":p[3]}

def p_is_assing(p):
    '''is_assing : ASSIGN expression 
                | '''
    p[0] = 0
    if len(p) > 2:
        p[0] = p[2]

def p_statement_print(p):
    '''statement : PRINT LPTHESES expression RPTHESES '''
    print(p[3])

def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]


# def p_statement_expr(p):
#     'statement : expression'
#     # print(p[1])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression
                  | expression EXP expression'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
            p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1]**p[3]
    

def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : LPTHESES expression RPTHESES"
    p[0] = p[2]


def p_expression_inumber(p):
    "expression : INUM"
    p[0] = p[1]


def p_expression_fnumber(p):
    "expression : FNUM"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]["value"]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
argparser = argparse.ArgumentParser()
argparser.add_argument('-f', '--file')
args = argparser.parse_args()

if(args.file):
    try:

        file = args.file
        source = open(file, 'r')
        lines = source.readlines()
        source.close()

        for line in lines:
            yacc.parse(line)
    except(FileNotFoundError):
        print('El archivo no existe.')
        
else:
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        yacc.parse(s)