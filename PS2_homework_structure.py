from __future__ import print_function
from ortools.sat.python import cp_model
import time
import numpy as np

def main():
  # define model: you can use CpModel()

  start = time.time()
  impact = [
          [30, 45, 40, 50, 70, 90, 110, 100],
          [35, 50, 45, 66, 79, 100, 130, 90],
          [40, 60, 50, 70, 80, 90, 100, 90],
          [55, 65, 60, 80, 90, 110, 60, 80],
          [79, 80, 60, 90, 105, 120, 80, 97],
          [86, 90, 80, 95, 110, 130, 90, 100],
          [90, 100, 90, 148, 103, 140, 95, 110],
          [180, 190, 110, 159, 116, 190, 140, 130],
          [200, 260, 180, 170, 150, 200, 180, 190],
          [200, 270, 260, 200, 170, 210, 200, 190]]


  # Variables

  # Constraints


  # define objective function and solve the model

  if status == cp_model.OPTIMAL:
    print('Minimum impact = %i' % solver.ObjectiveValue())
    print()

    for i in range(num_vehicles):

      for j in range(num_deliveries):

        if solver.Value(x[i][j]) == 1:
          print('Vehicle ', i, ' performs delivery ', j, '  Km = ', impact[i][j])
    print()
    end = time.time()
    print("Time = ", round(end - start, 4), "seconds")


if __name__ == '__main__':
  main()
