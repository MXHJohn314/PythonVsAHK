"""
Assign 04 - <INSERT YOUR NAME HERE>

Directions:
    * Complete the graph algorithm functions given below. Note that it may be
      helpful to define auxiliary/helper functions that are called from the
      functions below.  Refer to the README.md file for additional info.

    * NOTE: As with other assignments, please feel free to share ideas with
      others and to reference sources from textbooks or online. However, do your
      best to attain a reasonable grasp of the algorithm that you are
      implementing as there will very likely be questions related to it on
      quizzes/exams.

    * NOTE: Remember to add a docstring for each function, and that a reasonable
      coding style is followed (e.g. blank lines between functions).
      Your program will not pass the tests if this is not done!
"""

# for timing checks
import queue
import time


def adjMatFromFile(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    print(f" n_verts = {n_verts}")
    adjmat = [[None] * n_verts for i in range(n_verts)]
    for i in range(n_verts):
        adjmat[i][i] = 0
    for line in f:
        int_list = [int(i) for i in line.split()]
        vert = int_list.pop(0)
        assert len(int_list) % 2 == 0
        n_neighbors = len(int_list) // 2
        neighbors = [int_list[n] for n in range(0, len(int_list), 2)]
        distances = [int_list[d] for d in range(1, len(int_list), 2)]
        for i in range(n_neighbors):
            adjmat[vert][neighbors[i]] = distances[i]
    f.close()
    return adjmat


def verify_connection(n, dict_):
    q = queue.Queue()
    [q.put(i[0:2]) for i in dict_["solution"]]
    unvisited = [i for i in range(n)]
    while q and len(unvisited) != 0:
        edge = q.get()
        if edge[0] in unvisited:
            unvisited.remove(edge[0])
        if edge[1] in unvisited:
            unvisited.remove(edge[1])
    if len(unvisited) != 0:
        Exception(f"The following tree is not fully connected:\n{dict_}")
    return dict_


def prim(W):
    """ Carry out Prim's algorithm using W as a weight/adj matrix. """
    start = time.time()
    visited = {0}
    solution = []
    unvisited = [_ for _ in range(1, len(W))]
    edges = {}
    for i in range(len(W)):
        edges[i] = sorted([(i, j, W[i][j]) for j in range(len(W))
                           if j != i and j not in visited and W[i][j]],
                          key=lambda x: x[2], reverse=True)
    while unvisited:
        min_edge = min([item for item in edges.items() if item[0] in visited and len(item[1]) > 0],
                       key=lambda x: x[1][-1][2])[1].pop()
        solution.append(min_edge)
        unvisited.remove(min_edge[1])
        visited.add(min_edge[1])
        [edge_list.remove(edge) for vertex, edge_list in edges.items() for edge in edge_list
         if edge[1] in visited]
    speed = time.time() - start
    return {
        "solution": solution,
        "cost": sum([i[2] for i in solution]),
        "time": speed
    }


def kruskal(w):
    """ Carry out Kruskal's using W as a weight/adj matrix. """
    start = time.time()
    solution = []
    sets = [{i} for i in range(len(w))]
    edges = sorted([(i, j, w[i][j]) for i in range(len(w))
                    for j in range(len(w)) if w[i][j] and i != j], key=lambda x: x[2])
    i = 0
    while len(sets) > 1:
        min_edge = edges[i]
        min_set = next((x for x in sets if min_edge[0] in x), None)
        while min_edge[0] in min_set and min_edge[1] in min_set:
            i += 1
            if i == len(edges):
                break
            min_edge = edges[i]
            min_set = next((x for x in sets if min_edge[0] in x), None)
        solution.append(min_edge)
        set1 = next((x for x in sets if min_edge[0] in x), None)
        set2 = next((x for x in sets if min_edge[1] in x), None)
        sets.remove(set1)
        sets.remove(set2)
        sets.append(set1 | set2)
    speed = time.time() - start
    return {
        "solution": solution,
        "cost": sum([i[2] for i in solution]),
        "time": speed
    }


def run_algorithms(fileName):
    graph = adjMatFromFile(fileName)
    return {
        'name': fileName[0:-4],
        'krus': verify_connection(len(graph), kruskal(graph)),
        'prim': verify_connection(len(graph), prim(graph)),
    }


def print_results(res):
    return f"""
{res["name"]}: {"{"}
 krus: {"{"}
  cost: {res["krus"]["cost"]}
  time: {res["krus"]["time"]}
 {"}"}
 prim: {"{"}
  cost: {res["prim"]["cost"]}
  time: {res["prim"]["time"]}
 {"}"}
{"}"}"""


def assign04_main():
    graphs = []
    s = ''
    for size in [25, 50, 250, 500]:
        for version in ["A", "B"]:
            graphs.append(f"graph_verts{size}{version}.txt")
    results = []
    for val in graphs:
        res = run_algorithms(val)
        res["name"] = val
        results.append(res)
    for res in results:
        s += print_results(res)
    print(s)


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign04_main()

