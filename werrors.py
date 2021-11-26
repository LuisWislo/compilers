class WException(Exception):
    
    def __init__(self, message) -> None:
        self.message = message

class SemanticError(WException):
    
    def __init__(self, message) -> None:
        super().__init__(f'[Semantic Error]: {message}')

class VarAlreadyDeclaredError(SemanticError):
    
    def __init__(self, var) -> None:
        super().__init__(f'Variable \'{var}\' is already declared.')

class UndeclaredVarError(SemanticError):
    
    def __init__(self, var) -> None:
        super().__init__(f'Variable \'{var}\' has not been declared.')

class UnassignedVarError(SemanticError):
    
    def __init__(self, var) -> None:
        super().__init__(f'Variable \'{var}\' has not been assigned a value.')

class TypeMismatchError(SemanticError):
    
    def __init__(self, from_type, to_type) -> None:
        super().__init__(f'Cannot assign \'{from_type}\' to \'{to_type}\'')

class OperandMismatchError(SemanticError):
    def __init__(self, a_type, b_type, operation) -> None:
        super().__init__(f'Cannot apply operation \'{operation}\' between \'{a_type}\' and \'{b_type}\'')