from werrors import WException
from wtree import AbstractSyntaxTree as AST, Node
import wsymbols as sym
from wscope import ScopeNode



def analyze(ast:AST):
    try:
        global_scope = ScopeNode()
        traverse(ast.root, global_scope)
        print(global_scope)
    except WException as err:
        print(err.message)


def traverse(current:Node, cscope:ScopeNode): #should return value from children

    #print(current)
    if(current.token_id == 'INT'):
        sym.init_symbol(current.children[0], 'INUM', cscope)
        return True
    
    elif(current.token_id == 'FLOAT'):
        sym.init_symbol(current.children[0], 'FNUM', cscope)
        return True
    
    elif(current.token_id == 'STRING'):
        sym.init_symbol(current.children[0], 'STRVAL', cscope)
        return True
    
    elif(current.token_id == 'BOOLEAN'):
        sym.init_symbol(current.children[0], 'BOOLVAL', cscope)
        return True

    elif(current.token_id == 'ASSIGN'):
        to_set = traverse(current.children[1], cscope)
        sym.set_symbol_value(current.children[0], to_set, cscope)
        return True

    elif(current.token_id == 'PRINT'):
        node = traverse(current.children[0], cscope)
        val = sym.get_node_value(node, cscope)
        print(val)
        return True
    
    elif(current.token_id in ['PLUS', 'MINUS', 'MULT', 'DIVIDE', 'EXP']):
        left = traverse(current.children[0], cscope)
        right = traverse(current.children[1], cscope)
        return binary_ops(left, right, current.value, cscope)
    
    
    elif(current.token_id == 'INUM'
        or current.token_id == 'FNUM'
        or current.token_id == 'BOOLVAL'
        or current.token_id == 'STRVAL'
        or current.token_id == 'ID'):
        return current

    for child in current.children:
        traverse(child, cscope)

def binary_ops(left:Node, right:Node, operator, scope:ScopeNode):
    newval = None

    left_prim = sym.get_node_value(left, scope)
    right_prim = sym.get_node_value(right, scope)

    if(operator == '+'):
        newtype = ''
        newval = left_prim.value + right_prim.value
    elif(operator == '-'):
        newtype = ''
        newval = left_prim.value - right_prim.value
    elif(operator == '*'):
        newtype = ''
        newval = left_prim.value * right_prim.value
    elif(operator == '/'):
        newtype = ''
        newval = left_prim.value / right_prim.value
    elif(operator == '^'):
        newtype = ''
        newval = left_prim.value ** right_prim.value
    
    return Node(left_prim.token_id, newval)
