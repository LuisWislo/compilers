class ScopeNode: 
    def __init__(self, level):
        self.level = level
        self.table = {'_scope_lvl': self.level}
        self.parent = None
        self.children = []
    
    def __repr__(self) -> str:
        return repr(self.table)