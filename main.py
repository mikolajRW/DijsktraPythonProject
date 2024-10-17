"""
Main purpose of the project is to find the shortest round between particular cities
In the simplified map pointed by the user
Map consists of three main elements
* - represent coordinates of the city
# - represent road
. - represent not passable coordinate
"""

from collections import defaultdict
from collections import deque

rows_vector = [0, 0, 1, -1]
column_vector = [1, -1, 0, 0]
INF = 100000


def find_city(x, y, city_list):
    for i in range(len(city_list)):
        if city_list[i][1] == x and city_list[i][2] == y:
            return city_list[i][0]


def check_if_city_is_around(map, x, y, height, width):
    store_x = deque()
    store_y = deque()
    if x - 1 >= 0 and map[x - 1][y] == '*':
        store_x.append(x-1)
        store_y.append(y)
    if x + 1 < height and map[x + 1][y] == '*':
        store_x.append(x + 1)
        store_y.append(y)
    if y - 1 >= 0 and map[x][y - 1] == '*':
        store_x.append(x)
        store_y.append(y-1)
    if y + 1 < width and map[x][y + 1] == '*':
        store_x.append(x)
        store_y.append(y + 1)

    if len(store_y) > 0:
        return True, store_x, store_y
    else:
        return False, store_y, store_y


# Explore_neighbours explores fields of the map, are they passable.
def explore_neighbours(tmp_x, tmp_y, map, width, height, visited, stack_x, stack_y, stack_points, counter, graph, city_list, city_number):
    for x in range(4):
        tmp__x = tmp_x + rows_vector[x]
        tmp__y = tmp_y + column_vector[x]

        if tmp__y < 0 or tmp__x < 0:
            continue
        if tmp__x >= height or tmp__y >= width:
            continue
        if visited[tmp__x][tmp__y]:
            continue
        if map[tmp__x][tmp__y] == '*':
            visited[tmp__x][tmp__y] = True
            graph[city_list[city_number][0]].append([find_city(tmp__x, tmp__y, city_list), counter+1, False])
            continue
        if map[tmp__x][tmp__y] != '#':
            continue

        stack_x.appendleft(tmp__x)
        stack_y.appendleft(tmp__y)
        stack_points.appendleft(counter + 1)
        visited[tmp__x][tmp__y] = True


# Execution of BFS algorithm
def create_a_graph(width, height, map, city_list):
    graph = defaultdict(list)
    for x in range(len(city_list)):
        tmp_x = city_list[x][1]
        tmp_y = city_list[x][2]
        visited = [[False for y in range(width)] for x in range(height)]
        visited[tmp_x][tmp_y] = True
        stack_x = deque()
        stack_y = deque()
        stack_points = deque()
        stack_x.append(tmp_x)
        stack_y.append(tmp_y)
        counter = 0
        stack_points.append(counter)
        while len(stack_x) > 0:
            tmp_x = stack_x.pop()
            tmp_y = stack_y.pop()
            counter = stack_points.pop()
            explore_neighbours(tmp_x, tmp_y, map, width, height, visited, stack_x, stack_y, stack_points, counter, graph, city_list, x)

    return graph


# After finding '*' in our map, program finds the exact name of the city
def find_the_nearest_city(width, map, tmp_y, tmp_x):
    while 1 > 0:
        if (tmp_y - 1 < 0 or map[tmp_x][tmp_y - 1] == '.' or map[tmp_x][tmp_y - 1] == '#'
                or map[tmp_x][tmp_y - 1] == '*'):
            break
        tmp_y -= 1

    city_name = ''
    while 1 > 0:
        city_name += map[tmp_x][tmp_y]
        if (tmp_y + 1 >= width or map[tmp_x][tmp_y + 1] == '.' or map[tmp_x][tmp_y + 1] == '#'
                or map[tmp_x][tmp_y + 1] == '*'):
            break
        tmp_y += 1

    return city_name


