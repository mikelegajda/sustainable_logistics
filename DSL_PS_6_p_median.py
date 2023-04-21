"""
  P-median problem in Google CP Solver.
  Model and data from the OPL Manual, which describes the problem:
  '''
  The P-Median problem is a well known problem in Operations Research.
  The problem can be stated very simply, like this: given a set of customers
  with known amounts of demand, a set of candidate locations for warehouses,
  and the distance between each pair of customer-warehouse, choose P
  warehouses to open that minimize the demand-weighted distance of serving
  all customers from those P warehouses.
  '''
  """
from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp


def main():

  # Create the solver.
  solver = pywrapcp.Solver('P-median problem')


  # data
  p = 3

  num_customers = 6
  customers = list(range(num_customers))
  C1, C2, C3, C4, C5, C6 = customers
  num_warehouses = 4
  warehouses = list(range(num_warehouses))
  W1, W2, W3, W4 = warehouses

  demand = [100, 80, 80, 70, 20, 30]
  distance = [[2, 10, 50, 20],
              [2, 10, 52, 30],
              [50, 60, 3, 10],
              [40, 60, 1, 18],
              [30, 20, 10, 5],
              [15, 30, 20, 4]
              ]

  
  # declare variables
  open = [solver.IntVar(warehouses, 'open[%i]% % i') for w in warehouses]
  path = {}
  for c in customers:
    for w in warehouses:
      path[c, w] = solver.IntVar(0, 1, 'path[%i,%i]' % (c, w))
  path_flat = [path[c, w] for c in customers for w in warehouses]

  z = solver.IntVar(0, 1000, 'z')

  # constraints
  #Path[i,j] = 1 if customer i is allocated to be served by warehouse j
  for c in customers:
    s = solver.Sum([path[c, w] for w in warehouses])
    solver.Add(s == 1)

  solver.Add(solver.Sum(open) == p)

  for c in customers:
    for w in warehouses:
      solver.Add(path[c, w] <= open[w])

  z_sum = solver.Sum([
      demand[c] * distance[c][w] * path[c, w]
      for c in customers
      for w in warehouses
  ])
  solver.Add(z == z_sum)

  # objective
  objective = solver.Minimize(z, 1)


  # solution and search
  db = solver.Phase(open + path_flat, solver.INT_VAR_DEFAULT,
                    solver.ASSIGN_MIN_VALUE)
  solver.Solve(db)

  solver.NewSearch(db, [objective])

  num_solutions = 0
  while solver.NextSolution():
    num_solutions += 1
    print('z:', z.Value())
    print('open:', [open[w].Value() for w in warehouses])
    for c in customers:
      for w in warehouses:
        print(path[c, w].Value(), end=' ')
      print()
    print()

  print('num_solutions:', num_solutions)
  print('failures:', solver.Failures())
  print('branches:', solver.Branches())


if __name__ == '__main__':
  main()
