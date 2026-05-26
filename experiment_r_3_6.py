from pysat.solvers import Glucose3
from pysat.solvers import Cadical153
from Helper import GenGraph, GenGraph_Incremental, Mapper, GenClauses_36_init, GenClauses_36_adder



def Ramsey_36():
    N = 6
    graph = GenGraph(N)
    clauses = GenClauses_36_init(N, graph)
    #solver = Glucose3()
    solver = Cadical153()

    arc_0_1 = Mapper(0, 1, graph)
    clauses.append([arc_0_1])
    
    # add the clauses for the first vertex for symmetry breaking
    # we can assume that the first vertex is positive connected to at least 5 other vertices
    for i in range(1, 6):
        clauses.append([Mapper(0, i, graph)])
        

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
        print("unsatisfiable \nthe Ramsey numeber for R(3,6) is: ")
        print(N+1)
        return
    
    # add the clauses for the second vertex for symmetry breaking
    for i in range(1, 6):
        for j in range(i + 1, 6):
            clauses.append([-Mapper(i, j, graph)])

    while True:
    
        graph = GenGraph_Incremental(N,graph)
        clauses_add = GenClauses_36_adder(N, graph)

        

        for clause in clauses_add:
            solver.add_clause(clause)



        result = solver.solve()
        if result == True:
            print("satisfiable")

            # return the solution

            tot_arcs = ((N + 1) * N) // 2

            
            model = [v for v in solver.get_model() if abs(v) < tot_arcs]
            print(f"solution: {model}")
            #return True

        else:
            print("unsatisfiable \nthe Ramsey numeber for R(3,6) is: ")
            print(N+1)
            return

        print(N+1)
        N += 1

    

Ramsey_36()
