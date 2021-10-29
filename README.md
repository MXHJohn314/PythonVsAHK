# Should do a detailed comparison of Python implementation vs AutoHotkey

## Kruskal's and Prim's minimum spanning tree (MST) algorithms. Uses sorting, swapping and comparison helper functnions, and three helper `Set` class. 

Note that both of the functions to be implemented have the exact same input and output (see example input and output below for more details)

* __prim(W)__ carry out Prim's algorithm on a graph represented by its weight matrix
  * input: adjacency weight matrix, W such that W[i][j] is the weight from vertex i to vertex j
  * output/return: a list of tuples where each tuple is an edge in the MST and is in the form (i, j, wij), denoting an edge between vertex i and j with a weight of wij (see example below)

* __kruskal(W)__ carry out Dijkstra's algorithm on a graph represented by its weight matrix
  * input: adjacency weight matrix, W such that W[i][j] is the weight from vertex i to vertex j
  * output/return: a list of tuples where each tuple is an edge in the MST and is in the form (i, j, wij), denoting an edge between vertex i and j with a weight of wij (see example below)




### Example with a 3-vertex graph

    # a graph defined by its adjacency matrix
    g = [ [0, 8, 9], [8, 0, 3], [9, 3, 0] ]
    prim_result = prim(g)
    kruskal_result = kruskal(g)

    # both prim_result and kruskal_result should be a (Python) list of (Python) tuples, 
    # which represents a (mathematical) set of (mathematical) tuples 
    print(prim_result) 
    [(0, 1, 8), (1, 2, 3)]
