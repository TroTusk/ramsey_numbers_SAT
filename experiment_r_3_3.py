
from Helper import GenGraph, GenGraph_Incremental, GenClauses_three
from pysat.solvers import Glucose3

def Ramsey(clauses):
  with Glucose3() as solver:

      for clause in clauses:
          solver.add_clause(clause)


      result = solver.solve()

      if result == True:
          print("satisfiable")

          # return the solution
          model = solver.get_model()
          print("solution: ", model)
          return True

      else:
          print("unsatisfiable")
          return False

n = 0
graph = GenGraph(n)
clauses = GenClauses_three(n, graph)
Ramsey(clauses)
n += 1

while True:
  graph = GenGraph_Incremental(n,graph)
  clauses = GenClauses_three(n, graph)
  if (Ramsey(clauses) == False):
    break
  n += 1

print("unsatisfiable \nthe Ramsey numeber for R(3,3) is: ")
print (n+1)
