#  Lexer
ident = 'id'          # used in token as (indent, <string> )    
integer = 'int'       #  (integer, <value> )
floating = 'float'    #  (floating, <value> )  
trueTok = 'True'
falseTok = 'False'
noneTok = "None"
plus = '+'            #  (plus,)    rest as this one, no attribute necessary
minus = '-'          
mult = '*'
div = '/' 
mod = '%'
exp = '**'
lparen = '('
rparen = ')'
lbrace = '['
rbrace = ']'
equals = '=='
assign = '='
colon = ':'
lt = '<'
gt = '>'
ge = '>='
le = '<='
ne = '!='
andTok = 'and'
orTok = 'or'
notTok = 'not'
defTok = 'def'
semicolon = ';'
comma = ','
let = 'let'
inTok = 'in'
ifTok = 'if'
thenTok = 'then'
elseTok = 'else'
lambdaTok = 'lambda'
apply = 'apply'
returnTok = 'return'
nil = 'nil'
cons = 'cons'
first = 'first'
rest = 'rest'
error = 'error'       #  (error, <string> )     gives spelling of token that caused the lexical error

# Non-terminals are encoded as pairs using these codes:

S = 'S'             # (S,)  etc. 
E = 'E'
A = 'A'
L = 'L'
T = 'T'
F = 'F'
I = 'I'
C = 'C'
Top = 'top'
Bor = 'Bor'
Band = 'Band'
Bnot = 'Bnot'


# special token for end of input

end_of_input = '$'       # (end_of_input,) will be pretty-printed as ($,)


def tokenToString(t):
    if t == None:
        return str(t)
    elif t[0] in ['int','float','id']:
        return '(' + t[0] + ',' + str(t[1]) + ')'
    else:
        return '(' + t[0] + ',)'
        
def tokenListToString(lst):
    res = '[ '
    for t in lst[:-1]:
        res = res + tokenToString(t) + ', '
    res = res + tokenToString(lst[-1]) + ' ]'
    return res


# Code for lexer

# put white space between each separator or operator token and split into words

def splitTokens(s):
    for t in ['+','-','*','/','(',')','[',']',',','<', ':', '>', '=', '!','%']:
        s = s.replace(t,' ' + t + ' ')
    # now repair two-character tokens
    s = s.replace('<  =','<=')
    s = s.replace('>  =','>=')
    s = s.replace('=  =','==')
    s = s.replace('!  =','!=')
    s = s.replace('*  *','**')
    return s.split()

