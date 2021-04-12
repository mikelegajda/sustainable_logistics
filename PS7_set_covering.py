"""
  Set covering in Google CP Solver.
  Given 9 Swiss cities and the distance matrix between them, decide where to open warehouses
   to be able to serve all the cities within 120km. We want to minimize the number of warehouses to open.
"""
from __future__ import print_function
from ortools.sat.python import cp_model as cp


def main(unused_argv):
    model = cp.CpModel()

    # data
    min_distance = 120
    num_cities = 9
    #cities: 0: Lausanne, 1: Geneva, 2: Zurich, 3: Bern, 4: Lugano, 5: Luzern, 6: Basel, 7: St. Gallen, 8: Chur

    distance = [
        [0, 64, 229, 109, 378, 110, 201, 304, 346],
        [64, 0, 280, 161, 370, 266, 253, 360, 398],
        [229, 280, 0, 124, 205, 53, 86, 86, 120],
        [109, 161, 124, 0, 277, 110, 96, 204, 241],
        [378, 370, 205, 277, 0, 167, 262, 248, 146],
        [110, 266, 53, 110, 167, 0, 97, 144, 142],
        [201, 253, 86, 96, 262, 97, 0, 170, 204],
        [304, 360, 86, 204, 248, 144, 170, 0, 104],
        [346, 398, 120, 241, 146, 142, 204, 104, 0],
    ]

    
    # declare variables
    x = [model.NewIntVar(0, 1, "x[%i]" % i) for i in range(num_cities)]
    z = model.NewIntVar(0, num_cities, "z")

    # objective to minimize
    model.Add(z == sum(x))


    # constraints
    
    # ensure that all cities are covered
    for i in range(num_cities):
        model.Add(sum([x[j] for j in range(num_cities) if distance[i][j] <= min_distance]) >= 1)

    model.Minimize(z)

    # solution and search
    solver = cp.CpSolver()
    status = solver.Solve(model)

    if status == cp.OPTIMAL:
        print("z:", solver.Value(z))
        print("x:", [solver.Value(x[i]) for i in range(num_cities)])

    print("NumConflicts:", solver.NumConflicts())
    print("NumBranches:", solver.NumBranches())

if __name__ == "__main__":
  main("cp sample")

