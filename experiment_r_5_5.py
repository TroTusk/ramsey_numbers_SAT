from pysat.solvers import Cadical153
from Helper import GenGraph, GenGraph_Incremental, Mapper, GenClauses_55_init, GenClauses_55_adder


def Ramsey_55():
    N = 5 # we start from 5 nodes because K5 requires at least 5 nodes
    graph = GenGraph(N)
    clauses = GenClauses_55_init(N, graph) 
    
    # Cadical performs better for R(5,5)
    solver = Cadical153()

    # add the clauses for the first vertex for symmetry breaking
    # we can assume that the first vertex is positive connected to node 1
    arc_0_1 = Mapper(0, 1, graph)
    clauses.append([arc_0_1])
    
    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()
    if result == True:
        print("satisfiable")

        # print the solution, calculating tot_arcs is necessary to filter the arcs added by using top_id in the GenClauses
        tot_arcs = (N * (N - 1)) // 2
        clean_model = [v for v in solver.get_model() if abs(v) <= tot_arcs]
        print("solution: ", clean_model)

    else:
        print("unsatisfiable \nthe Ramsey number for R(5,5) is: ")
        print(N)
        return
  
    while True:
    
        graph = GenGraph_Incremental(N, graph)
        clauses_add = GenClauses_55_adder(N, graph)

        
        for clause in clauses_add:
            solver.add_clause(clause)

        result = solver.solve()
        
        # print solver stats to track performance
        stats = solver.accum_stats()
        print(f"N={N+1}:")
        print(f"decisions: {stats['decisions']}")
        print(f"conflicts: {stats['conflicts']}")

        if result == True:
            print("satisfiable")

           
            tot_arcs = ((N + 1) * N) // 2
            clean_model = [v for v in solver.get_model() if abs(v) <= tot_arcs]
            print("solution: ", clean_model)

        else:
            print("unsatisfiable \nthe Ramsey number for R(5,5) is: ")
            print(N+1)
            return

        N += 1
    

Ramsey_55()
