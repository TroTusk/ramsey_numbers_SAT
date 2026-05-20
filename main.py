from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType

from Helper import GenGraph, GenGraph_Incremental, GenGraph_Incremental_adder, Mapper, GenClauses_three, GenClauses_four_init, GenClauses_four_adder



def Ramsey_four():
    N = 0
    graph = GenGraph(N)
    clauses = GenClauses_four_init(N, graph)
    solver = Glucose3()
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
        print("unsatisfiable")
        return False
  
    N += 1

    while True:
    
        graph = GenGraph_Incremental(N,graph)
        clauses_add = GenClauses_four_adder(N, graph)
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
            print("unsatisfiable")
            print(N)
            return False

        print(N)
        N += 1

    

Ramsey_four()
