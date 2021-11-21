class Node:
    
    def __init__(self, token_id=None, value=None) -> None:
        self.token_id = token_id
        self.value = value
        self.children = []
    
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
        else:
            self.children.append(node)
    
    def is_empty(self):
        return self.token_id == None
    


class LoopNode(Node):

    def __init__(self, token_id, value) -> None:
        super().__init__(token_id, value)


class IfControllerNode(Node):

    def __init__(self, token_id, value) -> None:
        super().__init__(token_id, value)
        self.condition = None
        self.els = None
    
    def set_condition(self, node:Node):
        self.add_child(node)
        self.condition = node
        
    # def set_then(self, node:Node):
    #     self.add_child(node)
    #     self.then = node

    def set_else(self, node:Node):
        self.add_child(node)
        self.els = node

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

    





