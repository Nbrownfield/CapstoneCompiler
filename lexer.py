import sys
import string
import TokenTypes

# Token class, each token has a type and value
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    #prints token
    def string(self):
        if self.value != None:
            return f'{self.type}:{self.value}'
        return f'{self.type}:{self.value}'

# Errors
class LexerError:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def tostring(self):
        result = f'{self.error_name}: {self.details}'

class Lexer:
    #initialize, start at first character
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    #goes to next character in line
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        #continues until end of line
        while self.current_char != None:

            #ignore whitespace
            if self.current_char in ' \t':
                self.advance()

            #numbers
            elif self.current_char in string.digits:
                tokens.append(self.makeNum())

            #words (identifiers, keywords, etc)
            elif self.current_char in string.ascii_letters:
                tokens.append(self.makeWord())

            #operators
            elif self.current_char in '+-*/=&!|<>':
                tokens.append(self.makeOp())

            #punctuation
            elif self.current_char == '(':
                tokens.append(Token(TokenTypes.T_LPAREN, None))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenTypes.T_RPAREN, None))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TokenTypes.T_LBRACE, None))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TokenTypes.T_RBRACE, None))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TokenTypes.T_LBRACK, None))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TokenTypes.T_RBRACK, None))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TokenTypes.T_SEMICOLON, None))
                self.advance()

        tokens.append(Token(TokenTypes.T_EOF, None))
        return tokens

    #function when number detected
    def makeNum(self):
        num_str = ''
        dot_count = 0
        
        #add each character to number string until char that isnt number or '.' is reached
        while self.current_char != None and self.current_char in string.digits + '.':
            #if current char is dot
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
                self.advance()
            else:
                num_str += self.current_char
                self.advance()

        #if no dot, store as int, else store as float.
        if dot_count == 0:
            return Token(TokenTypes.T_INT, int(num_str))
        else:
            return Token(TokenTypes.T_FLOAT, float(num_str))

    #function when word detected
    def makeWord(self):
        word_str = ''

        #add to word until char that isnt a letter or '_' is reached
        while self.current_char != None and self.current_char in string.ascii_letters + string.digits + '_':
            word_str += self.current_char
            self.advance()

        #checks if keyword or literal
        if word_str == 'int':
            return Token(TokenTypes.T_TYPE, word_str)
        elif word_str == 'float':
            return Token(TokenTypes.T_TYPE, word_str)
        elif word_str == 'bool':
            return Token(TokenTypes.T_TYPE, word_str)
        elif word_str == 'char':
            return Token(TokenTypes.T_TYPE, word_str)
        elif word_str == 'return':
            return Token(TokenTypes.T_KEYWORD, word_str)
        elif word_str == 'if':
            return Token(TokenTypes.T_KEYWORD, word_str)
        elif word_str == 'while':
            return Token(TokenTypes.T_KEYWORD, word_str)
        elif word_str == 'else':
            return Token(TokenTypes.T_KEYWORD, word_str)
        elif word_str == 'main':
            return Token(TokenTypes.T_MAIN, None)
        else:
            return Token(TokenTypes.T_IDEN, word_str)
    
    #function when operator detected
    def makeOp(self):
        op_str = ''

        while self.current_char != None and self.current_char in '+-*/=&!|<>':
            op_str += self.current_char
            self.advance()
        
        #determines operator
        if op_str == '+':
            return Token(TokenTypes.T_PLUS, '+')
        elif op_str == '-':
            return Token(TokenTypes.T_MINUS, '-')
        elif op_str == '*':
            return Token(TokenTypes.T_MUL, '*')
        elif op_str == '/':
            return Token(TokenTypes.T_DIV, '/')
        elif op_str == '%':
            return Token(TokenTypes.T_MOD, '%')
        elif op_str == '<<':
            return Token(TokenTypes.T_LSHIFT, '<<')
        elif op_str == '>>':
            return Token(TokenTypes.T_RSHIFT, '>>')
        elif op_str == '=':
            return Token(TokenTypes.T_ASSIGN, '=')
        elif op_str == '==':
            return Token(TokenTypes.T_EQCOMP, '==')
        elif op_str == '!=':
            return Token(TokenTypes.T_NOTEQ, '!=')
        elif op_str == '>':
            return Token(TokenTypes.T_GTHAN, '>')
        elif op_str == '<':
            return Token(TokenTypes.T_LTHAN, '<')
        elif op_str == '>=':
            return Token(TokenTypes.T_GTEQ, '>=')
        elif op_str == '<=':
            return Token(TokenTypes.T_LTEQ, '<=')
        elif op_str == '&&':
            return Token(TokenTypes.T_AND, '&&')
        elif op_str == '||':
            return Token(TokenTypes.T_OR, '||')
        elif op_str == '!':
            return Token(TokenTypes.T_NOT, '!')
        else:
            return Token(None, None) #error


def run(text):
    #create lexer class, make tokens from line of text
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    return tokens