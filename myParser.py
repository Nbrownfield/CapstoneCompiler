import lexer
import TokenTypes
import sys

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
        res = self.expr()

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

    #expression = {term [PLUS | MINUS] term} |  {TYPE IDENTIFIER = expression}
    def expr(self):

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
            return self.binOp(self.term, (TokenTypes.T_PLUS, TokenTypes.T_MINUS))

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