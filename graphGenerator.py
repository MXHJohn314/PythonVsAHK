import queue
import random
import random as r
import sys

from assign04 import krus, adjMatFromFile


def getSkeleto(n):
    '''Ensures there is at least one spanning tree before filling in other random values.'''
    visited = {}
    unvisited = [i for i in range(n)]
    sv = random.choice(unvisited)
    visited_keys = [sv]
    unvisited.remove(sv)
    while unvisited:
        next_v = random.choice(unvisited)
        prev = random.choice(visited_keys)
        visited_keys.append(next_v)
        unvisited.remove(next_v)
        if (next_v, prev) in visited:
            unvisited.append(visited_keys.pop())
            continue
        cost = r.randint(1, 20)
        if random.uniform(-.5, .5) > 0:
            visited[(prev, next_v)] = cost
            visited[(next_v, prev)] = cost
        else:
            visited[(next_v, prev)] = cost
            visited[(prev, next_v)] = cost
    return visited


def generateGraph(n: int, is_dense: bool, version='', max_weight=20, density_factor=.9):
    """
    Writes a dense or sparse graph's set of edges to a file. will generate an edge between two
    vertices denisty_factor percent of the time by default if is_dense is true.
    """
    skeleton = getSkeleto(n)
    a_spanning_tree = sorted([(k[0], k[1], v) for k, v in skeleton.items() if v],
                             key=lambda x: x[2])
    density = density_factor if is_dense else 1 / n
    lines = {i: {} for i in range(n)}
    for a in range(n):
        q = queue.Queue()
        [q.put(x) for x in range(n) if x != a]
        for _ in range(n):
            if q.empty():
                break
            b = q.get()
            if a in lines[b]:
                continue
            if (a, b) not in skeleton and not (is_dense and r.randint(1, n) / n < density or r.randint(1, n) / (n**2 - n) > 1 / n):
                continue
            cost = r.randint(1, max_weight) if (a, b) not in skeleton else skeleton[(a, b)]
            lines[a][b] = cost
            lines[b][a] = cost
    s = f'{n}\n'
    for a, items in lines.items():
        s += f'{a}'
        for b, cost in items.items():
            s += f' {b} {cost}'
        s += '\n'
    name = f"graph_verts{n}{version}.txt"
    with open(name, "w") as file:
        file.write(s)
    return adjMatFromFile(name), a_spanning_tree


def generateGraphs(size):
    """ Generates one dense and one sparse graph of the given size. """
    w, skeleton = generateGraph(size, False, "A")
    krusRes1 = krus(w)
    w2, skeleton2 = generateGraph(size, True, "B")
    krusRes2 = krus(w2)
    print(f'''
    krusA sum = {sum(i[2] for i in krusRes1['solution'])}
    {krusRes2}

    krusB sum = {sum(i[2] for i in krusRes2['solution'])}
    {krusRes2}

    skelton sum = {sum([i[2] for i in skeleton])}\
    {skeleton}''')


if __name__ == "__main__":
    sizes = [i for i in range(25, 101, 2)]
    for size in sizes:
        generateGraphs(size)
