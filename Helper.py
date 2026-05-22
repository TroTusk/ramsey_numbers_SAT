from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType



def GenGraph(graph_size):

  graph_map = {}
  k = 1

  for x in range(graph_size):
    for y in range(x + 1,graph_size):
      if (x>y):
        graph_map[(y,x)] = k
      else:
        graph_map[(x,y)] = k
      k+=1

  return graph_map





def GenGraph_Incremental(new_node, graph):

  k = len(graph) + 1
  for x in range(new_node):
    graph[(x, new_node)] = k
    k+=1
  return graph

"""
def GenGraph_Incremental_adder(new_node, graph):

  k = len(graph) + 1
  added_arcs = {}
  for x in range(new_node):
    added_arcs[(x, new_node)] = k
    k+=1
  return added_arcs
"""


def Mapper(x,y, graph):
  if(x>y):
    return graph[(y,x)]
  else:
    return graph[(x,y)]
  



#R(3,3)
def GenClauses_three(graph_size, graph):
  clauses = []
  for a in range(graph_size):
      for b in range(a + 1, graph_size):
          for c in range(b + 1, graph_size):

              arc_ab = Mapper(a, b, graph)
              arc_ac = Mapper(a, c, graph)
              arc_bc = Mapper(b, c, graph)

              # add the negative clauses
              clause_negative = [-arc_ab, -arc_ac, -arc_bc]
              clauses.append(clause_negative)

              # add the positive clauses
              clause_positive = [arc_ab, arc_ac, arc_bc]
              clauses.append(clause_positive)
  return clauses




#R(4,4)
def GenClauses_44_init(graph_size, graph):
  clauses = []
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
        for d in range(c + 1,graph_size):

          arc_ab = Mapper(a, b, graph)
          arc_ad = Mapper(a, d, graph)
          arc_ac = Mapper(a, c, graph)
          arc_bc = Mapper(b, c, graph)
          arc_bd = Mapper(b, d, graph)
          arc_cd = Mapper(c, d, graph)
          
          # add the negative clauses
          clause_negative = [-arc_ab, -arc_ad, -arc_ac, -arc_bc, -arc_bd, -arc_cd]
          clauses.append(clause_negative)

          # add the positive clauses
          clause_positive = [arc_ab, arc_ad, arc_ac, arc_bc, arc_bd, arc_cd]
          clauses.append(clause_positive)
  return clauses


def GenClauses_44(new_node, clauses, graph):
  
  for a in range(new_node):
    for b in range(a + 1, new_node):
      for c in range(b + 1, new_node):
        

        arc_ab = Mapper(a, b, graph)
        arc_ac = Mapper(a, c, graph)
        arc_bc = Mapper(b, c, graph)
        arc_ad = Mapper(a, new_node, graph)
        arc_bd = Mapper(b, new_node, graph)
        arc_cd = Mapper(c, new_node, graph)
          
        # add the negative clauses
        clause_negative = [-arc_ab, -arc_ad, -arc_ac, -arc_bc, -arc_bd, -arc_cd]
        clauses.append(clause_negative)

        # add the positive clauses
        clause_positive = [arc_ab, arc_ad, arc_ac, arc_bc, arc_bd, arc_cd]
        clauses.append(clause_positive)

  return clauses




def GenClauses_44_adder(new_node, graph):
  new_clauses = []
  for a in range(new_node):
    for b in range(a + 1, new_node):
      for c in range(b + 1, new_node):
        
        arc_ab = Mapper(a, b, graph)
        arc_ac = Mapper(a, c, graph)
        arc_bc = Mapper(b, c, graph)
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




#R(3,5)

def GenClauses_35_init(graph_size, graph):
  clauses = []
  
  # rule for negative clauses
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
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
          
          arc_aN = Mapper(a, new_node, graph)
          arc_bN = Mapper(b, new_node, graph)
          arc_cN = Mapper(c, new_node, graph)
          arc_dN = Mapper(d, new_node, graph)
          
          new_clauses.append([arc_ab, arc_ac, arc_ad, arc_bc, arc_bd, arc_cd, arc_aN, arc_bN, arc_cN, arc_dN])
          
  return new_clauses

#R(3,6)

def GenClauses_36_init(graph_size, graph):
  clauses = []
  
  # rule for negative clauses
  for a in range(graph_size):
    for b in range(a + 1, graph_size):
      for c in range(b + 1, graph_size):
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
            for f in range(e + 1, graph_size):
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
        
    if len(new_node_arcs) > 5:
        # add the rule that the new node can have at most 5 arcs of the same color
        # top_id is set to a large number to avoid conflicts with existing variables
        # + (new_node * 1000) is important to avoid conflicts with previous new nodes
        sbp_clauses = CardEnc.atmost(lits=new_node_arcs, bound=5, top_id=100000 + (new_node * 1000))
        for clause in sbp_clauses.clauses:
            new_clauses.append(clause)

    node_arcs_len = len(new_node_arcs)
    min_negative = node_arcs_len - 13
    
    if min_negative > 0:
        # add the rule that the new node must have at least min_negative arcs of the same color
        sbp_clauses_min = CardEnc.atleast(lits=new_node_arcs, bound=min_negative, top_id=200000 + (new_node * 1000))
        for clause in sbp_clauses_min.clauses:
            new_clauses.append(clause)
        print("bruhhh")

    return new_clauses


