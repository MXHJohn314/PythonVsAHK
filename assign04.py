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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
    graph = adjMatFromFile(fileName)
    return verify_connection(len(graph), algo(graph))


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
    makeGraphs([i for i in range(25, 101, 2)])

def makeGraphs(sizes):
    # with open("ahkResults.txt") as ahk_file:
    #     ahk_results = json.loads(ahk_file.read())
    graphs = []

    py_results = {"prim": {}, "krus": {}}

    v_dict = {"A": "sparse", "B": "dense"}
    for size in sizes:
        for version in ["A", "B"]:
            file_name = f"graph_verts{size}{version}.txt"
            for algo in [prim, krus]:
                if v_dict[version] not in py_results[algo.__name__]:
                    py_results[algo.__name__][v_dict[version]] = []
                py_results[algo.__name__][v_dict[version]].append(run_algorithm(file_name, algo))

    # ahk_results_krus_dense_ = ahk_results['krus']['dense'][:-1]
    # ahk_results_krus_sparse_ = ahk_results['krus']['sparse'][:-1]

    # plt.plot(sizes[:-1], ahk_results_krus_dense_, label="ahk_krus_dense", marker='o')
    # plt.plot(sizes[:-1], ahk_results_krus_sparse_, label="ahk_krus_sparse", marker='o')
    py_results_krus_dense_ = py_results['krus']['dense'][:-1]
    py_results_krus_sparse_ = py_results['krus']['sparse'][:-1]
    print("py_results_krus_sparse_=" + str(py_results_krus_sparse_),
          # 'ahk_results_krus_sparse_=' + str(ahk_results_krus_sparse_),
          "py_results_krus_dense_=" + str(py_results_krus_dense_),
          # 'ahk_results_krus_dense_=' + str(ahk_results_krus_dense_),
          sep="\n")
    plt.plot(sizes[:-1], py_results_krus_dense_, label="py_krus_dense", marker='o')
    plt.plot(sizes[:-1], py_results_krus_sparse_, label="py_krus_sparse", marker='o')
    print()
    plt.xlabel("size as n approaches ∞")
    plt.ylabel("time in seconds")
    plt.title("Kruskal's Algorithm Runtime Comparison")
    plt.legend()
    plt.show()


# for i,val in enumerate(graphs):
#     if val[-5] == 'A'
# # json_test = json.dumps(results, indent=0)
# # print(re.sub("\s","",json_test))
# columns=["size"]
# for letter in ["A","B"]:
#     for algo in ["Krus","Prim"]:
#         for language in ["PY"]:
#             columns.append(f"{language}_{algo}_{letter}")
# max_time = None
# columns = {col : [] for col in columns}
# for graph_name in results:
#     letter = graph_name[-5]
#     krus_time_ = results[graph_name]["krus"]["time"]
#     columns[f"PY_Krus_{letter}"].append(krus_time_)
#     prim_time_ = results[graph_name]["prim"]["time"]
#     columns[f"PY_Prim_{letter}"].append(prim_time_)
#     if not max_time:
#         max_time = max(krus_time_, prim_time_)
#     else:
#         max_time = max(krus_time_, prim_time_, max_time)
#
#
# columns["size"] = sizes
# df = pd.DataFrame.from_dict(columns)
# for graph_name in results:
#     letter = graph_name[-5]
#     plt.plot(sizes, df[f"PY_Krus_{letter}"], label=f"PY_Krus_{letter}", marker='o', linewidth=3)
#     plt.plot(sizes, df[f"PY_Prim_{letter}"], label=f"PY_Prim_{letter}", marker='o', linewidth=3)
# print(df)
#
# plt.xlabel('size as n approaches ∞')
# plt.ylabel('time in microseconds')
# plt.legend(loc='upper left')
# plt.xticks(df ['size'].tolist())
# plt.yticks(np.arange(0, max_time, .05))
# plt.title('Stuff')
# plt.show()

# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign04_main()
