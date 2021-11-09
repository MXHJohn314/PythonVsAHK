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
import re
import time
import json
import matplotlib.pyplot as plt
import numpy as np


def adjMatFromFile(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    # print(f" n_verts = {n_verts}")
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
    """ Helper method to verify that all vertices can be connected from a given list of solution edges. """
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
    return dict_["time"]


def prim(W):
    """ Carry out Prim's algorithm using W as a weight/adj matrix. """
    times = []
    start = time.time()
    visited = {0}
    solution = []
    unvisited = [_ for _ in range(1, len(W))]
    edges = {}
    times.append(time.time() - start)
    for i in range(len(W)):
        start = time.time()
        edges[i] = sorted([(i, j, W[i][j]) for j in range(len(W))
                           if j != i and j not in visited and W[i][j]],
                          key=lambda x: x[2], reverse=True)
        times.append(time.time() - start)
    start = time.time()
    while unvisited:
        min_edge = min([item for item in edges.items() if item[0] in visited and len(item[1]) > 0],
                       key=lambda x: x[1][-1][2])[1].pop()
        solution.append(min_edge)
        unvisited.remove(min_edge[1])
        visited.add(min_edge[1])
        [edge_list.remove(edge) for vertex, edge_list in edges.items() for edge in edge_list
         if edge[1] in visited]
    times.append(time.time() - start)
    return {
        "solution": solution,
        "cost": sum([i[2] for i in solution]),
        "time": sum(times)
    }


def krus(w):
    """ Carry out Kruskal's using W as a weight/adj matrix. """
    times = []
    start = time.time()
    solution = []
    sets = [{i} for i in range(len(w))]
    times.append(time.time() - start)
    edges = sorted([(i, j, w[i][j]) for i in range(len(w))
                    for j in range(len(w)) if w[i][j] and i != j], key=lambda x: x[2])
    start = time.time()
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
    times.append(time.time() - start)
    return {
        "solution": solution,
        "cost": sum([i[2] for i in solution]),
        "time": sum(times)
    }


def run_algorithm(fileName, algo):
    """ Calls the specified algorithm to be run with a given graph file. """
    graph = adjMatFromFile(fileName)
    return verify_connection(len(graph), algo(graph))


def run(doWrite=False):
    """
    Will run all python algorithms and write results to a file if doWrite=True.
    Reads python results from a file as a list of json objects, and returns a dictionary.
    """
    if doWrite:
        s = ''
        for j in range(100):
            resKrusSparse = []
            resPrimSparse = []
            resKrusDense = []
            resPrimDense = []
            js = []
            for i in range(25, 100, 2):
                resKrusSparse.append(krus(adjMatFromFile(f"graph_verts{i}A.txt"))["time"])
                resKrusDense.append(krus(adjMatFromFile(f"graph_verts{i}B.txt"))["time"])
                resPrimSparse.append(prim(adjMatFromFile(f"graph_verts{i}A.txt"))["time"])
                resPrimDense.append(prim(adjMatFromFile(f"graph_verts{i}B.txt"))["time"])
            js.append({
                    "krus": {"sparse": resKrusSparse, "dense": resKrusDense},
                    "prim": {"sparse": resPrimSparse, "dense": resPrimDense}
            })
            sub_ = re.sub("'", '"', json.dumps(js))
            s += f'{sub_}\n'
            print(j)
        with open('pyResults.txt', 'w') as file:
            file.write(s)
    js = [json.loads(i)[0] for i in open('pyResults.txt', 'r').readlines()]
    py_res = {'krus': {'sparse': [], 'dense': []}, 'prim': {'sparse': [], 'dense': []}}
    for algo_name, algo_def in {'krus': krus, 'prim': prim}.items():
        for algo_key, algo_val in {"sparse": "A", 'dense': 'B'}.items():
            for j in range(len(js[0]['krus']['sparse'])):
                py_res[algo_name][algo_key].append(
                    np.mean([js[i][algo_name][algo_key][j] for i in range(len(js))]))
    return py_res

def assign04_main(doPythonRuns=False, doGraphs=True, sizes=None):
    """
    Will create python results if doPythonRuns=True
    Will create graphs if doGraphs=True
    Will initialize the sizes if sizes=None.
    sizes is used to determine which `graph_verts` files to use.
    """
    global py_res
    if sizes is None:
        sizes = [i for i in range(25, 100, 2)]
    if doPythonRuns:
        py_res = run(False)
    with open("ahk_results.txt") as ahk_file:
        js = [json.loads(line) for line in ahk_file.readlines()]
        rng = range(len(js[0]['krus']['sparse']))
        ahk_res = {'krus': {'sparse': [], 'dense': []}, 'prim': {'sparse': [], 'dense': []}}
        for algo_name, algo_def in {'krus': krus, 'prim': prim}.items():
            for algo_key, algo_val in {"sparse": "A", 'dense': 'B'}.items():
                for j in rng:
                    ahk_res[algo_name][algo_key].append(np.mean([js[i][algo_name][algo_key][j] for i in range(len(js))]))
    if doGraphs:
        makeGraphs(sizes, py_res, ahk_res)


def makeGraphs(sizes, py_res, ahk_res):
    """
    Creates plots by taking in dictionaries containing results from both languages.
    Only uncomment one of the following sections of code to make a graph comparing those results.
    """
    plt.xlabel("Number of Vertices")
    plt.ylabel("Time (Seconds)")
    plt.legend()
    plt.show()

    """Section 1, kruskal, dense"""
    # plt.plot(sizes[:-1], ahk_res['krus']['dense'], label="ahk_krus_dense", marker='o')
    # plt.plot(sizes[:-1], py_res['krus']['dense'][:-1], label="py_krus_dense", marker='o')
    # plt.title("Kruskal's Algorithm (Dense Graphs)")

    """Section 2, kruskal, sparse"""
    # plt.plot(sizes[:-1], ahk_res['krus']['sparse'], label="ahk_krus_sparse", marker='o')
    # plt.plot(sizes[:-1], py_res['krus']['sparse'][:-1], label="py_krus_sparse", marker='o')
    # plt.title("Kruskal's Algorithm (Sparse Graphs)")

    """Section 3, prim, dense"""
    # plt.plot(sizes[:-1], ahk_res['prim']['dense'], label="ahk_prim_dense", marker='o')
    # plt.plot(sizes[:-1], py_res['prim']['dense'][:-1], label="py_prim_dense", marker='o')
    # plt.title("Prim's Algorithm (Dense Graphs)")

    """Section 4, prim, sparse"""
    plt.plot(sizes[:-1], ahk_res['prim']['sparse'], label="ahk_prim_sparse", marker='o')
    plt.plot(sizes[:-1], py_res['prim']['sparse'][:-1], label="py_prim_sparse", marker='o')
    plt.title("Prim's Algorithm (Sparse Graphs)")


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign04_main(doPythonRuns=True, doGraphs=True)
