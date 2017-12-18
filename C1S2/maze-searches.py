
maze = {'in': set([1]),
        1: set(['in',4]),
        2: set([3,5]),
        3: set([2,6]),
        4: set([1,5]),
        5: set([2,4,8]),
        6: set([3]),
        7: set([8]),
        8: set([5,7,9]),
        9: set([8,'out']),
        'out': set([9])}


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    #return visited

dfs(maze, 'in') # in 1 4 5 2 3 6 8 7 9 out



def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            queue.extend(sorted(graph[vertex] - visited))
    #return visited

bfs(maze, 'in') # in 1 4 5 2 8 3 7 9 6 out
