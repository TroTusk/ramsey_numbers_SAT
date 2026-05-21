from pysat.solvers import Glucose3
from Helper import GenGraph, GenGraph_Incremental, Mapper, GenClauses_35_init, GenClauses_35_adder



def Ramsey_35():
    N = 5
    graph = GenGraph(N)
    clauses = GenClauses_35_init(N, graph)
    solver = Glucose3()

    arc_0_1 = Mapper(0, 1, graph)
    clauses.append([arc_0_1])
    
    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()
    if result == True:
        print("satisfiable")

        # return the solution
        model = solver.get_model()
        print("solution: ", model)
        #return True

    else:
        print("unsatisfiable \nthe Ramsey numeber for R(3,5) is: ")
        print(N+1)
        return
  
    

    while True:
    
        graph = GenGraph_Incremental(N,graph)
        clauses_add = GenClauses_35_adder(N, graph)

        

        for clause in clauses_add:
            solver.add_clause(clause)



        result = solver.solve()
        if result == True:
            print("satisfiable")

            # return the solution
            model = solver.get_model()
            print("solution: ", model)
            #return True

        else:
            print("unsatisfiable \nthe Ramsey numeber for R(3,5) is: ")
            print(N+1)
            return

        print(N+1)
        N += 1

    

Ramsey_35()
