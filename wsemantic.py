from collections import Counter
import werrors
from wtac import TACTable
from wtree import AbstractSyntaxTree as AST, Node, IfControllerNode
import wsymbols as sym
from wscope import ScopeNode

tac = TACTable()

wl_plus = [
    Counter(['INUM', 'INUM']), 
    Counter(['FNUM', 'FNUM']), 
    Counter(['INUM', 'FNUM']), 
    Counter(['INUM', 'STRVAL']), 
    Counter(['FNUM', 'STRVAL']),
    Counter(['STRVAL', 'STRVAL'])
]

wl_others = [
    Counter(['INUM', 'INUM']), 
    Counter(['FNUM', 'FNUM']), 
    Counter(['INUM', 'FNUM'])
]

def display_scopes(scope:ScopeNode):
    if(scope):
        print(scope)
        for child in scope.children:
            display_scopes(child)


def analyze(ast:AST):
    global_scope = ScopeNode(0)
    traverse(ast.root, global_scope)

def get_tac_arg(node:Node):
    if(node.tac_id):
        return node.tac_id
    return node.value

def traverse(current:Node, cscope:ScopeNode): #should return value from children

    #print(current)
    if(current.token_id == 'INT'):
        sym.init_symbol(current.children[0], 'INUM', cscope)
        tac.add_entry('INT', current.children[0].value)
        return True
    
    elif(current.token_id == 'FLOAT'):
        sym.init_symbol(current.children[0], 'FNUM', cscope)
        tac.add_entry('FLOAT', current.children[0].value)
        return True
    
    elif(current.token_id == 'STRING'):
        sym.init_symbol(current.children[0], 'STRVAL', cscope)
        tac.add_entry('STRING', current.children[0].value)
        return True
    
    elif(current.token_id == 'BOOLEAN'):
        sym.init_symbol(current.children[0], 'BOOLVAL', cscope)
        tac.add_entry('BOOLEAN', current.children[0].value)
        return True

    elif(current.token_id == 'ASSIGN'):
        to_set = traverse(current.children[1], cscope)
        tac.add_entry('ASSIGN', current.children[0].value, get_tac_arg(to_set))
        sym.set_symbol_value(current.children[0], to_set, cscope)
        return True

    elif(current.token_id == 'PRINT'):
        node = traverse(current.children[0], cscope)
        val = sym.get_node_value(node, cscope)
        tac.add_entry('PRINT', val.value, node.value)
        return True
    
    elif(current.token_id in ['PLUS', 'MINUS', 'MULT', 'DIVIDE', 'EXP']):
        left = traverse(current.children[0], cscope)
        right = traverse(current.children[1], cscope)
        result = binary_ops(left, right, current.value, cscope)
        tac_id = tac.add_entry(current.token_id, arg1=get_tac_arg(left), arg2=get_tac_arg(right), temp_var=True)['result']
        result.tac_id = tac_id
        return result
    
    elif(current.token_id in ['EQUAL', 'NOTEQUAL', 'GTHAN', 'LTHAN', 'GEQTHAN', 'LEQTHAN']):
        left = traverse(current.children[0], cscope)
        right = traverse(current.children[1], cscope)
        result = comparison(left, right, current.value, cscope)
        tac_id = tac.add_entry(current.token_id, arg1=get_tac_arg(left), arg2=get_tac_arg(right), temp_var=True)['result']
        result.tac_id = tac_id
        return result
    
    elif(current.token_id in ['AND', 'OR']):
        left = traverse(current.children[0], cscope)
        right = traverse(current.children[1], cscope)
        result = comparison(left, right, current.value, cscope)
        result.tac_id = tac.add_entry(current.token_id, arg1=get_tac_arg(left), arg2=get_tac_arg(right), temp_var=True)['result']
        return result

    elif(isinstance(current, IfControllerNode)):
        condition = sym.get_node_value(traverse(current.condition, cscope), cscope)
        #tac_id?
        print(condition)

        var_condition = None
        if(condition.tac_id):
            var_condition = condition.tac_id
        else:
            var_condition = condition.value

        print(var_condition)
        
        then_scope = ScopeNode(cscope.level + 1)
        then_scope.parent = cscope
        else_scope = ScopeNode(cscope.level + 1)
        else_scope.parent = cscope

        cscope.children.append(then_scope)
        cscope.children.append(else_scope)

        else_index = current.get_else_index()

        if(len(current.children) > 1):
            tac_cond = tac.add_entry('IFGOTO', arg1=var_condition, arg2='_jump')
            if(else_index > -1):
                for child in current.children[else_index:]:
                    traverse(child, else_scope)
                
                # Jump to the end of if->then
                if_out = tac.add_entry('GOTO', arg1='_jump')
                tac.add_entry('CHECKPOINT', set_label=tac_cond['arg2'])

                for child in current.children[1:else_index]:
                    traverse(child, then_scope)
                
                # End of if statement
                tac.add_entry('CHECKPOINT', set_label=if_out['arg1'])
                
            else:
                if_out = tac.add_entry('GOTO', arg1='_jump')
                tac.add_entry('CHECKPOINT', set_label=tac_cond['arg2'])
                for child in current.children[1:]:
                    traverse(child, then_scope)

                tac.add_entry('CHECKPOINT', set_label=if_out['arg1'])  
            
        return True


    elif(current.token_id == 'INUM'
        or current.token_id == 'FNUM'
        or current.token_id == 'BOOLVAL'
        or current.token_id == 'STRVAL'
        or current.token_id == 'ID'):
        return current

    for child in current.children:
        traverse(child, cscope)

