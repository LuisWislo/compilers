class ScopeNode:

    next_id = 0

    def __init__(self, level):
        self.id = f'S{ScopeNode.next_id}'
        ScopeNode.next_id += 1
        self.level = level
        self.table = {'_scope_lvl': self.level}
        self.parent = None
        self.children = []
    
    def __repr__(self) -> str:
        return repr(self.table)