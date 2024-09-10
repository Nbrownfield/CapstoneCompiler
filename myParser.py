import lexer
import TokenTypes
import sys

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

class ReturnNode:
    def __init__(self, val):
        self.val = val
    
    def string(self):
        return f'(return {self.val.value})'

#ie int A = 5 + 3;
class VarAssignNode:
    def __init__(self, type, name, expr):
        self.type = type
        self.name = name
        self.expr = expr

    #returns string representing node
    def string(self):
        return f'({self.type.value} {self.name.value} = {self.expr.string()})'

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

#main class
class myParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.advance()

    #iterate through token list
    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.currentToken = self.tokens[self.idx]

    #main function, for now assuming main node is expression
    def parse(self):
        res = self.function()

        #if self.currentToken.type is not TokenTypes.T_EOF:
            #error

        return res
            
    #factor = {-factor} | {number} | {identifier} | {LPAREN expression RPAREN}
    def factor(self):
        token = self.currentToken

        #if current token is minus sign (-)
        if token.type in (TokenTypes.T_MINUS):
            #go to next token, store as factor
            self.advance()
            factor = self.factor()
            #should I return error in the case of -(-factor)? double negative should be fine...
            return UnOpNode(token, factor)

        #if current token is number or identifier
        elif token.type in (TokenTypes.T_INT, TokenTypes.T_FLOAT):
            #return number node and advance to next token
            self.advance()
            return NumberNode(token)

        elif token.type in (TokenTypes.T_IDEN):
            self.advance()
            return VarAccessNode(token)

        #if current token is LPAREN '('
        elif token.type is TokenTypes.T_LPAREN:
            #go to next token, store expression
            self.advance()
            expr = self.expr()

            #if next token is closing parentheses, return expression
            if self.currentToken.type is TokenTypes.T_RPAREN:
                self.advance()
                return expr
            #else: error

        #else: error

    #term = {factor [MUL | DIV] factor} | factor
    def term(self):
        return self.binOp(self.factor, (TokenTypes.T_MUL, TokenTypes.T_DIV))

    #expression = {term [PLUS | MINUS] term} | term
    def expr(self):
        return self.binOp(self.term, (TokenTypes.T_PLUS, TokenTypes.T_MINUS))

    #comparison = {NOT comparison} | {expr [logic op] expr} | expr
    def comparison(self):
        #if current token is NOT (!blah)
        if self.currentToken.type is TokenTypes.T_NOT:
            opToken = self.currentToken
            self.advance()
            comp = self.comparison()
            return UnOpNode(opToken, comp)

        else:
            return self.binOp(self.expr, (TokenTypes.T_EQCOMP, TokenTypes.T_NOTEQ, TokenTypes.T_GTHAN, TokenTypes.T_LTHAN, TokenTypes.T_GTEQ, TokenTypes.T_LTEQ))


    #equation = {TYPE IDENTIFIER = expression} | {comparison [AND | OR] comparison} | comp
    def equation(self):
        #if current token is type keyword (int, float)
        if self.currentToken.type is TokenTypes.T_TYPE and self.currentToken.value in ('int', 'float'):
            varType = self.currentToken
            self.advance()

            #if not identifier, error
            identifier = self.currentToken
            self.advance()

            #if not =, error
            self.advance()

            #store expression
            expr = self.expr()

            return VarAssignNode(varType, identifier, expr)
        
        else:
            return self.binOp(self.comparison, (TokenTypes.T_AND, TokenTypes.T_OR))

    #to be main function for each line: determines if assignment, if, while, return, etc.
    def statement(self):
        if self.currentToken.type is TokenTypes.T_KEYWORD:
            if self.currentToken.value == 'return':
                self.advance()
                returnValue = self.currentToken

                #if not semicolon error
                self.advance()
                
                return ReturnNode(returnValue)
        else:
            return self.equation()


    def function(self):
        if self.currentToken.type is TokenTypes.T_TYPE:
            funcType = self.currentToken
            self.advance()

            #if not func identifier, error
            funcIden = self.currentToken
            self.advance()

            #if not LPAREN, error
            self.advance()

            argList = []
            while self.currentToken.type is not TokenTypes.T_RPAREN:
                #loop through arguments (TYPE IDENTIFER, TYPE IDENTIFER)
                argType = self.currentToken
                self.advance()

                argIden = self.currentToken
                self.advance()

                argList.append((argType,argIden))


            self.advance()

            #if not LBRACE error
            self.advance()

            statementList = []
            while self.currentToken.type is not TokenTypes.T_RBRACE:
                #loop through statements
                statement = self.statement()

                statementList.append(statement)

                #if no semicolon, error
                self.advance()

        return FunctionNode(funcType, funcIden, argList, statementList)

    def binOp(self, func, ops):
        #stores left
        left = func()

        #while current token is in acceptable list of ops
        while self.currentToken.type in ops:
            opToken = self.currentToken
            self.advance()
            right = func()
            left = BinaryOpNode(left, opToken, right)

        return left

#main run function, called by main.py
def run(tokens):
    parser = myParser(tokens)
    ast = parser.parse()

    return ast