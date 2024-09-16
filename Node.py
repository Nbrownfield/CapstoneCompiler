class FunctionNode:
    def __init__(self, type, name, args, block):
        self.type = type
        self.name = name
        self.args = args #list of tokens that rep args
        self.block = block

    def string(self):
        #convert argument list to string
        argListString = ''
        for arg in self.args:
            argListString = argListString + arg[0].value + ' ' + arg[1].value

            #add comma to separate arguments unless it is last argument in last
            if self.args.index(arg) != len(self.args)-1:
                argListString += ', '

        #convert statement list to string
        statementListString = ''
        for statement in self.block:
            statementListString = statementListString + statement.string() + ';\n'

        return f'({self.type.value} {self.name.value}({argListString})\n{{\n{statementListString}}})'

class IfNode:
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def string(self):
        #convert statement list to string
        statementListString = ''
        for statement in self.block:
            statementListString = statementListString + statement.string() + ';\n'

        return f'(if ({self.cond.string()})\n{{\n{statementListString}}})'

class ReturnNode:
    def __init__(self, val):
        self.val = val
    
    def string(self):
        return f'(return {self.val.string()})'

#ie int A = 5 + 3;
class VarAssignNode:
    def __init__(self, type, name, expr):
        self.type = type
        self.name = name
        self.expr = expr

    #returns string representing node
    def string(self):
        return f'({self.type.value} {self.name.value} = {self.expr.string()})'

#ie A = 4;
class AccessVarNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def string(self):
        return f'({self.name.value} = {self.expr.string()})'

#node representing a single number (or variable)
class NumberNode:
    def __init__(self, val):
        self.val = val

    def string(self):
        return f'{self.val.value}'

class VarAccessNode:
    def __init__(self, val):
        self.val = val

    def string(self):
        return f'{self.val.value}'

#ie 5 + 3
class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def string(self):
        return f'({self.left.string()} {self.op.value} {self.right.string()})'

#ie -5
class UnOpNode:
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def string(self):
        return f'({self.op.value} {self.arg.string()})'