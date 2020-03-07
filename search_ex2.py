import numpy
import queue
# Matthew Mabrey
# Homework 2 for Artificial Intelligence
# 1.2 Implementation of an optimal algorithm that always finds the goal with shortest path
# CSC-380-01 Dr. Yoon
# February 22nd 2020
#

target_c = 0
target_r = 0
p_que = queue.PriorityQueue()
path_to_goal = []
sample_move_grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 0],
                    [4, 6, 4, 4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                    [1, 6, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 6, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [4, 4, 4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 4, 0],
                    [1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 0],
                    [1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 0],
                    [4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 4, 4, 4, 0],
                    [1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 0],
                    [1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 0],
                    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]
visited = numpy.zeros_like(sample_move_grid)


# Class Node used to store parent_node, the path cost to get to this node so far, and the row/column of this node
# to back track when it's f_val is the lowest in the priority queue
class Node:
    def __init__(self, parent_node, path_cost, row, col):
        self.parent_node = parent_node
        self.path_cost = path_cost
        self.row = row
        self.col = col
        # f_val is equal to the current path cost so far plus the heuristic value for this node
        self.f_val = path_cost + heuristic_value(row, col)


# Find_target_location method is used to get the row and column location of the target in the grid
# so that we can use it in the heuristic method to get a heuristic value for any given node
def find_target_location(move_grid, target):

    for row in move_grid:
        if row.__contains__(target):
            global target_r
            target_r = move_grid.index(row)
            global target_c
            target_c = row.index(target)
            break

    return


# The heuristic value gives the smallest possible number of moves from the given node to the target node
def heuristic_value(cur_r, cur_c):

    # Getting the absolute value of the (row distance difference) and the (column distance difference)
    h_val = abs(target_r - cur_r) + abs(target_c - cur_c)

    return h_val


def find_path(move_grid, cur_r, cur_c, target):

    find_target_location(move_grid, target)

    # if the find_target_location left target_r and target_c at their initial 0 values, then exit
    if target_r == 0 and target_c == 0:
        print("No target found in the grid!")
    else:

        target_node = search_move_grid(move_grid, cur_r, cur_c, target)

        # retrace the best path by going back to every parent node and store it
        while target_node is not None:
            path_to_goal.insert(0, target_node)
            target_node = target_node.parent_node

        # print all of the (rows, columns) of the path_to_goal
        for n in path_to_goal:
            print("(", n.row, ",", n.col, ")")
            visited[n.row][n.col] = 2

        # print the grid of the best path and the searched path
        print("Final Search Grid (X = best path, O = searched path)")
        for row in visited:

            for col in row:
                if col == 0:
                    print(".", end=" ")
                elif col == 1:
                    print("O", end=" ")
                elif col == 2:
                    print("X", end=" ")
            print("|")

    return


# Search_move_grid uses A* Search to find the path of optimal length by using a priority queue (p_que)
# to select which node gets expanded next. Each while loop adds all possible next nodes to the p_que and
# then selects the least cost node (the head node) from the p_que and makes that the next parent_node
# The priority queue values are equal to the total path cost to get to that node so far, plus the heuristic
# value of that node. The node_count is the second value compared if two heuristic values are equal.
def search_move_grid(move_grid, cur_r, cur_c, target):

    row = cur_r
    col = cur_c

    # target -> found the goal!
    # 0 -> always move left
    # 1 -> move only left and right (cannot go to 0)
    # 6 -> move only up or down (cannot go to 4)
    # See homework description for details.

    # boolean variable to stop searching if once the target is reached
    target_found = False
    # initializing parent_node to current space with no parent
    parent_node = Node(None, 0, row, col)
    # node count to use in priority queue (p_que) for comparisons of nodes with equal f_vals
    node_count = 0

    while not target_found:

        if 0 <= row <= 11 and 0 <= col <= 19:

            visited[row][col] = 1

            if move_grid[row][col] == target:
                print("TARGET REACHED")
                print("Goal Path:")
                target_found = True
                return parent_node
            elif move_grid[row][col] == 0:
                # if currently on a 0 space, always move left
                node = Node(parent_node, 0, row, col - 1)
                p_que.put((node.f_val, node_count, node))
                node_count = node_count + 1

            elif move_grid[row][col] == 1:
                # if the space to the left is unvisited, then move left
                if visited[row][col - 1] == 0:
                    node = Node(parent_node, parent_node.path_cost + 1, row, col - 1)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

                # if space to the right is unvisited, not equal to 0, and target is yet to be found, then move right
                if visited[row][col + 1] == 0 and move_grid[row][col + 1] != 0 and not target_found:
                    node = Node(parent_node, parent_node.path_cost + 1, row, col + 1)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

                # if space below is unvisited, equal to 6, and target is yet to be found, then move down
                if visited[row + 1][col] == 0 and move_grid[row + 1][col] == 6 and not target_found:
                    node = Node(parent_node, parent_node.path_cost + 1, row + 1, col)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

            elif move_grid[row][col] == 6:

                # if space above is unvisited and we're currently on a 6 space, then move up
                if visited[row - 1][col] == 0:
                    node = Node(parent_node, parent_node.path_cost + 1, row - 1, col)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

                # if space below is unvisited, not equal to 4, and target is yet to be found, then move down
                if visited[row + 1][col] == 0 and move_grid[row + 1][col] != 4 and not target_found:
                    node = Node(parent_node, parent_node.path_cost + 1, row + 1, col)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

                # if space to the left is unvisited, above a 4 space, and target is yet to be found, the move left
                if visited[row][col - 1] == 0 and move_grid[row + 1][col - 1] == 4 and not target_found:
                    node = Node(parent_node, parent_node.path_cost + 1, row, col - 1)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

                # if space to the right is unvisited, above a 4 space, and the target isn't found, then move right
                if visited[row][col + 1] == 0 and move_grid[row + 1][col + 1] == 4 \
                        and move_grid[row][col + 1] != 0 and not target_found:
                    node = Node(parent_node, parent_node.path_cost + 1, row, col + 1)
                    p_que.put((node.f_val, node_count, node))
                    node_count = node_count + 1

        # if the priority queue is empty then no possible next steps were found, so return None
        if p_que.empty():
            print("No target found!")
            return None
        else:
            # get the least cost node from the p_que (the head node) and make that the parent_node for the next nodes
            parent_node = p_que.get()[2]

            # set the row and col to this new parent nodes row and col
            # so we "move" to that nodes location for the next while loop
            row = parent_node.row
            col = parent_node.col


if __name__ == "__main__":
    # initial = (10, 19)
    # target = 8

    find_path(sample_move_grid, 10, 19, 8)


