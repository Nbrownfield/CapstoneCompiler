import lexer
import myParser
import sys
import TokenTypes

#open file
programLines = []
with open(sys.argv[1]) as f:
    programLines=[line.strip() for line in f.readlines()]

#go through each line
allTokens = []
for line in programLines:

    #create tokens from each line
    tokens = lexer.run(line)

    #add tokens to list of tokens
    allTokens.extend(tokens)

allTokens.append(lexer.Token(TokenTypes.T_EOF, None))

#print list of tokens
print("***LIST OF TOKENS***")
for token in allTokens:
    print(token.string())

#as of right now, parser only supports 1 line.
print("\n***GENERATED AST***")
ast = myParser.run(allTokens)
print(ast.string())