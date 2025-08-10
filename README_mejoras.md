# Mejoras implementadas

## Cambios por criterio
- **Análisis del problema (Ejercicio 3):** se reescribió la introducción para explicar el árbol filogenético, el objetivo de encontrar el LCA y la elección de DLS.
- **Justificación de métricas (Ejercicio 4):** se documentó el origen de la métrica de riesgo y la pertinencia de UCS frente a otras métricas.
- **Automatización:** se creó `run_compare_algorithms` para comparar algoritmos en todos los ejercicios, incluyendo Filogenia y Evacuación.
- **Reflexión crítica:** se añadieron conclusiones sobre el desempeño de UCS y A* en el escenario de evacuación.
- **Complejidad:** se incorporó una sección final con el análisis temporal y espacial de BFS, IDS/DLS, UCS y A*.
- **Modularización:** se agregó `utils.py` para centralizar la función `reconstruct` y el precálculo de distancias base con `compute_hop_dist`, reduciendo duplicación y mejorando la eficiencia de A* en evacuación.

## Posibles mejoras futuras
- Extender la modularización a más componentes para habilitar pruebas unitarias.
- Explorar heurísticas aprendidas o probabilísticas para el cálculo de riesgo en escenarios de evacuación.
- Ampliar el análisis de complejidad con experimentos empíricos en grafos más grandes.