def comparison(left:Node, right:Node, operator, scope:ScopeNode):
    left_prim = sym.get_node_value(left, scope)
    right_prim = sym.get_node_value(right, scope)

    newval = False
    newtype = 'BOOLVAL'

    if(operator == '=='):
        newval = left_prim.value == right_prim.value
    elif(operator == '!='):
        newval = left_prim.value != right_prim.value
    elif(operator == '>'):
        newval = left_prim.value > right_prim.value
    elif(operator == '<'):
        newval = left_prim.value < right_prim.value
    elif(operator == '>='):
        newval = left_prim.value >= right_prim.value
    elif(operator == '<='):
        newval = left_prim.value <= right_prim.value
    elif(operator == 'and'):
        newval = left_prim.value and right_prim.value
    elif(operator == 'or'):
        newval = left_prim.value or right_prim.value
    
    return Node(newtype, newval)

def binary_ops(left:Node, right:Node, operator, scope:ScopeNode):
    left_prim = sym.get_node_value(left, scope)
    right_prim = sym.get_node_value(right, scope)

    newval = None
    newtype = left_prim.token_id

    operands = Counter([left_prim.token_id, right_prim.token_id])
    if(operator == '+'):
        if(operands in wl_plus):
            if(operands == Counter(['STRVAL', 'INUM']) or operands == Counter(['STRVAL', 'FNUM'])):
                newval = str(left_prim.value) + str(right_prim.value)
                newtype = 'STRVAL'
            else:
                if(operands == Counter(['INUM', 'FNUM'])):
                    newtype = 'FNUM'

                newval = left_prim.value + right_prim.value
        else:
            raise werrors.OperandMismatchError(left_prim.token_id, right_prim.token_id, '+')
    elif(operator == '-'):
        if(operands in wl_others):
            if(operands == Counter(['INUM', 'FNUM'])):
                newtype = 'FNUM'

            newval = left_prim.value - right_prim.value
        else:
            raise werrors.OperandMismatchError(left_prim.token_id, right_prim.token_id, '-')
        
    elif(operator == '*'):
        if(operands in wl_others):
            if(operands == Counter(['INUM', 'FNUM'])):
                newtype = 'FNUM'

            newval = left_prim.value * right_prim.value
        else:
            raise werrors.OperandMismatchError(left_prim.token_id, right_prim.token_id, '*')
    elif(operator == '/'):
        if(operands in wl_others):
            if(operands == Counter(['INUM', 'INUM'])):
                newval = left_prim.value // right_prim.value
            else:
                newtype = 'FNUM'
                newval = left_prim.value / right_prim.value
        else:
            raise werrors.OperandMismatchError(left_prim.token_id, right_prim.token_id, '/')
    elif(operator == '^'):
        if(operands in wl_others):
            if(operands == Counter(['INUM', 'FNUM'])):
                newtype = 'FNUM'

            newval = left_prim.value ** right_prim.value
        else:
            raise werrors.OperandMismatchError(left_prim.token_id, right_prim.token_id, '^')
    
    return Node(newtype, newval)