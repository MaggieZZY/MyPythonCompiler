# Code for shift-reduce parser

# pretty-printing parser configurations

def pprint_parser(parsingStack,inputListOfTokens):
    totalWidth = 80
    smallestGap = 6
    largestStackLength = int(totalWidth*0.6 - smallestGap/2)   # most characters to display
    largestInputLength = totalWidth - largestStackLength - smallestGap
    
    p = '| '
    for symbol in parsingStack:
        p = p + tokenToString(symbol) + ' '
    if len(p) > largestStackLength:
        ind = int(len(p) - largestStackLength + 9)
        p = '| ... ' + p[ind:]
        
    q = ""
    for tok in inputListOfTokens[:-1]:
        q = q + tokenToString(tok) + ' '
    if len(inputListOfTokens) > 0:
        q = q + tokenToString(inputListOfTokens[-1]) 

    if len(q) > largestInputLength:
        ind = int(largestInputLength - 9)
        q = q[:ind] + ' ... ' 
    
    q = q + ' |'
        
    p = p + (' ' * (totalWidth - len(p) - len(q)))
    print(p+q)
    
# Pretty-printing code for testing your solution

def AST_to_string(t):
    if t == None:
        return None
    elif t == []:
        return '[]'
    elif type(t) == list:
        s = '['
        for el in t[:-1]:
            s += AST_to_string(el) + ','
        s += AST_to_string(t[-1])
        return s + ']'
    elif type(t) != tuple:
        return str(t)
    elif t[0] in ['int','id','float']:
        return str(t[1])
    elif t[0] == nil:
        return 'nil'
    elif len(t) == 1 and (t[0] == 'params' or t[0] == 'args'):
        return '()'
    elif len(t) == 1 and t[0] in ['cons','first','rest']:
        return t[0]
    elif len(t) == 1:
        return '(' + AST_to_string(t[0]) + ')'
    elif len(t) == 2 and t[0] in ['-', 'not']:
        return t[0] + '(' + AST_to_string(t[1]) + ')'
    elif len(t) == 2 and (t[0] == 'params' or t[0] == 'args'):
        return '(' + AST_to_string(t[1]) + ')'
    elif len(t) == 2:
        return '(' + AST_to_string(t[0]) + ',' + AST_to_string(t[1]) + ')'
    elif len(t) == 3 and t[0] in ['*','+', '/', '%', '**', '-','and', 'or','<','>','!=','==','>=','<=']:
        return  '(' + AST_to_string(t[1]) + ' ' + t[0] + ' ' + AST_to_string(t[2]) + ')'
    elif len(t) == 3 and t[0] == 'apply':
        s = AST_to_string(t[1])
        if t[2] == None:
            return s + '()'
        else:
            return s + AST_to_string(t[2]) 
    elif len(t) == 3 and t[0] == '=':
        return  AST_to_string(t[1]) + ' = ' + AST_to_string(t[2])
    elif len(t) == 3 and t[0] == 'let':
        return '(' + listAST_to_string(t[0]) + ' ' + AST_to_string(t[1]) + ' in ' + AST_to_string(t[2]) + ')'
    elif len(t) == 3 and t[0] == 'cons':
        return listAST_to_string(t)
    elif len(t) == 3 and (t[0] == 'params' or t[0] == 'args'):
        return '(' + AST_to_string(t[1]) + ',' + AST_to_string(t[2]) + ')'
    elif len(t) == 3:
        return '(' + AST_to_string(t[0]) + ' ' + AST_to_string(t[1]) + ', ' + AST_to_string(t[2]) + ')'
    elif len(t) == 4 and t[0] == 'if':
        return '(' + t[0] + ' ' + AST_to_string(t[1]) + ' then ' + AST_to_string(t[2]) + ' else ' + AST_to_string(t[3]) + ')'
    elif len(t) == 4 and (t[0] == 'params' or t[0] == 'args'):
        return '(' + AST_to_string(t[1]) + ',' + AST_to_string(t[2]) + ',' + AST_to_string(t[3]) + ')'
    elif len(t) == 4 and t[0] == 'lambda':
        return "(\u03bb" +  AST_to_string(t[1]) + '. ' + AST_to_string(t[2]) + ' @ ' + str(t[3]) + ')'
    #else
    print("** " + str(len(t)))
    print("** " + str(t))
    return "ERROR!"


    
