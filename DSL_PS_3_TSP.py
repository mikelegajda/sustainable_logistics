"""Simple travelling salesman problem between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    #cities: 0: Lausanne, 1: Geneva, 2: Zurich, 3: Bern, 4: Lugano, 5: Luzern, 6: Basel, 7: St. Gallen, 8: Chur
    data = {}
    data['distance_matrix'] = [
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

    data['num_vehicles'] = 1	

    #The index of the depot, the location where all vehicles start and end their routes.
    data['depot'] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()
