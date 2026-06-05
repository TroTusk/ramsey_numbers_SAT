from pysat.solvers import Cadical153
from Helper import GenGraph, GenGraph_Incremental, Mapper
from pysat.card import CardEnc

def GenClauses_36_init(graph_size, graph):
  clauses = []
  
  # rule for negative clauses (red)
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
        arc_ab = Mapper(a, b, graph)
        arc_ac = Mapper(a, c, graph)
        arc_bc = Mapper(b, c, graph)
        
        clauses.append([-arc_ab, -arc_ac, -arc_bc])

  # rule for positive clauses (blue)
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
        for d in range(c + 1, graph_size):
          for e in range(d + 1, graph_size):
            for f in range(e + 1, graph_size):
              
              # 6 nodes interconnected means 15 arcs
              arc_ab = Mapper(a, b, graph)
              arc_ac = Mapper(a, c, graph)
              arc_ad = Mapper(a, d, graph)
              arc_ae = Mapper(a, e, graph)
              arc_af = Mapper(a, f, graph)
              arc_bc = Mapper(b, c, graph)
              arc_bd = Mapper(b, d, graph)
              arc_be = Mapper(b, e, graph)
              arc_bf = Mapper(b, f, graph)
              arc_cd = Mapper(c, d, graph)
              arc_ce = Mapper(c, e, graph)
              arc_cf = Mapper(c, f, graph)
              arc_de = Mapper(d, e, graph)
              arc_df = Mapper(d, f, graph)
              arc_ef = Mapper(e,f ,graph)

              
              clauses.append([arc_ab, arc_ac, arc_ad, arc_ae, arc_af,
                              arc_bc, arc_bd, arc_be, arc_bf,
                              arc_cd, arc_ce, arc_cf,
                              arc_de ,arc_df ,arc_ef])
              
  return clauses

def GenClauses_36_adder(new_node, graph):
    new_clauses = []
    
    # rule for negative clauses (red)
    for a in range(new_node):
      for b in range(a + 1, new_node):
        arc_ab = Mapper(a, b, graph)
        arc_aN = Mapper(a, new_node, graph)
        arc_bN = Mapper(b, new_node, graph)
        new_clauses.append([-arc_ab, -arc_aN, -arc_bN])

    # rule for positive clauses (blue)
    for a in range(new_node):
      for b in range(a + 1, new_node):
        for c in range(b + 1, new_node):
          for d in range(c + 1, new_node):
            for e in range(d + 1, new_node):
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

              # we add the clauses for the new node with all the other nodes in the graph
              arc_aN = Mapper(a, new_node, graph)
              arc_bN = Mapper(b, new_node, graph)
              arc_cN = Mapper(c, new_node, graph)
              arc_dN = Mapper(d, new_node, graph)
              arc_eN = Mapper(e ,new_node ,graph)
              
              new_clauses.append([arc_ab ,arc_ac ,arc_ad ,arc_ae,
                                  arc_bc ,arc_bd ,arc_be,
                                  arc_cd ,arc_ce,
                                  arc_de,
                                  arc_aN ,arc_bN ,arc_cN ,arc_dN ,arc_eN])
              
    

    new_node_arcs = []

    # add the arcs of the new node to the list of arcs
    for i in range(new_node):
      new_node_arcs.append(Mapper(i, new_node, graph))



    if new_node > 5:
      # add the rule that the new node can have at most 5 arcs of the same color
      # top_id is set to a large number to avoid conflicts with existing variables
      # + (new_node * 1000) is important to avoid conflicts with previous new nodes
      sbp_clauses = CardEnc.atmost(lits=new_node_arcs, bound=5, top_id=100000 + (new_node * 1000))
      for clause in sbp_clauses.clauses:
        new_clauses.append(clause)

    min_negative = len(new_node_arcs) - 13
    
    if min_negative > 0:
      # add the rule that the new node must have at least min_negative arcs of the same color
      # top_id is set to a large number to avoid conflicts with existing variables
      sbp_clauses_min = CardEnc.atleast(lits=new_node_arcs, bound=min_negative, top_id=200000 + (new_node * 1000))
      for clause in sbp_clauses_min.clauses:
        new_clauses.append(clause)
      

    
    # adding the 18th node
    if new_node == 17:
      print("processing the 18th node")
      all_arcs = []
      # get all the arcs of the graph
      for a in range(new_node + 1):
        for b in range(a + 1, new_node + 1):
          all_arcs.append(Mapper(a, b, graph))

      # positive arcs must be between 36 and 45 
      # top_id is set to a large number to avoid conflicts with existing variables
      positive_min = CardEnc.atleast(lits=all_arcs, bound=36, top_id=500000)
      positive_max = CardEnc.atmost(lits=all_arcs, bound=45, top_id=600000)

      # add the clauses to the list of new clauses
      for clause in positive_min.clauses:
        new_clauses.append(clause)
      for clause in positive_max.clauses:
        new_clauses.append(clause)

    new_clauses.append([-Mapper(0, new_node, graph)])

    return new_clauses






def Ramsey_36():
    N = 6
    graph = GenGraph(N)
    clauses = GenClauses_36_init(N, graph)
    solver = Cadical153() # using Cadical for better performance on larger instances

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
        print(f"solution for {N+1} nodes: {model}")

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
            # we filter the model to only include the variables that correspond to arcs in the graph
            model = [v for v in solver.get_model() if abs(v) < tot_arcs]
            print(f"solution for {N+1} nodes: {model}")

        else:
            print("unsatisfiable \nthe Ramsey numeber for R(3,6) is: ")
            print(N+1)
            return

        print(N+1)
        N += 1

    

Ramsey_36()