def isLetter(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'

def isDigit(c):
    return '0' <= c <= '9' 

def isIdToken(s):
    state = 1
    for ch in s:
        if state == 1:
            if isLetter(ch) or ch == '_':
                state = 2
            else:
                return False
        elif state == 2:
            if isLetter(ch) or isDigit(ch) or ch == '_':
                state = 2
            else:
                return False
    return (state == 2)

                        
def isIntToken(s):
    if s == '0':
        return True
    state = 1
    for ch in s:
        if state == 1:
            if isDigit(ch) and ch != '0':
                state = 2
            else:
                return False
        elif state == 2:
            if isDigit(ch):
                state = 2
            else:
                return False
    return (state == 2)
    
def isFloatToken(s):
    state = 1
    finalStates = [4,6]
    for ch in s:
        if state == 1:
            if isDigit(ch) and ch != '0':
                state = 2
            elif ch == '0':
                state = 3
            elif ch == '.':
                state = 5
            else:
                return False
        elif state == 2:
            if isDigit(ch):
                state = 2
            elif ch == '.':
                state = 4
            else:
                return False
        elif state == 3:
            if ch == '.':
                state = 4
            else:
                return False
        elif state == 4:
            if isDigit(ch):
                state = 4
            else:
                return False
        elif state == 5:
            if isDigit(ch):
                state = 6
            else:
                return False
        elif state == 6:
            if isDigit(ch):
                state = 6
            else:
                return False                
                
    return (state in finalStates)   
    
def isAssignToken(s):
    return s == '='

def isPlusToken(s):
    return s == '+'
    
def isMinusToken(s):
    return s == '-'

def isMultToken(s):
    return s == '*'
    
def isDivToken(s):
    return s == '/'
    
def isModToken(s):
    return s == '%'

def isExpToken(s):
    return s == '**'

def isEqualsToken(s):
    return s == '=='

def isNEToken(s):
    return s == '!='

def isLEToken(s):
    return s == '<='
    
def isGEToken(s):
    return s == '>='

def isLTToken(s):
    return s == '<'
    
def isGTToken(s):
    return s == '>'

def isLparenToken(s):
    return s == '('
    
def isRparenToken(s):
    return s == ')'

def isLbraceToken(s):
    return s == '['
    
def isRbraceToken(s):
    return s == ']'

def isColonToken(s):
    return s == ':'

def isSemicolonToken(s):
    return s == ';'

def isCommaToken(s):
    return s == ','

def isLetToken(s):
    return s == 'let'

def isLambdaToken(s):
    return s == 'lambda'

def isInToken(s):
    return s == 'in'

def isIfToken(s):
    return s == 'if'

def isThenToken(s):
    return s == 'then'

def isElseToken(s):
    return s == 'else'

def isDefToken(s):
    return s == 'def'

def isAndToken(s):
    return s == 'and'

def isOrToken(s):
    return s == 'or'

def isNotToken(s):
    return s == 'not'

def isReturnToken(s):
    return s == 'return'

def isTrueToken(s):
    return s == 'True'

def isFalseToken(s):
    return s == 'False'

def isNoneToken(s):
    return s == 'None'

def isNilToken(s):
    return s == 'nil'

def isConsToken(s):
    return s == 'cons'

def isFirstToken(s):
    return s == 'first'

def isRestToken(s):
    return s == 'rest'

def stringToToken(t):
    if isPlusToken(t):
        return (plus,) 
    elif isMinusToken(t):
        return (minus,) 
    elif isMultToken(t):
        return (mult,) 
    elif isDivToken(t):
        return (div,) 
    elif isExpToken(t):
        return (exp,) 
    elif isModToken(t):
        return (mod,) 
    elif isLTToken(t):
        return (lt,) 
    elif isGTToken(t):
        return (gt,) 
    elif isGEToken(t):
        return (ge,)    
    elif isLEToken(t):
        return (le,) 
    elif isEqualsToken(t):
        return (equals,)
    elif isNEToken(t):
        return (ne,)     
    elif isAndToken(t):
        return (andTok,) 
    elif isOrToken(t):
        return (orTok,)
    elif isNotToken(t):
        return (notTok,)    
    elif isLparenToken(t):
        return (lparen,) 
    elif isRparenToken(t):
        return (rparen,)
    elif isLbraceToken(t):
        return (lbrace,) 
    elif isRbraceToken(t):
        return (rbrace,)
    elif isDefToken(t):
        return (defTok,)    
    elif isAssignToken(t):
        return (assign,)
    elif isColonToken(t):
        return (colon,)
    elif isSemicolonToken(t):
        return (semicolon,)
    elif isCommaToken(t):
        return (comma,)
    elif isLetToken(t):
        return (let,)
    elif isLambdaToken(t):
        return (lambdaTok,)
    elif isIfToken(t):
        return (ifTok,)
    elif isThenToken(t):
        return (thenTok,)
    elif isElseToken(t):
        return (elseTok,)
    elif isInToken(t):
        return (inTok,t)
    elif isReturnToken(t):
        return (returnTok,t)
    elif isTrueToken(t):
        return (trueTok,)
    elif isFalseToken(t):
        return (falseTok,t)
    elif isNoneToken(t):
        return (noneTok,t)
    elif isNilToken(t):
        return (nil,)
    elif isConsToken(t):
        return (cons,)
    elif isFirstToken(t):
        return (first,)
    elif isRestToken(t):
        return (rest,)
    elif isIdToken(t):
        return (ident,t)
    elif isIntToken(t):
        return (integer,int(t)) 
    elif isFloatToken(t):
        return (floating,float(t)) 

    else:
        return (error,)


def lexer(s):
    return [stringToToken(t) for t in splitTokens(s)]

