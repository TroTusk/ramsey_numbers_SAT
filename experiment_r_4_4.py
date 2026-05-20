from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType

from Helper import GenGraph, GenGraph_Incremental, GenGraph_Incremental_adder, Mapper, GenClauses_three, GenClauses_four_init, GenClauses_four_adder



def Ramsey_four():
    N = 4
    graph = GenGraph(N)
    clauses = GenClauses_four_init(N, graph)
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
        print("unsatisfiable \nthe Ramsey numeber for R(4,4) is: ")
        print(N+1)
        return
  
    

    while True:
    
        graph = GenGraph_Incremental(N,graph)
        clauses_add = GenClauses_four_adder(N, graph)

        arc_0_N = Mapper(0, N, graph)

        if N <= 8:
            clauses_add.append([arc_0_N])
        else:
            clauses_add.append([-arc_0_N])


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
            print("unsatisfiable \nthe Ramsey numeber for R(4,4) is: ")
            print(N+1)
            return

        print(N+1)
        N += 1

    

Ramsey_four()
