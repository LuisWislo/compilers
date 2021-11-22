class ScopeNode: 
    def __init__(self):
        self.table = {'_scope_lvl': 0}
        self.parent = None
    
    def __repr__(self) -> str:
        return repr(self.table)