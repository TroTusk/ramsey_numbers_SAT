import itertools
from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType


# function to initialize a graph with a given size
def GenGraph(graph_size):

  graph_map = {}
  k = 1

  for x in range(graph_size):
    for y in range(x + 1,graph_size):
      if (x>y): # to ensure that the smaller node is always the first one in the tuple
        graph_map[(y,x)] = k
      else:
        graph_map[(x,y)] = k
      k+=1

  return graph_map


# function to add a new node to the graph and connect it to all existing nodes
def GenGraph_Incremental(new_node, graph):

  k = len(graph) + 1
  for x in range(new_node):
    graph[(x, new_node)] = k
    k+=1
  return graph


# function to get the arc between two nodes
def Mapper(x,y, graph):
  if(x>y):
    return graph[(y,x)]
  else:
    return graph[(x,y)]