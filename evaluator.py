## Evaluator for ASTs:      

# eval(t,env,memory) takes an abstract syntax tree, an environment, and a global memory and evaluates
# the term in the context of the bindings in env, which is a stack, so
# the first occurrence of the binding is the one that is used; if a variable
# is not found in the env, it is looked for in the global memory; if not there
# an unbound variable exception is raised

# global memory is a dictionary of bindings, e.g., { 'x': 4.5, 'y':-1 }

# bindings are in the form of a tuple (str,value), e.g., ('x',4.5) so
# environment is a list of bindings, e.g., [ ('x',4.5), ('y',-1), ('x',4) ]

# for efficiency, env stack grows from left to right, so push binding on env for
# the recursive call by using env + [binding]

# Use the following for errors with unbound variables

class UnboundVariableException(Exception):
    def __init__(self, name):
        self.name = name
        
class FunctionTypeException(Exception):
    def __init__(self, name):
        self.name = name

class ArgumentMismatchException(Exception):
    def __init__(self, name):
        self.name = name

# Your code here for the two additional exceptions


# look up a variable id (the string representation, not the whole token) in the
# environment from end of list to beginning; if not there, look in memory, if
# not there, raise an exception:   raise UnboundVariableException(name) 

def lookup(name,env,memory):
    for i in range(len(env)-1,-1,-1):
        if(name == env[i][0]):
            return env[i][1]
    if name in memory:
        return memory[name]
    else:
        raise UnboundVariableException(name)       


def eval(t,env,memory):
    #print(AST_to_string(t) + '\t' + str(env))     # to debug
    
    if t[0] in['nil','first','rest']:                  # nil is nil!
        return  t
    elif t[0] == 'True':
        return  1
    elif t[0] == 'False':
        return  0
    elif t[0] in ['int','float']:
        return t[1]
    elif t == ('cons',):
        return t
    
    # Your code here to deal with ('cons',), ('first',), and ('rest',) as explained above
    
    elif t[0] == 'id':                   # identifier, so must look up in env then global memory
        return  lookup(t[1],env,memory)
    elif t[0] == '+':
        return eval(t[1],env,memory) + eval(t[2],env,memory)
    elif t[0] == '*':
        return eval(t[1],env,memory) * eval(t[2],env,memory)
    elif t[0] == '-' and len(t) == 3:
        return eval(t[1],env,memory) - eval(t[2],env,memory)
    elif t[0] == '-' and len(t) == 2:
        return -eval(t[1],env,memory)
    elif t[0] == '/':
        return eval(t[1],env,memory) / eval(t[2],env,memory)
    elif t[0] == '%':
        return eval(t[1],env,memory) % eval(t[2],env,memory)
    elif t[0] == '**':
        return eval(t[1],env,memory) ** eval(t[2],env,memory)
    elif t[0] == 'and':
        res = eval(t[1],env,memory) and eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == 'or':
        res = eval(t[1],env,memory) or eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == 'not':
        res = not eval(t[1],env,memory)
        return 1 if res else 0
    elif t[0] == '<':
        res = eval(t[1],env,memory) < eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '>':
        res = eval(t[1],env,memory) > eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '<=':
        res = eval(t[1],env,memory) <= eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '>=':
        res = eval(t[1],env,memory) >= eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '==':
        res = eval(t[1],env,memory) == eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '!=':
        return eval(t[1],env,memory) != eval(t[2],env,memory)
        return 1 if res else 0
    elif t[0] == '=':                    # assignment expression
        val = eval(t[2],env,memory)
        memory[t[1][1]] = val
        return  val
    elif t[0] == 'if':                   # if-then-else
        (_,test,then_exp,else_exp) = t
        return  eval(then_exp,env,memory) if eval(test,env,memory) else eval(else_exp,env,memory) 
    elif t[0] == 'let':                  # let expression, so must extend env with new binding
        (_,(_,(_,var),exp1),exp2) = t
        binding = (var,eval(exp1,env,memory))
        return  eval(exp2,env + [binding],memory)
    
    # Your code here to deal with t[0] being 'cons', args', or 'apply'
    # You probably want to deal with 'params' inside the apply, but you could do them
    #     separately in the main list of cases
    elif t[0] == 'lambda':
        (_,v,b,e) = t
        return ('lambda',v,b,env+e)
    
    elif t[0] == 'args':
        if len(t) == 1:
            return ('args',)
        elif len(t) == 2:
            return ('args',eval(t[1],env,memory))
        elif len(t) == 3:
            return ('args',eval(t[1],env,memory),eval(t[2],env,memory))
        elif len(t) == 4:
            return ('args',eval(t[1],env,memory),eval(t[2],env,memory),eval(t[3],env,memory))

    elif t[0] == 'cons':
        return ('cons',eval(t[1],env,memory),eval(t[2],env,memory))
    
    elif t[0] == 'apply':       
        (_,f,a) = t
        func = eval(f,env,memory)
        args = eval(a,env,memory)
        
        if type(func) != tuple or func[0] not in ['lambda','cons','first','rest']:
            raise FunctionTypeException("Function Type Error")

        elif func[0] == 'lambda':
            if len(func[1]) != len(args):
                raise ArgumentMismatchException("Argument Mismatch Error")
            elif len(func[1]) == 4: # three id
                (_,(_,(_,name1),(_,name2),(_,name3)),body,e) = func
                return eval(body,env+e+[(name1,args[1])]+[(name2,args[2])]+[(name3,args[3])],memory)
            elif len(func[1]) == 3: # two id
                (_,(_,(_,name1),(_,name2)),body,e) = func
                return eval(body,env+e+[(name1,args[1])]+[(name2,args[2])],memory)
            elif len(func[1]) == 2: # one id
                (_,(_,(_,name1)),body,e) = func
                return eval(body,env+e+[(name1,args[1])],memory)
            elif len(func[1]) == 1: # zero id
                (_,(_,),body,e) = func
                return eval(body,env+e,memory)
        
        elif func == ('cons',):
            return ('cons',args[1],args[2])
        
        elif func == ('first',):
            return (args[1][1])
        
        elif func == ('rest',):
            return (args[1][2])
        
    else:
        return t

