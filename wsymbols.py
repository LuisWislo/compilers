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
    node.fullname = construct_fullname(scope.id, node.value)
    scope.table[node.fullname] = {'value': '_undefined', 'type': _type}

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
        actualval = newval_scope.table[value.fullname]['value']
        valtype = newval_scope.table[value.fullname]['type']
    
    id_fullname = construct_fullname(id_scope.id, id.value)

    if(id_scope.table[id_fullname]['type'] == valtype):
        id_scope.table[id_fullname]['value'] = actualval
    else: #check type conversion (int2Float)
        raise werrors.TypeMismatchError(valtype, id_scope.table[id_fullname]['type'])

def get_node_value(node:Node, scope:ScopeNode):
    if(is_primitive(node)):
        return node
    return get_symbol_value(node.value, scope)

def get_symbol_value(symbol_name, scope:ScopeNode):
    if(scope):
        fullname = construct_fullname(scope.id, symbol_name)
        if(fullname in scope.table):
            if(scope.table[fullname] == '_undefined'):
                raise werrors.UnassignedVarError(symbol_name)
            out = Node(scope.table[fullname]['type'], scope.table[fullname]['value'])
            out.fullname = construct_fullname(scope.id, symbol_name)
            return out
        return get_symbol_value(symbol_name, scope.parent)
    raise werrors.UndeclaredVarError(symbol_name)
    
        
def symbol_exists(symbol_name, scope:ScopeNode):
    if(scope):
        fullname = construct_fullname(scope.id, symbol_name)
        if(fullname in scope.table):
            return scope
        return symbol_exists(symbol_name, scope.parent)
    return False

def print_symbols(scope:ScopeNode):
    if(scope):
        print(scope.table)
        print_symbols(scope.parent)
    
def construct_fullname(namespace, symbol_name):
    return f'{namespace}-{symbol_name}'