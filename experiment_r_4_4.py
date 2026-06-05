from pysat.solvers import Glucose3
from Helper import GenGraph, GenGraph_Incremental, Mapper



# function to generate the starting clauses for R(4,4) problem
def GenClauses_44_init(graph_size, graph):
  clauses = [] # list to store the clauses
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
        for d in range(c + 1,graph_size):
        
          # (4 nodes interconnected means 6 six arcs)
          arc_ab = Mapper(a, b, graph)
          arc_ad = Mapper(a, d, graph)
          arc_ac = Mapper(a, c, graph)
          arc_bc = Mapper(b, c, graph)
          arc_bd = Mapper(b, d, graph)
          arc_cd = Mapper(c, d, graph)
          
          
          # add the negative clauses
          # if all six arcs are negative, then we have a red K4
          clause_negative = [-arc_ab, -arc_ad, -arc_ac, -arc_bc, -arc_bd, -arc_cd]
          clauses.append(clause_negative)

          # add the positive clauses
          # if all six arcs are positive, then we have a blue K4
          clause_positive = [arc_ab, arc_ad, arc_ac, arc_bc, arc_bd, arc_cd]
          clauses.append(clause_positive)
  return clauses

# function to add the clauses for the new node in R(4,4) problem
def GenClauses_44_adder(new_node, graph):
  new_clauses = []
  for a in range(new_node):
    for b in range(a + 1, new_node):
      for c in range(b + 1, new_node):

        arc_ab = Mapper(a, b, graph)
        arc_ac = Mapper(a, c, graph)
        arc_bc = Mapper(b, c, graph)

        # we add the clauses for the new node with all the other nodes in the graph
        arc_ad = Mapper(a, new_node, graph)
        arc_bd = Mapper(b, new_node, graph)
        arc_cd = Mapper(c, new_node, graph)
          
        # add the negative clauses
        clause_negative = [-arc_ab, -arc_ad, -arc_ac, -arc_bc, -arc_bd, -arc_cd]
        new_clauses.append(clause_negative)

        # add the positive clauses
        clause_positive = [arc_ab, arc_ad, arc_ac, arc_bc, arc_bd, arc_cd]
        new_clauses.append(clause_positive)
  return new_clauses





def Ramsey_44():
    # starting with 4 nodes since it is the 
    # minimum number of nodes required to have a K4
    N = 4
    # generate the graph and the clauses for the initial graph
    graph = GenGraph(N)
    clauses = GenClauses_44_init(N, graph)
    solver = Glucose3() # initialize the solver

    # first symmetry breaking clause, we can assume that 
    # the arc between node 0 and node 1 is positive (blue)
    arc_0_1 = Mapper(0, 1, graph)
    clauses.append([arc_0_1])
    
    # add the clauses to the solver
    for clause in clauses:
        solver.add_clause(clause)


    result = solver.solve()
    if result == True:
        print("satisfiable")

        # return the solution
        model = solver.get_model()
        print("solution: ", model)
        
    else:
        print("unsatisfiable \nthe Ramsey numeber for R(4,4) is: ")
        print(N+1)
        return
  
    while True:
        # increment the graph by adding a new node and the corresponding arcs
        graph = GenGraph_Incremental(N,graph)
        # add the clauses for the new node to the solver
        clauses_add = GenClauses_44_adder(N, graph)

        # add the symmetry breaking clause for the new node

        # takes the arc between node 0 and the new node N
        arc_0_N = Mapper(0, N, graph) 

        # the first 8 nodes can be blue
        # after that we can assume that the arcs between node 0 and the new node are negative (red)
        if N <= 8:
            clauses_add.append([arc_0_N])
        else:
            clauses_add.append([-arc_0_N])

        # add the symmetry breaking clause and the new other clauses to the solver
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

    

Ramsey_44()
