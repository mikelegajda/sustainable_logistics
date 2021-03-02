from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
  solver = pywraplp.Solver.CreateSolver('CLP')

  cost = [[45, 50, 90, 80],
        [40, 70, 55, 70],
        [130, 100, 40, 90],
        [45, 80, 120, 50],
        [40, 110, 80, 95],
        [55, 90, 70, 110]]

  team1 = [0, 1, 4]
  team2 = [2, 3, 5]
  team_max = 2

  num_workers = len(cost)
  num_tasks = len(cost[1])

  x = {}
  for i in range(num_workers):
    for j in range(num_tasks):
      x[i, j] = solver.IntVar(0, 1, '')

  # Objective
  solver.Minimize(solver.Sum([cost[i][j] * x[i,j] for i in range(num_workers)
                                                  for j in range(num_tasks)]))

  # Constraints

  # Each worker is assigned to at most 1 task.
  for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

  # Each task is assigned to exactly one worker.
  for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

  # Worker 0 has to be assigned to either task 2 or 3  
  solver.Add(solver.Sum(x[0, j] for j in [2, 3]) == 1)

  # Each team takes on two tasks.
  for i in team1:
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= team_max)
  for i in team2:  
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= team_max)

  #solve the model
  sol = solver.Solve()

  print('Total cost = ', solver.Objective().Value())
  print()
  for i in range(num_workers):
    for j in range(num_tasks):
      if x[i, j].solution_value() > 0:
        print('Worker %d assigned to task %d.  Cost = %d' % (
              i,
              j,
              cost[i][j]))

  print()
  print("Time = ", solver.WallTime(), " milliseconds")

if __name__ == '__main__':
  main()
