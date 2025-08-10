from collections import deque
from typing import Dict, List, Optional, Iterable, Any
import time



def reconstruct(parent: Dict[Any, Optional[Any]], goal: Any) -> List[Any]:
    """Reconstruye la ruta desde el inicio implícito hasta ``goal``.

    Parameters
    ----------
    parent: Dict[Any, Optional[Any]]
        Mapeo de cada nodo con su predecesor.
    goal: Any
        Nodo objetivo desde el cual se reconstruye la ruta.

    Returns
    -------
    List[Any]
        Secuencia de nodos desde el inicio hasta ``goal``.
    """
    path: List[Any] = []
    n = goal
    while n is not None:
        path.append(n)
        n = parent.get(n)
    return list(reversed(path))


def compute_hop_dist(graph, goals: Iterable[Any]) -> Dict[Any, int]:
    """Calcula la distancia en número de aristas (hops) mínima desde cada nodo a
    cualquiera de los objetivos proporcionados.

    Este pre-cálculo puede reutilizarse como heurística admisible en algoritmos
    como A* cuando se minimiza el riesgo acumulado.
    """
    dist: Dict[Any, int] = {g: 0 for g in goals}
    q = deque(goals)
    while q:
        u = q.popleft()

        for item in graph.neighbors(u):
            # ``item`` puede ser simplemente el vecino o un par ``(vecino, attrs)``
            if isinstance(item, tuple):
                v, attrs = item
                if isinstance(attrs, dict) and attrs.get("closed"):
                    continue
            else:
                v = item

        for v, _ in graph.neighbors(u):

            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

class PhyloTree:
    """Árbol simple orientado para consultas de LCA."""

    def __init__(self, root: Any):
        self.root = root
        self.children: Dict[Any, List[Any]] = {root: []}

    def add_edge(self, parent: Any, child: Any) -> None:
        self.children.setdefault(parent, []).append(child)
        self.children.setdefault(child, [])

    def successors(self, node: Any) -> Iterable[Any]:
        return self.children.get(node, [])


def _dls_path(tree: PhyloTree, start: Any, goal: Any, limit: int):
    """Devuelve la ruta a ``goal`` con búsqueda en profundidad limitada."""
    stack = [(start, [start], 0)]
    expanded = 0
    while stack:
        node, path, depth = stack.pop()
        if node == goal:
            return path, expanded
        if depth < limit:
            for child in reversed(list(tree.successors(node))):
                stack.append((child, path + [child], depth + 1))
        expanded += 1
    return [], expanded


def _bfs_path(tree: PhyloTree, start: Any, goal: Any):
    """Devuelve la ruta a ``goal`` con búsqueda en amplitud."""
    q = deque([(start, [start])])
    expanded = 0
    visited = {start}
    while q:
        node, path = q.popleft()
        if node == goal:
            return path, expanded
        for child in tree.successors(node):
            if child not in visited:
                visited.add(child)
                q.append((child, path + [child]))
        expanded += 1
    return [], expanded


def lca_with_method(
    tree: PhyloTree, u: Any, v: Any, method: str = "DLS", max_depth: Optional[int] = None
):
    """Encuentra el ancestro común más reciente entre ``u`` y ``v``."""
    start = tree.root
    t0 = time.time()
    m = method.upper()
    if m == "DLS":
        if max_depth is None:
            raise ValueError("max_depth es obligatorio para DLS")
        path_u, exp_u = _dls_path(tree, start, u, max_depth)
        path_v, exp_v = _dls_path(tree, start, v, max_depth)
    elif m == "BFS":
        path_u, exp_u = _bfs_path(tree, start, u)
        path_v, exp_v = _bfs_path(tree, start, v)
    else:
        raise ValueError("method debe ser 'DLS' o 'BFS'")

    lca = None
    for a, b in zip(path_u, path_v):
        if a == b:
            lca = a
        else:
            break
    res = {
        "ruta_u": path_u,
        "ruta_v": path_v,
        "expandidos_u": exp_u,
        "expandidos_v": exp_v,
        "profundidad_u": len(path_u) - 1 if path_u else None,
        "profundidad_v": len(path_v) - 1 if path_v else None,
        "LCA": lca,
        "tiempo_ms": round((time.time() - t0) * 1000, 3),
    }
    return res