def listAST_to_string(L):
    if type(L) != tuple:
        return str(L)
    elif L[0] != 'cons':
        return AST_to_string(L)
    else:
        return "[" + lts_helper(L)

def lts_helper(L):
    if L == nil or L == ('nil',):
        return "]"
    elif L[2] == (nil,):     # list with one element
        return listAST_to_string(L[1]) + ']'
    else:
        return listAST_to_string(L[1]) + ',' + lts_helper(L[2])
    
def pprint_list(L):
    print(list_to_string(L))

def pprint_AST(t):
    pprint_AST_helper(t,'')

def pprint_AST_helper(t,indent):
    if t == None:
        print(indent+'()')
    elif type(t) == list:
        print(indent + str(t))
    elif (t[0] in [ident,integer,floating]):
        print(indent + '(' + t[0] + ',' + str(t[1]) + ')')
    elif (t[0] in ['True', 'False', 'nil']):
        print(indent + '(' + t[0] + ',)')
    else:
        print(indent + t[0])
        for k in range(1,len(t)):
            pprint_AST_helper(t[k],indent + '\t')    

# parse takes a list of tokens and determines if it is a 
# well-formed arithmetic expression.
# This version will also build an AST

def parse(list_of_input_tokens,rules,table,verbose=False):
    
    # add end of input marker
    list_of_input_tokens.append( (end_of_input,) )
    
    # input stack; use pop(0) to remove front item in list
    input_stack = list_of_input_tokens
    
    # parsing stack; use append to push onto end and pop() to pop from end
    parsing_stack = []
    
    if verbose:
        print('Input Tokens: ' + tokenListToString(input_stack) + '\n')
        pprint_parser(parsing_stack,input_stack) 
    
    while( len(input_stack) > 0 ):
        
        # Now we will "lookahead" at the next symbol on the input and ask the automaton what to do
        # a positive number means to shift, and a negative number -n means to reduce by rule n
        
        n = action(parsing_stack+[input_stack[0]],table)
        if n == accept:   # reduce by start rule, success
            if verbose:
                print("\nAccept!")
            return parsing_stack[-1][1] 
        elif n == err:     #  problem on stack!
            if verbose:
                print("\nERROR: No transition here:")
                pprint_parser(parsing_stack,input_stack)
            return None

        elif n > 0:     # shift 
            if verbose:
                print('\naction: ' + str(n) + '\tshift\n')
            parsing_stack.append( input_stack.pop(0)) 
        else:         # reduce by rule -n 
            if verbose:
                print('\naction: ' + str(n) + '\treduce by rule ' + str(-n) + ': ' + rule_to_string(rules[-n])+'\n')
            r = -n
            LHS = rules[r][0]
            if r in [0,1,2,14,16,18,20,27,30,34,36,38,44]:  # unary rules just pass ast up 
                (_,ast) = parsing_stack.pop()
                parsing_stack.append( (LHS[0],ast) )
                
            # Your code here for rules 3 - 6
            elif r == 3: # Top := def id ( ) : return Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop return
                parsing_stack.pop() # pop :
                parsing_stack.pop() # pop )
                parsing_stack.pop() # pop (
                t = parsing_stack.pop() # id0
                parsing_stack.pop() # pop def
                added_tuple = (assign,t,(lambdaTok,('params',),ast,[]))
                parsing_stack.append((LHS,added_tuple))
                
            elif r == 4: # Top := def id ( id ) : return Expr 
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop return
                parsing_stack.pop() # pop :
                parsing_stack.pop() # pop )
                t2 = parsing_stack.pop() # id
                parsing_stack.pop() # pop (
                t1 = parsing_stack.pop() # id0
                parsing_stack.pop() # pop def
                added_tuple = (assign,t1,(lambdaTok,('params',t2),ast,[]))
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 5: # def id ( id , id ) : return Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop return
                parsing_stack.pop() # pop :
                parsing_stack.pop() # pop )
                t3 = parsing_stack.pop() # id2
                parsing_stack.pop() # pop ,
                t2 = parsing_stack.pop() # id1
                parsing_stack.pop() # pop (
                t1 = parsing_stack.pop() # id0
                parsing_stack.pop() # pop def
                added_tuple = (assign,t1,(lambdaTok,('params',t2,t3),ast,[]))
                parsing_stack.append((LHS,added_tuple))
                
            elif r == 6: # def id ( id , id , id) : return Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop return
                parsing_stack.pop() # pop :
                parsing_stack.pop() # pop )
                t4 = parsing_stack.pop() # id3
                parsing_stack.pop() # pop ,
                t3 = parsing_stack.pop() # id2
                parsing_stack.pop() # pop ,
                t2 = parsing_stack.pop() # id1
                parsing_stack.pop() # pop (
                t1 = parsing_stack.pop() # id0
                parsing_stack.pop() # pop def
                added_tuple = (assign,t1,(lambdaTok,('params',t2,t3,t4),ast,[]))
                parsing_stack.append((LHS,added_tuple))
                
            elif r == 7:                           # Assign := id = Expr
                (_,ast) = parsing_stack.pop()      # Expr
                parsing_stack.pop()                # =
                t = parsing_stack.pop()            # id               
                parsing_stack.append( (LHS[0],(assign,t,ast) ) )
            elif r == 8:                           # Expr := if Bor then Expr else Expr
                (_,ast3) = parsing_stack.pop()     # Expr 
                parsing_stack.pop()                # else
                (_,ast2) = parsing_stack.pop()     # Expr  
                parsing_stack.pop()                # then
                (_,ast1) = parsing_stack.pop()     # Bor
                (operator,) = parsing_stack.pop()  # if
                parsing_stack.append( (LHS[0],(ifTok,ast1,ast2,ast3) ) )
                
            # Your code here for rules 9 -- 12
            
            elif r == 9: # Expr := lambda : Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop :
                parsing_stack.pop() # pop lambda
                added_tuple = (lambdaTok,('params',),ast,[])
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 10: # Expr := lambda id : Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop :
                t = parsing_stack.pop() # id1
                parsing_stack.pop() # pop lambda
                added_tuple = (lambdaTok,('params',t),ast,[])
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 11: # Expr := lambda id , id : Expr 
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop :
                t2 = parsing_stack.pop() # pop id2
                parsing_stack.pop() # pop ,
                t1 = parsing_stack.pop() # pop id1
                parsing_stack.pop() # pop lambda
                added_tuple = (lambdaTok,('params',t1,t2),ast,[])
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 12: # Expr := lambda id , id, id : Expr 
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                parsing_stack.pop() # pop :
                t3 = parsing_stack.pop() # pop id3
                parsing_stack.pop() # pop ,
                t2 = parsing_stack.pop() # pop id2
                parsing_stack.pop() # pop ,
                t1 = parsing_stack.pop() # pop id1
                parsing_stack.pop() # pop lambda
                added_tuple = (lambdaTok,('params',t1,t2,t3),ast,[])
                parsing_stack.append((LHS,added_tuple))
                
            elif r == 13:                          # Expr := let Assign in Expr  
                (_,ast2) = parsing_stack.pop()     # Expr
                parsing_stack.pop()                # in 
                (_,ast1) = parsing_stack.pop()     # Assign
                parsing_stack.pop()                # let 
                parsing_stack.append( (LHS[0],(let,ast1,ast2)) )
            elif r in [15,17,21,22,23,24,25,26,28,29,31,32,33,37]:   # binary operators
                (_,ast2) = parsing_stack.pop()
                (operator,) = parsing_stack.pop()
                (_,ast1) = parsing_stack.pop()
                parsing_stack.append( (LHS[0],(operator,ast1,ast2)) )
            elif r in [19,35]:                     # unary operators
                (_,ast) = parsing_stack.pop()      # F  | Bnot
                (operator,) = parsing_stack.pop()  # - | not
                parsing_stack.append( (LHS[0],(operator,ast)) )
            
            # Your code here for rules 39 - 42
            
            elif r == 39: # F2 := F2 ( ) => ('apply', ('id', 'f'), ('args',) )
                LHS = LHS[0]
                parsing_stack.pop() # pop )
                parsing_stack.pop() # pop (
                (_,ast0) = parsing_stack.pop() # id0
                added_tuple = (apply,ast0,('args',))
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 40: # F2 := F2 ( Expr )
                LHS = LHS[0]
                parsing_stack.pop() # pop )
                (_,ast) = parsing_stack.pop() # Expr1
                parsing_stack.pop() # pop (
                (_,ast0) = parsing_stack.pop() # id0
                added_tuple = (apply,ast0,('args',ast))
                parsing_stack.append((LHS,added_tuple))
                
            elif r == 41: # F2 := F2 ( Expr , Expr ) 
                LHS = LHS[0]
                parsing_stack.pop() # pop )
                (_,ast2) = parsing_stack.pop() # Expr2
                parsing_stack.pop() # pop ,
                (_,ast1) = parsing_stack.pop() # Expr1
                parsing_stack.pop() # pop (
                (_,ast0) = parsing_stack.pop() # id0
                added_tuple = (apply,ast0,('args',ast1,ast2))
                parsing_stack.append((LHS,added_tuple))  
            
            elif r == 42: # F2 := F2 ( Expr , Expr , Expr) 
                LHS = LHS[0]
                parsing_stack.pop() # pop )
                (_,ast3) = parsing_stack.pop() # Expr3
                parsing_stack.pop() # pop ,
                (_,ast2) = parsing_stack.pop() # Expr2
                parsing_stack.pop() # pop ,
                (_,ast1) = parsing_stack.pop() # Expr1
                parsing_stack.pop() # pop (
                (_,ast0) = parsing_stack.pop() # id0
                added_tuple = (apply,ast0,('args',ast1,ast2,ast3))
                parsing_stack.append((LHS,added_tuple)) 
            
            # Hm... I wonder where rules 51 - 53 should go??
            
            elif r in [43,45,46,47,48,49,50,51,52,53]:      # rules for values create leaf node by passing tuple up
                t = parsing_stack.pop()            
                parsing_stack.append( (LHS[0],t) )
            elif r == 54:                          # F3 := ( Expr )
                parsing_stack.pop()                # (
                (_,ast) = parsing_stack.pop()      # E
                parsing_stack.pop()                # )
                parsing_stack.append( (LHS[0],ast) )
            
            # Your code for rules 55 - 58
            elif r == 55: # F3 := [ ] 
                LHS = LHS[0]
                parsing_stack.pop() # pop ]
                parsing_stack.pop() # pop [
                added_tuple = (nil,)
                parsing_stack.append((LHS,added_tuple)) 
            
            elif r == 56: # F3 := [ EList ]
                LHS = LHS[0]
                parsing_stack.pop() # pop ]
                (_,ast) = parsing_stack.pop() # EList
                parsing_stack.pop() # pop [
                parsing_stack.append((LHS,ast)) 
            
            elif r == 57: # EList := Expr , EList
                LHS = LHS[0] 
                (_,ast2) = parsing_stack.pop() # EList
                parsing_stack.pop() # pop ,
                (_,ast1) = parsing_stack.pop() # Expr
                added_tuple = ('cons',ast1,ast2)
                parsing_stack.append((LHS,added_tuple))
            
            elif r == 58: # EList := Expr
                LHS = LHS[0]
                (_,ast) = parsing_stack.pop() # Expr
                added_tuple = ('cons',ast,('nil',))
                parsing_stack.append((LHS,added_tuple))
            
            else:
                print("parse stack error: action " + str(n))
                return None
   
        if verbose:
            pprint_parser(parsing_stack,input_stack)
            
    return None     # this will never be executed

def testParserAST(s,verbose=False):
    t = parse(lexer(s),Grammar1_1,table,verbose)
    if t == None or t == False:
        print("Error: No AST generated!")
    else:
        print('Input: ' + str(s))
        print("\nAbstract Syntax Tree:\n")
        print(AST_to_string(t)) 
        print()
        pprintAST(t)
