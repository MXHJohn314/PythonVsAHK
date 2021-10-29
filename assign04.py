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


def prim(W):
    """ Carry out Prim's algorithm using W as a weight/adj matrix. """
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
    return solution


def kruskal(w):
    """ Carry out Kruskal's using W as a weight/adj matrix. """
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
    return solution


def assign04_main():
    """ Demonstrate the functions, starting with creating the graph. """
    graph_verts10 = adjMatFromFile("graph_verts10.txt")
    graph_verts100A = adjMatFromFile("graph_verts100_A.txt")
    graph_verts100B = adjMatFromFile("graph_verts100_B.txt")

    # Run Prim's algorithm
    start_time = time.time()
    res_prim_10 = prim(graph_verts10)
    res_prim_100A = prim(graph_verts100A)
    res_prim_100B = prim(graph_verts100B)
    elapsed_time_prim = time.time() - start_time
    print(f"Prim's runtime: {elapsed_time_prim:.2f}")

    # Run Kruskal's for a single starting vertex, 2
    start_time = time.time()
    res_kruskal = kruskal(graph_verts10)
    res_kruskal100A = kruskal(graph_verts100A)
    res_kruskal100B = kruskal(graph_verts100B)
    for p, k in [(res_prim_10, res_kruskal), (res_prim_100A, res_kruskal100A), (res_prim_100B, res_kruskal100B)]:
        print(f"prim: sum= {sum(i[2] for i in p)}\nsolution={str(p)}\n\n"
              f"krus: sum= {sum(i[2] for i in k)}\nsolution={str(k)}\n\n\n")
    elapsed_time_kruskal = time.time() - start_time
    print(f"Kruskal's runtime: {elapsed_time_kruskal:.2f}")

    # If above assert passed, then it doesn't matter which result is used
    cost_prim = sum([e[2] for e in res_prim_10])
    print("MST cost w/ Prim: ", cost_prim)
    cost_kruskal = sum([e[2] for e in res_kruskal])
    print("MST cost w/ Kruskal: ", cost_kruskal)
    assert cost_prim == cost_kruskal
    print([_ for _ in res_prim_10], sep="\n")
    print(f'{sum(i[2] for i in res_kruskal)} vs {sum(i[2] for i in res_prim_10)}')
    print([_ for _ in res_kruskal], sep="\n")



# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign04_main()

