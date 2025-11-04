# Implementación: Algoritmo de Fuerza Bruta

## Descripción General

Este directorio contiene la implementación educativa del **algoritmo de fuerza bruta (exhaustive search)** para coloreo de grafos. El algoritmo prueba todas las posibles asignaciones de colores hasta encontrar una válida.

## Archivos Principales

### 1. **brute_force_coloring.py**
Implementación completa del algoritmo con:
- Clase `BruteForceColoring` con métodos principales
- Método `color_graph()`: colorea el grafo
- Método `get_chromaticity()`: retorna el número cromático
- Método `is_valid_coloring()`: valida una coloración
- Ejemplos de uso ejecutables
- Análisis de complejidad documentado

### 2. **test_brute_force.py**
Suite de pruebas unitarias que verifican:
- Grafo con un solo nodo
- Nodos desconectados (conjunto independiente)
- Grafo bipartito (K_{2,2})
- Triángulo (K_3)
- Grafo completo (K_4)
- Ciclo impar (C_5)

### 3. **implementaciones/fuerza-bruta.md**
Documentación teórica completa incluyendo:
- Concepto fundamental
- Pseudocódigo
- Ejemplos paso a paso
- Análisis de complejidad
- Ventajas y desventajas
- Comparación con otros algoritmos

## Requisitos

- Python 3.6+
- Módulo `itertools` (incluido en stdlib)
- Archivos `graph.py` (clase Graph y Node)

## Uso Básico

```python
from graph import Node, Graph
from brute_force_coloring import BruteForceColoring

# Crear un grafo
graph = Graph()
node_a = Node("A")
node_b = Node("B")
node_c = Node("C")

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

# Agregar aristas
graph.add_edge(node_a, node_b)
graph.add_edge(node_b, node_c)
graph.add_edge(node_c, node_a)

# Colorear con fuerza bruta
coloring_algo = BruteForceColoring(graph)
result = coloring_algo.color_graph()

# Obtener resultado
print(f"Coloración: {result}")
print(f"Número cromático: {coloring_algo.get_chromaticity()}")
```

## Ejecución de Ejemplos

### Ejemplo Principal
```bash
python3 brute_force_coloring.py
```

Salida: Colorea un grafo de 4 nodos y un triángulo (K_3), mostrando:
- Asignación de colores
- Validación de la coloración
- Número cromático
- Análisis de complejidad

### Pruebas Unitarias
```bash
python3 test_brute_force.py
```

Ejecuta 6 pruebas en grafos de diferentes tipos, demostrando que el algoritmo:
- Encuentra el número cromático correcto
- Produce coloraciones válidas
- Maneja casos especiales

## Características Clave

### ✓ Correctitud Garantizada
- Encuentra el número cromático óptimo
- Completitud: siempre encuentra solución si existe

### ✓ Educativo
- Código claro y bien comentado
- Docstrings en inglés, comentarios en español
- Ejemplos ejecutables incluidos

### ✓ Validación
- Método `is_valid_coloring()` para verificar resultados
- Suite de pruebas exhaustiva
- Verificación de cada arista en ejemplos

### ✗ Limitaciones de Escalabilidad
- Complejidad: O(k^n × m)
- Impracticable para grafos con >15-20 nodos
- Tiempo exponencial en el número de nodos

## Complejidad Computacional

| Métrica | Valor |
|---------|-------|
| **Temporal** | O(k^n × m) peor caso |
| **Espacial** | O(n) |
| **Grafos pequeños** | Instantáneo (<10 nodos) |
| **Grafos medianos** | Segundos a minutos (10-15 nodos) |
| **Grafos grandes** | Impracticable (>20 nodos) |

donde:
- k = número de colores intentados
- n = número de nodos
- m = número de aristas

## Comparación con Alternativas

| Algoritmo | Tiempo | Óptimo | Uso |
|-----------|--------|--------|-----|
| **Fuerza Bruta** | Exponencial | ✓ Sí | Educación, investigación |
| **Codicioso** | O(n + m) | ✗ No | Aplicaciones prácticas |
| **Welsh-Powell** | O(n² + m) | ✗ No | Mejor que codicioso |
| **Branch & Bound** | Mejor que FB | ✓ Sí | Balance |

## Cuándo Usar Esta Implementación

### ✓ Use si:
- Necesita aprender conceptos fundamentales
- Grafo tiene menos de 15 nodos
- Requiere número cromático exacto
- Propósito de investigación o verificación

### ✗ No use si:
- Grafo tiene más de 20 nodos
- Necesita resultado en tiempo real
- Aplicación práctica de producción
- Presupuesto computacional limitado

## Estructura del Código

```
brute_force_coloring.py
├── BruteForceColoring (clase principal)
│   ├── __init__(graph)
│   ├── color_graph() → diccionario
│   ├── _find_valid_coloring_with_k_colors(nodes, k) → diccionario
│   ├── _is_safe_coloring(coloring) → booleano
│   ├── is_valid_coloring(coloring) → booleano
│   └── get_chromaticity() → entero
├── Ejemplo 1: Grafo con 4 nodos
└── Ejemplo 2: Triángulo (K_3)
```

## Conceptos Demostrados

1. **Búsqueda Exhaustiva**: Exploración sistemática de soluciones
2. **Producto Cartesiano**: Generación de todas las combinaciones
3. **Validación de Restricciones**: Verificación de coloraciones válidas
4. **Complejidad Exponencial**: Por qué ciertos problemas son impracticables
5. **Trade-off Exactitud-Velocidad**: Soluciones óptimas vs. eficiencia

## Salida Ejemplo

```
BRUTE FORCE GRAPH COLORING - Example

1. Creating a graph with 4 nodes...
Adding edges: A-B, A-C, A-D, B-D, C-D
Graph: Graph(nodes=4, edges=5)

2. Applying Brute Force Coloring algorithm...
Coloring found:
  Node A: Color 1
  Node B: Color 0
  Node C: Color 0
  Node D: Color 2

3. Chromatic Number Analysis
Chromatic Number: 3
(This graph requires a minimum of 3 colors)

4. Validation
Is the coloring valid? True
```

## Conceptos Teóricos Incluidos

- Número cromático: mínimo de colores necesarios
- Grafo bipartito: coloreable con 2 colores
- Grafo completo Kₙ: requiere n colores
- Grafo ciclo C_n: requiere 2 colores si n es par, 3 si es impar
- Conjunto independiente: todos conectan el mismo color

## Próximas Mejoras Posibles

1. **Poda temprana**: Detectar inválidas durante búsqueda
2. **Heurística de ordenamiento**: Priorizar nodos de alto grado
3. **Memoización**: Cachear subgrafos
4. **Branch and Bound**: Usar límites inferiores

## Recursos Adicionales

- Ver `implementaciones/fuerza-bruta.md` para teoría completa
- Ver `graph.py` para clase Graph
- Ver `coloreo-de-grafos.md` para teoría general
- Ver `test_brute_force.py` para más ejemplos

## Licencia y Atribución

Parte del proyecto educativo "Coloreo de Grafos"
- Autor: Implementación educativa
- Propósito: Enseñanza de algoritmos
- Año: 2025

---

**Nota**: Esta implementación está diseñada con fines educativos. Para aplicaciones prácticas con grafos grandes, consulte algoritmos más eficientes como Welsh-Powell o técnicas avanzadas de optimización.
