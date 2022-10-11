from ortools.linear_solver import pywraplp

# Returns solution differently based on its type and value
def SolVal(x):
  if type(x) is not list:
    if (x is None):
      return 0
    elif (isinstance(x,(int,float))):
      return x
    elif (x.Integer() is False):
      return x.SolutionValue()
    else:
      return int(x.SolutionValue())
  elif type(x) is list:
    return [SolVal(e) for e in x]

def solve_model_eliminate(D, Subtours=[]):
  
  s = pywraplp.Solver.CreateSolver('CBC')
  n = len(D)
  x = [[s.IntVar(0, 0 if D[i][j] == 0 else 1,'')
        for j in range(n)] for i in range(n)] 

  # Basic constraints: 
  # - one only predecessor; 
  # - one only successor; 
  # - no route between same node -> xii=0
  for i in range(n):  
    s.Add(sum(x[i][j] for j in range(n)) == 1) 
    s.Add(sum(x[j][i] for j in range(n)) == 1) 
    s.Add(x[i][i] == 0)

 # Subtour constraint: The key to the elimination is to realize that 
 # for any strict subset of the nodes, 
 # the number of chosen arcs must be less than the number of nodes
  for sub in Subtours:
    # summing over K returns the number of chosen arcs
    K = [x[sub[i]][sub[j]]+x[sub[j]][sub[i]]
         for i in range(len(sub)-1) for j in range(i+1, len(sub))]
    # Adding constraint: number of arcs in subtour is <= number of nodes
    s.Add(sum(K) <= len(sub)-1)

  # Objective function
  s.Minimize(s.Sum(x[i][j]*(0 if D[i][j] is None else D[i][j]) 
                   for i in range(n) for j in range(n))) 
  status = s.Solve()
  tours = extract_tours(SolVal(x), n) 
  print("Tours:", tours)
  return status, s.Objective().Value(), tours

def extract_tours(R, n):
  node = 0
  tours = [[0]]
  allnodes = [0]+[1]*(n-1)
  # We iterate until the number of tours returned by the solver is one, 
  # taking care to accumulate subtours as they are discovered
  while sum(allnodes) > 0:
    #Another way of writing this for loop -> next = [i for i in range(n) if R[node][i]==1][0]
    for i in range(n):
      if R[node][i]==1:
        next = [i][0]
    if next not in tours[-1]:
      tours[-1].append(next)
      node = next
    else:
      node = allnodes.index(1)
      tours.append([node])
    allnodes[node] = 0
  return tours

def solve_model(D):
  subtours, tours = [], []
  while len(tours) != 1:
    status, Value, tours = solve_model_eliminate(D, subtours)
    if status == pywraplp.Solver.OPTIMAL:
      # [0,1,2].extend([3,4]) = [0,1,2,3,4]
      subtours.extend(tours)
  return status, Value, tours[0]

def main():
  D = [[0, 64, 229, 109, 378, 110, 201, 304, 346],
  [64, 0, 280, 161, 370, 266, 253, 360, 398],
  [229, 280, 0, 124, 205, 53, 86, 86, 120],
  [109, 161, 124, 0, 277, 110, 96, 204, 241],
  [378, 370, 205, 277, 0, 167, 262, 248, 146],
  [110, 266, 53, 110, 167, 0, 97, 144, 142],
  [201, 253, 86, 96, 262, 97, 0, 170, 204],
  [304, 360, 86, 204, 248, 144, 170, 0, 104],
  [346, 398, 120, 241, 146, 142, 204, 104, 0],
    ]
  status, value, tour = solve_model(D)

  if status == pywraplp.Solver.OPTIMAL:
      print('Objective value =', value)
      print('Solution =', tour)
  else:
      print('The problem does not have an optimal solution.')

main()
