from collections import deque
from typing import Dict, List, Optional, Iterable, Any


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
