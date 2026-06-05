
from Helper import GenGraph, GenGraph_Incremental, Mapper
from pysat.solvers import Glucose3


# function to generate the clauses for R(3,3) problem
def GenClauses_three(graph_size, graph):
  clauses = [] # list to store the clauses
  for a in range(graph_size):
      for b in range(a + 1, graph_size):
          for c in range(b + 1, graph_size):

            arc_ab = Mapper(a, b, graph)
            arc_ac = Mapper(a, c, graph)
            arc_bc = Mapper(b, c, graph)

            # add the negative clauses
            # if all three arcs are negative, then we have a red triangle
            clause_negative = [-arc_ab, -arc_ac, -arc_bc]
            clauses.append(clause_negative)

            # add the positive clauses
            # if all three arcs are positive, then we have a blue triangle
            clause_positive = [arc_ab, arc_ac, arc_bc]
            clauses.append(clause_positive)
  return clauses



# funtion that given the clauses, it will check if the 
# problem is satisfiable or not using the SAT solver
def Ramsey(clauses):
  # Glucose3 is the SAT solver chosen
  with Glucose3() as solver:

      # add the clauses to the solver
      for clause in clauses:
          solver.add_clause(clause)

      # check if the problem is satisfiable
      result = solver.solve()

      if result == True:
          print("satisfiable")

          # return the solution
          model = solver.get_model()
          print("solution: ", model)
          return True

      else:
          # the solver did not find a solution, which means that the problem is unsatisfiable
          print("unsatisfiable")
          return False



# main function to find the Ramsey number for R(3,3)
n = 0
# generate the starting graph and clauses
graph = GenGraph(n) 
clauses = GenClauses_three(n, graph)
Ramsey(clauses)
n += 1

# add nodes until the problem becomes unsatisfiable to find a ramsey number for R(3,3)
while True: 
  # increase the graph size and generate the new clauses
  graph = GenGraph_Incremental(n,graph)
  clauses = GenClauses_three(n, graph)
  if (Ramsey(clauses) == False):
    break
  n += 1

# the problem is unsatisfiable, which means that we have found the Ramsey number for R(3,3)
print("unsatisfiable \nthe Ramsey numeber for R(3,3) is: ")
print (n+1)
