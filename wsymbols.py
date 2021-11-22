import werrors
from wtree import Node
from wscope import ScopeNode

def is_expression(node:Node):
    return is_primitive(node) or (
        node.token_id == 'PLUS'
        or node.token_id == 'MINUS'
        or node.token_id == 'MULT'
        or node.token_id == 'DIVIDE'
        or node.token_id == 'EXP')

def is_primitive(node:Node):
    return (node.token_id == 'INUM' 
            or node.token_id == 'FNUM'
            or node.token_id == 'STRVAL'
            or node.token_id == 'BOOLVAL')

def init_symbol(node:Node, _type:str, scope:ScopeNode):
    if(symbol_exists(node.value, scope)):
        raise werrors.VarAlreadyDeclaredError(node.value)
    
    scope.table[node.value] = {'value': '_undefined', 'type': _type}

def set_symbol_value(id:Node, value:Node, scope:ScopeNode):

    id_scope = symbol_exists(id.value, scope)

    if(not id_scope):
        raise werrors.UndeclaredVarError(id.value)

    is_prim = is_primitive(value)
    newval_scope = symbol_exists(value.value, scope)
    
    if(not is_prim and not newval_scope):
        raise werrors.UndeclaredVarError(value.value)

    actualval = value.value
    valtype = value.token_id

    if(not is_prim):
        actualval = newval_scope.table[value.value]['value']
        valtype = newval_scope.table[value.value]['type']
    
    if(id_scope.table[id.value]['type'] == valtype):
        id_scope.table[id.value]['value'] = actualval
    else: #check type conversion (int2Float)
        raise werrors.TypeMismatchError(valtype, id_scope.table[id.value]['type'])

def get_node_value(node:Node, scope:ScopeNode):
    if(is_primitive(node)):
        return node
    return get_symbol_value(node.value, scope)

def get_symbol_value(symbol_name, scope:ScopeNode):
    if(scope):
        if(symbol_name in scope.table):
            if(scope.table[symbol_name] == '_undefined'):
                raise werrors.UnassignedVarError(symbol_name)
            return Node(scope.table[symbol_name]['type'], scope.table[symbol_name]['value'])#scope.table[symbol_name]['value']
        return get_symbol_value(symbol_name, scope.parent)
    raise werrors.UndeclaredVarError(symbol_name)
    
        
def symbol_exists(symbol_name, scope:ScopeNode):
    if(scope):
        if(symbol_name in scope.table):
            return scope
        return symbol_exists(symbol_name, scope.parent)
    return False

def print_symbols(scope:ScopeNode):
    if(scope):
        print(scope.table)
        print_symbols(scope.parent)