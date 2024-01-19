# You can modify this file to implement your own algorithm

from constants import *
import heapq
"""
You can use the following values from constants.py to check for the type of cell in the grid:
I = 1 -> Wall 
o = 2 -> Pellet (Small Dot)
e = 3 -> Empty
"""
# I = 1 
# o = 2
# e = 3
# O = 4
# n = 5
# c = 6
                          
def heuristic(a, b, grid):
    (x1, y1) = a
    (x2, y2) = b
    basic_cost = abs(x1 - x2) + abs(y1 - y2)
    return basic_cost 

def legal_direction(location, grid):
    x, y = location
    directions = [(0, 1), (0, -1), (-1, 0),  (1, 0)]  # Down, Right, Up, Left
    legal_d = []
    for d in directions:
        dx, dy = x + d[0], y + d[1]
        if 0 <= dx < len(grid) and 0 <= dy < len(grid[0]) and grid[dx][dy] != I and grid[dx][dy] != n:
            legal_d.append((dx, dy))
    return legal_d

def find_all_pellets(grid):
    pellets = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == o:
                pellets.append((i, j))
    return pellets

def a_star(start, goal, grid):
    """A* algorithm"""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal, grid)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current) 
                current = came_from[current]
            return path[::-1]  # Reversed path

        for neighbor in legal_direction(current, grid):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal,grid)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None

def find_nearest_pellet(grid, start, pellets):
    nearest_pellet = None
    shortest_path_length = float('inf')
    shortest_path = []

    for pellet in pellets:
        path = a_star(start, pellet, grid)
        if path and len(path) < shortest_path_length:
            shortest_path_length = len(path)
            nearest_pellet = pellet
            shortest_path = path

    return nearest_pellet, shortest_path

def get_next_coordinate(grid, location):
    """
    Calculate the next coordinate for 6ix-pac to move to.
    Check if the next coordinate is a valid move.

    Parameters:
    - grid (list of lists): A 2D array representing the game board.
    - location (list): The current location of the 6ix-pac in the form (x, y).

    Returns:
    - list or tuple: 
        - If the next coordinate is valid, return the next coordinate in the form (x, y) or [x,y].
        - If the next coordinate is invalid, return None.
    """    
    pallets = find_all_pellets(grid)
    nearest_pellet, shortest_path = find_nearest_pellet(grid, location, pallets)
    if nearest_pellet is None:
        return None 
    if shortest_path:
        return shortest_path[0]
    else:
        return None
    