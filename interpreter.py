# Basic Interpreter

# to catch an exception, use something like this:
#            try:
#                print("Out["+str(lineNum)+"]: " + str(eval(t,[])))
#            except UnboundVariableException as n:
#                print("Unbound Variable: " + str(n))

lineNum = 1

global_memory = { }

s = input("\nMyPython 1.2\nInput equation or type \"quit\" to quit:\n\nIn ["+str(lineNum)+"]: ")

while True:
    if s == "":
        pass
    elif s == 'quit':      
        print("\nBye!")
        break
    elif s == "global":
        print(global_memory)
    else:
        t = parse(lexer(s), Grammar1_2, table, False)
        
        if t == None:
            print("\nError, try again!")
        else:
            try:
                print("Out["+str(lineNum)+"]: " + AST_to_string(eval(t,[],global_memory)))
            except UnboundVariableException as n:
                print("Unbound Variable: " + str(n))
            
            except FunctionTypeException as n:
                print("Function Type Error: " + str(s))
            
            except ArgumentMismatchException as n:
                print("Argument Mismatch Error: " + str(s))
            
            # Your code here to deal with the other two exceptions
                      

    lineNum += 1
    s = input("\nIn ["+str(lineNum)+"]: ")

