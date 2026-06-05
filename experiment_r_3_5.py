from pysat.solvers import Glucose3
from Helper import GenGraph, GenGraph_Incremental, Mapper

# this is the function for R(3,5) problem,
# this only has a simple symmetry breaking clause,
# the faster version of R(3,5) is in experiment_r_3_5_fast.py
def GenClauses_35_init(graph_size, graph):
  clauses = []
  
  # rule for negative clauses
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):

        # 3 nodes interconnected means 3 arcs
        arc_ab = Mapper(a, b, graph)
        arc_ac = Mapper(a, c, graph)
        arc_bc = Mapper(b, c, graph)
        
        clauses.append([-arc_ab, -arc_ac, -arc_bc])

  # rule for positive clauses 
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
        for d in range(c + 1, graph_size):
          for e in range(d + 1, graph_size):

            # 5 nodes interconnected means 10 arcs
            arc_ab = Mapper(a, b, graph)
            arc_ac = Mapper(a, c, graph)
            arc_ad = Mapper(a, d, graph)
            arc_ae = Mapper(a, e, graph)
            arc_bc = Mapper(b, c, graph)
            arc_bd = Mapper(b, d, graph)
            arc_be = Mapper(b, e, graph)
            arc_cd = Mapper(c, d, graph)
            arc_ce = Mapper(c, e, graph)
            arc_de = Mapper(d, e, graph)
            
            clauses.append([arc_ab, arc_ac, arc_ad, arc_ae, arc_bc, arc_bd, arc_be, arc_cd, arc_ce, arc_de])
            
  return clauses

def GenClauses_35_adder(new_node, graph):
  new_clauses = []
  
  # rule for negative clauses
  for a in range(new_node):
    for b in range(a + 1, new_node):
      arc_ab = Mapper(a, b, graph)
      arc_aN = Mapper(a, new_node, graph)
      arc_bN = Mapper(b, new_node, graph)
      new_clauses.append([-arc_ab, -arc_aN, -arc_bN])

  # rule for positive clauses
  for a in range(new_node):
    for b in range(a + 1, new_node):
      for c in range(b + 1, new_node):
        for d in range(c + 1, new_node):
          arc_ab = Mapper(a, b, graph)
          arc_ac = Mapper(a, c, graph)
          arc_ad = Mapper(a, d, graph)
          arc_bc = Mapper(b, c, graph)
          arc_bd = Mapper(b, d, graph)
          arc_cd = Mapper(c, d, graph)
          
          # we add the clauses for the new node with all the other nodes in the graph
          arc_aN = Mapper(a, new_node, graph)
          arc_bN = Mapper(b, new_node, graph)
          arc_cN = Mapper(c, new_node, graph)
          arc_dN = Mapper(d, new_node, graph)
          
          new_clauses.append([arc_ab, arc_ac, arc_ad, arc_bc, arc_bd, arc_cd, arc_aN, arc_bN, arc_cN, arc_dN])
          
  return new_clauses




def Ramsey_35():
    N = 5
    graph = GenGraph(N)
    clauses = GenClauses_35_init(N, graph)
    solver = Glucose3()

    # symmetry breaking, we can assume that the arc between node 0 and node 1 is positive (blue)
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

    else:
        print("unsatisfiable \nthe Ramsey numeber for R(3,5) is: ")
        print(N+1)
        return
  
    

    while True:
    
        graph = GenGraph_Incremental(N,graph)
        clauses_add = GenClauses_35_adder(N, graph)

        
        # add the clauses for the new node to the solver
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
