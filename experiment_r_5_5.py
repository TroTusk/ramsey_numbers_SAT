from pysat.solvers import Cadical153
from Helper import GenGraph, GenGraph_Incremental, Mapper
from pysat.card import CardEnc
import itertools

def GenClauses_55_adder(new_node, graph):
    new_clauses = []
    
    # choose 4 nodes
    # use itertools.combinations to easily get all the combinations of 4 nodes from the existing graph
    for clique in itertools.combinations(range(new_node), 4):
        
        # group is formed by the new node and 4 nodes
        full_clique = list(clique) + [new_node]
        
        neg_clause = []
        pos_clause = []
        
        # get all the arcs between these 5 nodes
        for i, j in itertools.combinations(full_clique, 2):
            arc = Mapper(i, j, graph)
            
            neg_clause.append(-arc)
            
            pos_clause.append(arc)
            
        new_clauses.append(neg_clause)
        new_clauses.append(pos_clause)
        
    new_node_arcs = [Mapper(i, new_node, graph) for i in range(new_node)]
    

    # with the knowledge of R(4,5) = 25, 
    # we can set that the graph must have atmost 24 arcs of the same color
    if len(new_node_arcs) > 24:
        sbp_max = CardEnc.atmost(lits=new_node_arcs, bound=24, top_id=100000 + (new_node * 1000))
        for clause in sbp_max.clauses:
            new_clauses.append(clause)
            
    min_archi = len(new_node_arcs) - 24
    if min_archi > 0:
        sbp_min = CardEnc.atleast(lits=new_node_arcs, bound=min_archi, top_id=200000 + (new_node * 1000))
        for clause in sbp_min.clauses:
            new_clauses.append(clause)

    return new_clauses


def GenClauses_55_init(N, graph):
    new_clauses = []
    
    # choose 5 nodes directly from the initial N nodes
    for clique in itertools.combinations(range(N), 5):
        
        neg_clause = []
        pos_clause = []
        
        # get all the 10 arcs between these 5 nodes
        for i, j in itertools.combinations(clique, 2):
            arc = Mapper(i, j, graph)
            
            # adding negative clauses
            neg_clause.append(-arc)
            
            # adding positive clauses
            pos_clause.append(arc)
            
        new_clauses.append(neg_clause)
        new_clauses.append(pos_clause)
        
    return new_clauses


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
        

        if result == True:
            print("satisfiable")

            # print the solution, calculating tot_arcs is necessary to filter the arcs added by using top_id in the GenClauses
            tot_arcs = ((N + 1) * N) // 2
            clean_model = [v for v in solver.get_model() if abs(v) <= tot_arcs]
            print("solution: ", clean_model)

        else:
            print("unsatisfiable \nthe Ramsey number for R(5,5) is: ")
            print(N+1)
            return

        N += 1
    

Ramsey_55()
