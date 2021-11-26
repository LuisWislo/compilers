class Node:
    
    def __init__(self, token_id=None, value=None) -> None:
        self.token_id = token_id
        self.value = value
        self.children = []
        self.tac_id = None
        self.young = None
    
    def __repr__(self) -> str:
        return f'({self.token_id}, {self.value})'

    def set_first(self, node):
        if(node.token_id == 'CONNECT'):
            self.children = node.children + self.children
        else:
            self.children.insert(0, node)

    def add_child(self, node):
        if(node.token_id == 'CONNECT'):
            self.children += node.children
            return node.children[0]
        self.children.append(node)
        return node
    
    def is_empty(self):
        return self.token_id == None
    
    def set_scope(self, scope):
        self.scope = scope
    
    def set_young(self, tac_id):
        if(self.young != None):
            self.young = tac_id


class ForNode(Node):

    def __init__(self, token_id, value) -> None:
        super().__init__(token_id, value)
        self.statement = None
        self.condition = None
        self.tail = None
        self.then = None
        
    def sequence(self, which):
        if(which == 'statement'):
            return self.sequence_separator(0, self.condition)
        elif(which == 'condition'):
            index = self.segment_index(self.condition)
            return self.sequence_separator(index, self.tail)
        elif(which == 'tail'):
            index = self.segment_index(self.tail)
            return self.sequence_separator(index, self.then)
        elif(which == 'then'):
            index = self.segment_index(self.then)
            return self.sequence_separator(index)

    
    def segment_index(self, which):
        index = 0

        for i in self.children:
            if(i == which):
                return index
            index += 1
        
        return index
    
    def sequence_separator(self, _from, next = None):
        if next == None:
            return self.children[_from:]

        out = []
        for i in self.children[_from:]:
            if(i == next):
                break
            out.append(i)
        return out

    def set_statement(self, node:Node):
        self.statement = self.add_child(node)
    
    def set_condition(self, node:Node):
        self.condition = self.add_child(node)
    
    def set_tail(self, node:Node):
        self.tail = self.add_child(node)
    
    def set_then(self, node:Node):
        self.then = self.add_child(node)


class LoopNode(Node):

    def __init__(self, token_id, value) -> None:
        super().__init__(token_id, value)
        self.condition = None
        self.then = None
    
    def set_condition(self, node:Node):
        self.condition = self.add_child(node)
    
    def set_then(self, node:Node):
        self.then = self.add_child(node)


class IfControllerNode(Node):

    def __init__(self, token_id, value) -> None:
        super().__init__(token_id, value)
        self.condition = None
        self.els = None
    
    def set_condition(self, node:Node):
        self.condition = self.add_child(node)

    def set_else(self, node:Node):
        self.els = self.add_child(node)
    
    def get_else_index(self):
        index = 0
        for c in self.children:
            if(c == self.els):
                return index
            index += 1
        return -1


class AbstractSyntaxTree:

    def __init__(self):
        self.root = None
    
    def __repr__(self) -> str:
        return self.display(self.root)

    #add loop
    #add condition

    def display(self, node:Node, lvl=0) -> str:
        if(node):
            tree = '\t'*lvl+repr(node)+'\n'
            for child in node.children:
                tree += self.display(child, lvl+1)
            return tree
        return ''

    





