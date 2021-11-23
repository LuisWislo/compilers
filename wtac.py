class TACTable:

    def __init__(self):
        self.entries = []
        self.next_label = 0
        self.temp_var = 0

    def add_entry(self, operation, result=None, arg1=None, arg2=None, temp_var = False, set_label=None):
        label = None
        if(not set_label):
            label = f'l{self.next_label}'
            self.next_label += 1
        else:
            label = set_label

        if(temp_var):
            result = f'v{self.temp_var}'
            self.temp_var += 1

        if(arg1 == '_jump'):
            arg1 = f'l{self.next_label}'
            self.next_label += 1

        if(arg2 == '_jump'):
            arg2 = f'l{self.next_label}'
            self.next_label += 1
        
        entry = {
            'label': label,
            'result': result,
            'operation': operation,
            'arg1': arg1,
            'arg2': arg2
        }

        self.entries.append(entry)

        return entry
    
    def update_val(self, label, key, newval):
        pass
    
    def get_latest(self):
        return self.entries[-1]
    


    def get_format(self):
        lengths = []

        for k in self.entries[0].keys():
            allvals = list(map(lambda var: str(var) if var != None else '-',[d[k] for d in self.entries]))
            allvals.append(k)
            val = len(max(allvals, key=len)) + 1
            lengths.append(val)
        output = ''

        for l in lengths:
            output += f'{{:<{l}}}'
        output += '\n'
        return output
    
    def __repr__(self) -> str:
        theformat = self.get_format()
        out = theformat.format('Label', 'Result', 'Operation', 'Arg1', 'Arg2')
        for e in self.entries:
            str_result = '-' if e['result'] == None else str(e['result'])
            str_arg1 = '-' if e['arg1'] == None else str(e['arg1'])
            str_arg2 = '-' if e['arg2'] == None else str(e['arg2']) 
            out += theformat.format(e['label'], str_result, e['operation'] or '-', str_arg1, str_arg2)
        return out