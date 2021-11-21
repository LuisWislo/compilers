from typing import Counter
from wlexer import tokens
import argparse
import ply.yacc as yacc
from wtree import AbstractSyntaxTree, Node

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
ast = AbstractSyntaxTree()

def p_start(p):
    '''start : program'''
    if(p[1]):
        ast.root = p[1]
        ast.root.token_id = 'START'
        ast.root.value = 'START'

def p_program(p):
    '''program : stmntwrap program
                | block program
                | while program
                | for program
                | '''
    if(len(p) > 1):
        prog = Node('CONNECT', 'program')
        #merge here
        prog.add_child(p[1])
        if(p[2]):
            prog.add_child(p[2])
        p[0] = prog

def p_stmntwrap(p):
    '''stmntwrap : statement COLON'''
    p[0] = p[1]

def p_statement_declare_int(p):
    '''statement : INT ID is_assing
    '''
    p[0] = help_declaration('INT', p)
    

def p_statement_declare_float(p):
    'statement : FLOAT ID is_assing'
    p[0] = help_declaration('FLOAT', p)

def p_statement_declare_string(p):
    '''statement : STRING ID is_assing
    '''
    p[0] = help_declaration('STRING', p)

def p_statement_declare_boolean(p):
    '''statement : BOOLEAN ID is_assing
    '''
    p[0] = help_declaration('BOOLEAN', p)

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
    p[0] = None
    if len(p) > 2:
        assign = Node('ASSIGN', '=')
        assign.add_child(p[2])
        p[0] = assign
    

def p_statement_print(p):
    '''statement : PRINT LPTHESES expression RPTHESES '''
    prnt = Node('PRINT', p[1])
    prnt.add_child(p[3])
    p[0] = prnt

def p_statement_assign(p):
    '''statement : ID ASSIGN expression'''
    assign = Node('ASSIGN', p[2])
    id = Node('ID', p[1])
    expression = p[3]

    assign.add_child(id)
    assign.add_child(expression)

    p[0] = assign

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression
                  | expression EXP expression'''
    
    operand = None

    if p[2] == '+':
        operand = Node('PLUS', p[2])
    elif p[2] == '-':
        operand = Node('MINUS', p[2])
    elif p[2] == '*':
        operand = Node('MULT', p[2])
    elif p[2] == '/':
        operand = Node('DIVIDE', p[2])
    elif p[2] == '^':
        operand = Node('EXP', p[2])

    operand.add_child(p[1])
    operand.add_child(p[3])
    p[0] = operand

def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    mult = Node('MULT', '*')
    mult.add_child(Node('INUM', -1))
    mult.add_child(p[2])
    p[0] = mult


def p_expression_group(p):
    "expression : LPTHESES expression RPTHESES"
    p[0] = p[2]


def p_expression_inumber(p):
    '''expression : INUM'''
    p[0] = Node('INUM', p[1])


def p_expression_fnumber(p):
    '''expression : FNUM'''
    p[0] = Node('FNUM', p[1])

def p_expression_boolean(p):
    '''expression : BOOLVAL'''
    p[0] = Node('BOOLVAL', p[1])

def p_expression_strval(p):
    '''expression : STRVAL'''
    p[0] = Node('STRVAL', p[1])

def p_expression_name(p):
    '''expression : ID'''
    p[0] = Node('ID', p[1])


def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")

def help_declaration(dcl_type, p) -> Node:
    statement = Node('CONNECT', 'statement')
    #print(p)
    datadcl = Node(dcl_type, p[1])
    var = Node('ID', p[2])
    datadcl.add_child(var)
    
    statement.add_child(datadcl)

    #print(len(p), 'help')

    is_assign = p[3]

    if(is_assign):
        is_assign.set_first(var)
        statement.add_child(is_assign)

    return statement

def merge():
    pass

parser = yacc.yacc()
argparser = argparse.ArgumentParser()
argparser.add_argument('-f', '--file')
args = argparser.parse_args()

if(args.file):
    try:

        file = args.file
        source = open(file, 'r')
        prog = source.read()
        source.close()
        yacc.parse(prog)
    except(FileNotFoundError):
        print('File does not exist.')
        
else:
    while True:
        try:
            s = input('calc > ')
        except (EOFError, KeyboardInterrupt):
            break
        if s == '!exit':
            break
        if not s:
            continue
        yacc.parse(s)
print(ast)