# Execution of dijkstra algorithm
def dijkstra(graph, city_list, start_city, end_city, type):
    # For the simplification we assigned numerical index for each city
    city_to_digit_index = defaultdict(int)
    for x in range(len(city_list)):
        city_to_digit_index[city_list[x][0]] = x

    routes = []

    # Variable 'routes' represents each city, Flag informs user if city was checked
    # INF - informs about distance from departure city
    # None - previous city

    for x in range(len(city_list)):
        routes.append([False, INF, None])

    routes[city_to_digit_index[start_city]][1] = 0
    pg = deque()
    pg.append([start_city, 0])

    while len(pg) != 0:
        name_of_the_city, value = pg.pop()
        routes[city_to_digit_index[name_of_the_city]][0] = True
        for x in range(len(graph[name_of_the_city])):
            # This conditional statement informs algorithm if we checked particular city before
            # And if it is one-way connection
            if routes[city_to_digit_index[graph[name_of_the_city][x][0]]][0] is True and not graph[name_of_the_city][x][
                2]:
                continue
            new_dist = routes[city_to_digit_index[name_of_the_city]][1] + graph[name_of_the_city][x][1]
            if new_dist < routes[city_to_digit_index[graph[name_of_the_city][x][0]]][1]:
                routes[city_to_digit_index[graph[name_of_the_city][x][0]]][1] = new_dist
                routes[city_to_digit_index[graph[name_of_the_city][x][0]]][2] = name_of_the_city
                pg.appendleft([graph[name_of_the_city][x][0], new_dist])

    shortest_path = []
    if routes[city_to_digit_index[end_city]][1] == INF:
        shortest_path = None

    if type == 1:
        guide = end_city
        guide = routes[city_to_digit_index[guide]][2]
        if guide is None:
            return routes[city_to_digit_index[end_city]][1], shortest_path
        while guide is not None:
            if guide != start_city:
                shortest_path.append(guide)
            guide = routes[city_to_digit_index[guide]][2]
        shortest_path.reverse()

    return routes[city_to_digit_index[end_city]][1], shortest_path


"""
Function 'project' is responsible for gaining data from the user about the map, possible flights and roads in which user is interested
Later on algorithm responsible for finding the shortest road is executed
"""


def project():
    width = int(input('Give me width of the map: '))
    height = int(input('Give me the height of the map: '))
    map = [0 for y in range(height)]
    print("Input your map", end = '\n')
    for x in range(height):
        map[x] = input()
    number_of_flights = int(input("Give me number of flights: "))
    list_of_flights = [0 for y in range(number_of_flights)]
    if number_of_flights != 0:
        print("Input your flights", end='\n')
    for x in range(number_of_flights):
        list_of_flights[x] = input()
    number_of_queries = int(input("Give me number of queries you want to ask: "))
    list_of_queries = [0 for y in range(number_of_queries)]
    print("Input your queries", end='\n')
    for x in range(number_of_queries):
        list_of_queries[x] = input()

    city_list = []

    # In this double loop we want to find name of the cities, with their exact coordinates
    for x in range(height):
        for y in range(width):
            if map[x][y] == '*':
                if x - 1 >= 0 and str.isalpha(map[x - 1][y]):
                    city_list.append([find_the_nearest_city(width, map, y, x - 1), x, y])
                elif x + 1 < height and str.isalpha(map[x + 1][y]):
                    city_list.append([find_the_nearest_city(width, map, y, x + 1), x, y])
                elif y - 1 >= 0 and str.isalpha(map[x][y - 1]):
                    city_list.append([find_the_nearest_city(width, map, y - 1, x), x, y])
                elif y + 1 < width and str.isalpha(map[x][y + 1]):
                    city_list.append([find_the_nearest_city(width, map, y + 1, x), x, y])
                elif x - 1 >= 0 and y - 1 >= 0 and str.isalpha(map[x - 1][y - 1]):
                    city_list.append([find_the_nearest_city(width, map, y - 1, x - 1), x, y])
                elif x + 1 < height and y - 1 >= 0 and str.isalpha(map[x + 1][y - 1]):
                    city_list.append([find_the_nearest_city(width, map, y - 1, x + 1), x, y])
                elif x + 1 < height and y + 1 < width and str.isalpha(map[x + 1][y + 1]):
                    city_list.append([find_the_nearest_city(width, map, y + 1, x + 1), x, y])
                elif x - 1 >= 0 and y + 1 < width and str.isalpha(map[x - 1][y + 1]):
                    city_list.append([find_the_nearest_city(width, map, y + 1, x - 1), x, y])

    # The 'create_a_graph' function executes the BFS algorithm, which determines the shortest route to each
    # neighboring city

    graph = create_a_graph(width, height, map, city_list)

    # Flights are added to the graph, with the flag that informs that this is one-way connection
    for x in range(number_of_flights):
        graph[list_of_flights[x].split(" ")[0]].append(
            [list_of_flights[x].split(" ")[1], int(list_of_flights[x].split(" ")[2]), True])

    start_cities = []
    end_cities = []
    type = []

    # User's queries, departure city, and arrival city are added to the lists along with an additional variable 'type'
    # type = 0: The program does not show cities passed along the route
    # type = 1: The program shows cities passed along the route

    for x in range(number_of_queries):
        start_cities.append(list_of_queries[x].split(" ")[0])
        end_cities.append(list_of_queries[x].split(" ")[1])
        type.append(int(list_of_queries[x].split(" ")[2]))

    # Execution of dijkstra algorithm, between cities pointed by the user
    for x in range(number_of_queries):
        distance, route = dijkstra(graph, city_list, start_cities[x], end_cities[x], type[x])
        if type[x] == 1:
            print(f"Distance: {distance} and route: {route}")
        else:
            print(f"Distance: {distance}")


if __name__ == '__main__':
    project()