from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():

  # initialize your solver, you can use the 'CLP' solver 
  

  # initialize the cost matrix


  # declare the two teams and team_max


  # declare num_workers and num_tasks and assign them the correct value

  x = {}
  for i in range(num_workers):
    for j in range(num_tasks):
      x[i, j] = solver.IntVar(0, 1, '')

  # Objective function
  
  # Constraints

  # Each worker is assigned to at most 1 task.
  
  # Each task is assigned to exactly one worker.
  
  # Worker 0 has to be assigned to either task 2 or 3  
  
  # Each team takes on two tasks.
  
  #solve the model


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
