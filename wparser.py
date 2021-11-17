from typing import Counter
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

def p_program(p):
    '''program : stmntwrap
                | block
                | while
                | for
                | '''

def p_stmntwrap(p):
    '''stmntwrap : statement COLON'''

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

def p_statement_declare_string(p):
    '''statement : STRING ID is_assing
    '''
    names[p[2]] = {"type": "STRING", "value": p[3]}

def p_statement_declare_boolean(p):
    '''statement : BOOLEAN ID is_assing
    '''
    names[p[2]] = {"type": "BOOLEAN", "value": p[3]}

def p_block(p):
    '''block : ifblock '''

def p_ifblock(p):
    '''ifblock : IF LPTHESES condition RPTHESES LCURLY program RCURLY ifcont'''


def p_ifcont(p):
    '''ifcont : elifblock ifcont 
                | elseblock 
                | '''

def p_elseblock(p):
    '''elseblock : ELSE LCURLY program RCURLY'''

def p_elifblock(p):
    '''elifblock : ELIF LPTHESES condition RPTHESES LCURLY program RCURLY ifcont'''

def p_while(p):
    '''while : WHILE LPTHESES condition RPTHESES LCURLY program RCURLY'''

def p_for(p):
    '''for : FOR LPTHESES stmntwrap condition COLON expression RPTHESES LCURLY program RCURLY'''

def p_condition(p):
    '''condition : BOOLVAL appendcond
                | comparison appendcond'''

def p_appendcond(p):
    '''appendcond : AND condition
                    | OR condition
                    | '''

def p_comparison(p):
    '''comparison : expression EQUAL expression
                    | expression NOTEQUAL expression
                    | expression GTHAN expression
                    | expression LTHAN expression
                    | expression GEQTHAN expression
                    | expression LEQTHAN expression'''

    first = p[1]
    second = p[3]

    if(p[2] == '=='):
        p[0] = (first == second)
    elif(p[2] == '!='):
        p[0] = (first != second)
    elif(p[2] == '>'):
        p[0] = (first > second)
    elif(p[2] == '<'):
        p[0] = (first < second)
    elif(p[2] == '>='):
        p[0] = (first >= second)
    elif(p[2] == '<='):
        p[0] = (first <= second)

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

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression
                  | expression EXP expression'''

    type_first = type(p[1]).__name__
    type_second = type(p[3]).__name__
    both = Counter([type_first, type_second])

    if(both == Counter(['int', 'int']) 
        or both == Counter(['int', 'float']) 
        or both == Counter(['float', 'float'])):

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
    
    elif(both == Counter(['str', 'str'])):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        else:
            print(f'Cannot apply operation \'{p[2]}\' on strings.')
    
    elif(both == Counter(['str', 'int'])
        or both == Counter(['str', 'float'])):
        if p[2] == '+':
            p[0] = str(p[1]) + str(p[3])
        else:
            print(f'Cannot apply operation \'{p[2]}\' between \'{type_first}\' and \'{type_second}\'')
    else:
        print(f'Cannot apply operation \'{p[2]}\' between \'{type_first}\' and \'{type_second}\'')
    

    

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

def p_expression_boolean(p):
    '''expression : BOOLVAL
    '''
    p[0] = p[1]

def p_expression_strval(p):
    '''expression : STRVAL'''
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