from wscope import ScopeNode
from wtac import TACTable
import wsymbols

class Executer:

    def __init__(self, tac:TACTable) -> None:
        self.tac = tac
        self.symbols = {}

    def execute(self):
        i = 0

        while(i < len(self.tac.entries)):
            p = self.process(self.tac.entries[i])
            #print(p)
            if(p != False):
                i = self.get_label_index(p)
                continue
            i += 1
    def get_label_index(self, label):
        for i, entry in enumerate(self.tac.entries):
            if(entry['label'] == label):
                return i
        return -1
    def get_val(self, arg):
        if(arg in self.symbols):
            return self.symbols[arg]
        return arg

    def process(self, entry):
        op = entry['operation']

        # Print
        #print(self.symbols)
        if(op == 'PRINT'):
            print(self.get_val(entry['arg1']))
        
        # Declarations
        elif(op == 'INT'):
            self.symbols[entry['arg1']] = '_undefined'
        elif(op == 'FLOAT'):
            self.symbols[entry['arg1']] = '_undefined'
        elif(op == 'STRING'):
            self.symbols[entry['arg1']] = '_undefined'
        elif(op == 'BOOLEAN'):
            self.symbols[entry['arg1']] = '_undefined'
        elif(op == 'ASSIGN'):
            self.symbols[entry['arg1']] = self.get_val(entry['arg2'])
        
        #Binary Operations
        elif(op == 'PLUS'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) + self.get_val(entry['arg2'])
        elif(op == 'MINUS'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) - self.get_val(entry['arg2'])
        elif(op == 'MULT'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) * self.get_val(entry['arg2'])
        elif(op == 'DIVIDE'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) / self.get_val(entry['arg2'])
        elif(op == 'EXP'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) ** self.get_val(entry['arg2'])
        
        #Control
        elif(op == 'GOTO'):
            return entry['arg1']
        elif(op == 'IFGOTO'):
            booln = self.get_val(entry['arg1'])
            if(booln):
                return entry['arg2']
        elif(op == 'IFNOTGOTO'):
            booln = self.get_val(entry['arg1'])
            if(not booln):
                return entry['arg2']
            
        #Comparisons
        elif(op == 'LTHAN'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) < self.get_val(entry['arg2'])
        elif(op == 'EQUAL'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) == self.get_val(entry['arg2'])
        elif(op == 'NOTEQUAL'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) != self.get_val(entry['arg2'])
        elif(op == 'GTHAN'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) > self.get_val(entry['arg2'])
        elif(op == 'GEQTHAN'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) >= self.get_val(entry['arg2'])
        elif(op == 'LEQTHAN'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) <= self.get_val(entry['arg2'])
        elif(op == 'AND'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) and self.get_val(entry['arg2'])
        elif(op == 'OR'):
            self.symbols[entry['result']] = self.get_val(entry['arg1']) or self.get_val(entry['arg2'])

        return False
