# Prompt: Implementación del Algoritmo Codicioso (First-Fit) para Coloreo de Grafos

## Contexto del Proyecto

Este es un proyecto **educativo** sobre algoritmos de coloreo de grafos. Ya existe una implementación de fuerza bruta (`brute_force_coloring.py`) que sirve como referencia de estilo y estructura. Tu tarea es implementar el algoritmo codicioso siguiendo los mismos principios educativos.

## Objetivo

Implementar el **algoritmo codicioso first-fit** para coloreo de grafos en Python, siguiendo la arquitectura establecida en el proyecto y las especificaciones del documento `implementaciones/codicioso.md`.

## Estructura de Datos Existente

El proyecto utiliza las siguientes clases definidas en `graph.py`:

```python
class Node:
    """Representa un vértice del grafo"""
    def __init__(self, node_id, data=None)
    # Atributos: id, data
    # Métodos: __repr__, __eq__, __hash__

class Graph:
    """Representa un grafo no dirigido usando lista de adyacencia"""
    # Atributos: adjacency_list, nodes
    # Métodos clave:
    #   - add_node(node)
    #   - add_edge(node1, node2)
    #   - get_neighbors(node)
    #   - get_nodes()
    #   - get_edges()
    #   - get_degree(node)
    #   - has_edge(node1, node2)
    #   - get_max_degree()
```

## Especificación del Algoritmo

### Estrategia First-Fit

El algoritmo debe implementar la estrategia **first-fit** (primer ajuste):

1. **Ordenar** los vértices según algún criterio (por defecto: orden natural; opcionalmente permitir ordenamiento por grado)
2. **Asignar** el color 1 al primer vértice
3. **Para cada vértice restante:**
   - Recolectar los colores de todos sus vecinos ya coloreados
   - Identificar el conjunto de colores "prohibidos"
   - Asignar el **menor color disponible** (el primer entero positivo no prohibido)
4. **Retornar** el diccionario de coloración `{node: color}`

### Características Clave

- **Simplicidad:** Código claro y fácil de entender
- **Eficiencia:** O(n²) en tiempo, O(n) en espacio
- **Determinismo:** Mismo orden de entrada → mismo resultado
- **No backtracking:** Las decisiones son finales

## Especificaciones de Implementación

### Archivo: `greedy_coloring.py`

Crear un archivo con la siguiente estructura:

```python
"""
Greedy Graph Coloring Algorithm (First-Fit).

This module implements a greedy approach to graph coloring using
the first-fit strategy. It processes vertices sequentially and
assigns the smallest available color that doesn't conflict with
neighbors.

Educational Purpose:
- Demonstrates greedy algorithmic paradigm
- Shows trade-off between speed and optimality
- Practical for large graphs where exact solutions are infeasible
"""

from graph import Node, Graph


class GreedyColoring:
    """
    Greedy first-fit algorithm for graph coloring.
    
    This algorithm processes vertices in a specified order and assigns
    each vertex the smallest color that doesn't conflict with its
    already-colored neighbors.
    
    The resulting coloring is valid but may not use the minimum number
    of colors (not guaranteed to find the chromatic number).
    
    Attributes:
        graph: The Graph object to color
        coloring: Result of the coloring operation (node -> color mapping)
        order_strategy: Strategy for ordering vertices ('natural' or 'degree')
    """
```

### Métodos Requeridos

#### 1. `__init__(self, graph, order_strategy='natural')`

**Propósito:** Inicializar el algoritmo con el grafo y estrategia de ordenamiento.

**Parámetros:**
- `graph`: Objeto Graph a colorear
- `order_strategy`: 'natural' (orden por ID) o 'degree' (orden por grado descendente)

**Validaciones:**
- Graph no puede ser None → `ValueError("Graph cannot be None")`
- Graph debe tener al menos un nodo → `ValueError("Graph must contain at least one node")`
- order_strategy debe ser 'natural' o 'degree' → `ValueError("order_strategy must be 'natural' or 'degree'")`

**Inicialización:**
- `self.graph = graph`
- `self.coloring = {}` (vacío inicialmente)
- `self.order_strategy = order_strategy`

---

#### 2. `color_graph(self)`

**Propósito:** Colorear el grafo usando la estrategia first-fit.

**Algoritmo detallado:**

```
1. Obtener lista ordenada de nodos según self.order_strategy:
   - Si 'natural': ordenar por node.id (alfabéticamente o numéricamente)
   - Si 'degree': ordenar por grado descendente (mayor a menor)
     * En caso de empate (mismo grado), desempatar por node.id
     * Ejemplo: sorted(nodes, key=lambda n: (-self.graph.get_degree(n), str(n.id)))

2. Inicializar self.coloring = {}

3. Para cada nodo en la lista ordenada:
   a. Obtener colores de vecinos ya coloreados:
      - Crear conjunto forbidden_colors = set()
      - Para cada vecino del nodo:
        - Si vecino está en self.coloring:
          - Agregar self.coloring[vecino] a forbidden_colors
   
   b. Encontrar el menor color disponible:
      - OPCIÓN 1 (Simple y clara):
        color = 1
        while color in forbidden_colors:
            color += 1
        self.coloring[nodo] = color
      
      - OPCIÓN 2 (Más eficiente para muchos colores):
        if not forbidden_colors:
            color = 1
        else:
            # Encontrar el primer "hueco" en la secuencia
            color = 1
            sorted_forbidden = sorted(forbidden_colors)
            for forbidden_color in sorted_forbidden:
                if color == forbidden_color:
                    color += 1
                else:
                    break
        self.coloring[nodo] = color
      
      RECOMENDACIÓN: Usar OPCIÓN 1 por claridad educativa

4. Retornar self.coloring
```

**Retorno:** Diccionario `{Node: int}` con la coloración

**Complejidad:** 
- **Tiempo:** O(n² + n log n) ≈ O(n²) donde n es el número de vértices
  - Ordenamiento: O(n log n) para orden natural, O(n²) para orden por grado
  - Iteración sobre nodos: O(n)
  - Por cada nodo, revisar vecinos: O(d) donde d es el grado promedio
  - En el peor caso (grafo denso): O(n) vecinos por nodo → O(n²) total
- **Espacio:** O(n) para almacenar coloración y estructuras auxiliares

---

#### 3. `get_num_colors(self)`

**Propósito:** Obtener el número de colores utilizados.

**Implementación:**
- Si `self.coloring` está vacío: retornar 0
- Si no: retornar `max(self.coloring.values())`

**Retorno:** Entero con el número de colores usados

---

#### 4. `is_valid_coloring(self)`

**Propósito:** Verificar que la coloración sea válida (sin vecinos adyacentes del mismo color).

**Algoritmo:**
```
1. Si self.coloring está vacío: retornar False

2. Para cada nodo en self.graph.get_nodes():
   - Si nodo no está en self.coloring: retornar False
   
3. Para cada arista (node1, node2) en self.graph.get_edges():
   - Si self.coloring[node1] == self.coloring[node2]:
     - Retornar False

4. Retornar True
```

**Retorno:** Boolean

---

#### 5. `get_coloring_dict(self)`

**Propósito:** Obtener el diccionario de coloración con IDs de nodos en lugar de objetos Node.

**Implementación:**
```python
return {node.id: color for node, color in self.coloring.items()}
```

**Retorno:** Diccionario `{node_id: color}`

---

#### 6. `get_color_classes(self)` (OPCIONAL pero recomendado)

**Propósito:** Agrupar nodos por color para facilitar visualización y análisis.

**Implementación:**
```python
color_classes = {}
for node, color in self.coloring.items():
    if color not in color_classes:
        color_classes[color] = []
    color_classes[color].append(node.id)
return color_classes
```

**Retorno:** Diccionario `{color: [node_ids]}`

**Ejemplo:** `{1: ['A', 'C'], 2: ['B', 'D'], 3: ['E']}`

---

### Ejemplo de Uso (al final del archivo)

Incluir un bloque ejecutable que demuestre:

```python
if __name__ == "__main__":
    # 1. Crear un grafo de ejemplo (ciclo de 5 nodos)
    print("=" * 60)
    print("ALGORITMO CODICIOSO: FIRST-FIT")
    print("=" * 60)
    
    graph = Graph()
    nodes = [Node(chr(65 + i)) for i in range(5)]  # A, B, C, D, E
    
    for node in nodes:
        graph.add_node(node)
    
    # Crear ciclo: A-B-C-D-E-A
    edges = [(0,1), (1,2), (2,3), (3,4), (4,0)]
    for i, j in edges:
        graph.add_edge(nodes[i], nodes[j])
    
    print(f"\nGrafo creado: {graph}")
    print(f"Número cromático esperado: 3 (ciclo impar)")
    
    # 2. Colorear con estrategia natural
    print("\n" + "-" * 60)
    print("ESTRATEGIA: Orden Natural")
    print("-" * 60)
    
    greedy_natural = GreedyColoring(graph, order_strategy='natural')
    coloring_natural = greedy_natural.color_graph()
    
    print(f"\nColoración obtenida:")
    for node, color in sorted(coloring_natural.items(), key=lambda x: x[0].id):
        print(f"  {node.id}: Color {color}")
    
    print(f"\nNúmero de colores usados: {greedy_natural.get_num_colors()}")
    print(f"¿Coloración válida? {greedy_natural.is_valid_coloring()}")
    
    # Verificar que ningún par de vecinos tiene el mismo color
    print("\nVerificación de vecinos:")
    for node in nodes:
        neighbors = graph.get_neighbors(node)
        neighbor_colors = [coloring_natural[n] for n in neighbors]
        print(f"  {node.id} (Color {coloring_natural[node]}) - Vecinos: {neighbor_colors}")
    
    # 3. Colorear con estrategia por grado
    print("\n" + "-" * 60)
    print("ESTRATEGIA: Orden por Grado (descendente)")
    print("-" * 60)
    
    greedy_degree = GreedyColoring(graph, order_strategy='degree')
    coloring_degree = greedy_degree.color_graph()
    
    print(f"\nColoración obtenida:")
    for node, color in sorted(coloring_degree.items(), key=lambda x: x[0].id):
        print(f"  {node.id}: Color {color}")
    
    print(f"\nNúmero de colores usados: {greedy_degree.get_num_colors()}")
    print(f"¿Coloración válida? {greedy_degree.is_valid_coloring()}")
    
    # 4. Comparación
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPARATIVO")
    print("=" * 60)
    print(f"Número cromático teórico: 3")
    print(f"Colores usados (natural): {greedy_natural.get_num_colors()}")
    print(f"Colores usados (por grado): {greedy_degree.get_num_colors()}")
    print(f"\nNota: El algoritmo codicioso no garantiza encontrar el mínimo,")
    print(f"pero es mucho más rápido que la fuerza bruta para grafos grandes.")
```

## Archivo de Pruebas: `test_greedy.py`

Crear un archivo de pruebas unitarias con los siguientes casos:

### Test Cases Requeridos

1. **test_single_node**: Un nodo aislado → 1 color
2. **test_two_disconnected_nodes**: Dos nodos sin arista → 1 color
3. **test_two_connected_nodes**: Dos nodos conectados → 2 colores
4. **test_triangle**: Grafo K₃ (triángulo) → 3 colores
5. **test_bipartite_graph**: K₂,₂ (grafo bipartito) → 2 colores
6. **test_cycle_odd**: C₅ (ciclo impar) → 3 colores
7. **test_complete_graph**: K₄ (grafo completo) → 4 colores
8. **test_star_graph**: Grafo estrella (1 centro, n puntas) → 2 colores
9. **test_order_strategy_natural**: Verificar orden natural
10. **test_order_strategy_degree**: Verificar orden por grado
11. **test_invalid_order_strategy**: Verificar excepción con estrategia inválida
12. **test_empty_graph_error**: Verificar excepción con grafo vacío
13. **test_none_graph_error**: Verificar excepción con grafo None

### Estructura del Archivo de Pruebas

```python
"""
Unit tests for Greedy Graph Coloring Algorithm.

Tests verify correctness of the first-fit greedy coloring
for various graph structures and configurations.
"""

import unittest
from graph import Node, Graph
from greedy_coloring import GreedyColoring


class TestGreedyColoring(unittest.TestCase):
    """Test suite for GreedyColoring class."""
    
    def test_single_node(self):
        """A single node should use 1 color."""
        # Implementar...
        
    # ... más tests


if __name__ == '__main__':
    unittest.main()
```

## Archivo README: `GREEDY_README.md`

Crear documentación siguiendo el formato de `BRUTE_FORCE_README.md`:

### Secciones Requeridas

1. **Descripción General**
   - Explicación del algoritmo codicioso first-fit
   - Diferencias con fuerza bruta

2. **Archivos Principales**
   - `greedy_coloring.py`: Implementación
   - `test_greedy.py`: Pruebas unitarias
   - `implementaciones/codicioso.md`: Documentación teórica

3. **Requisitos**
   - Python 3.6+
   - Dependencia de `graph.py`

4. **Uso Básico**
   - Ejemplo completo de código

5. **Ejecución de Pruebas**
   ```bash
   python test_greedy.py
   python greedy_coloring.py  # Para ver ejemplos
   ```

6. **Análisis de Complejidad**
   - Temporal: O(n²)
   - Espacial: O(n)
   - Comparación con fuerza bruta

7. **Ventajas y Limitaciones**
   - **Ventajas:** Rápido, escalable, simple
   - **Limitaciones:** No garantiza número cromático

8. **Comparación de Estrategias**
   - Orden natural vs orden por grado
   - Casos donde una es mejor que otra

## Convenciones de Código

### Estilo Python
- **PEP 8:** Seguir guía de estilo estándar
- **Docstrings:** Formato Google/NumPy para todas las funciones
- **Type hints:** Opcional pero recomendado
- **Nombres:** Descriptivos en inglés (`forbidden_colors`, `color_candidate`)

### Documentación
- **Comentarios en español** para explicaciones conceptuales
- **Código en inglés** (variables, funciones, clases)
- **Docstrings en inglés** (consistencia con el proyecto)

### Ejemplo de Docstring
```python
def color_graph(self):
    """
    Color the graph using the greedy first-fit strategy.
    
    Processes vertices in the order specified by order_strategy,
    assigning each vertex the smallest color that doesn't conflict
    with its already-colored neighbors.
    
    Returns:
        dict: Mapping from Node objects to color integers (1-indexed)
        
    Raises:
        RuntimeError: If coloring process encounters unexpected state
        
    Time Complexity: O(n²) where n is the number of vertices
    Space Complexity: O(n) for storing the coloring
    
    Example:
        >>> greedy = GreedyColoring(graph)
        >>> coloring = greedy.color_graph()
        >>> print(coloring[node_a])
        1
    """
```

## Criterios de Aceptación

### Edge Cases a Considerar

El implementador debe manejar correctamente:

1. **Grafo con un solo nodo:** Debe retornar 1 color
2. **Grafo sin aristas:** Todos los nodos pueden usar el mismo color
3. **Grafo completo Kₙ:** Debe usar n colores (todos diferentes)
4. **Nodos aislados:** Se pueden colorear con el mismo color que otros aislados
5. **Llamadas múltiples a `color_graph()`:** Debe sobrescribir coloración anterior
6. **Grafo vacío al inicializar:** Debe lanzar excepción en `__init__`

### Funcionalidad
- ✅ Implementa correctamente el algoritmo first-fit
- ✅ Soporta ambas estrategias de ordenamiento
- ✅ Todas las pruebas unitarias pasan
- ✅ La coloración es siempre válida

### Código
- ✅ Sigue el estilo del proyecto existente
- ✅ Código limpio y legible
- ✅ Documentación completa (docstrings)
- ✅ Manejo apropiado de errores

### Documentación
- ✅ README completo y claro
- ✅ Ejemplos ejecutables funcionan correctamente
- ✅ Explicaciones paso a paso

### Educativo
- ✅ El código es fácil de entender para estudiantes
- ✅ Los ejemplos ilustran conceptos clave
- ✅ Incluye análisis de complejidad
- ✅ Muestra trade-offs (velocidad vs optimalidad)

## Comparación con Fuerza Bruta

Incluir en `GREEDY_README.md` una tabla comparativa:

| Aspecto | Fuerza Bruta | Codicioso First-Fit |
|---------|--------------|---------------------|
| **Complejidad Temporal** | O(k^n · n²) | O(n²) |
| **Complejidad Espacial** | O(n) + recursión | O(n) |
| **Optimalidad** | Garantizada (número cromático) | No garantizada |
| **Escalabilidad** | Grafos pequeños (~10 nodos) | Grafos grandes (miles de nodos) |
| **Determinismo** | Sí | Sí (con mismo orden) |
| **Aplicabilidad** | Académica, benchmarking | Práctica, real-world |
| **Tiempo para K₄** | ~0.01s | ~0.0001s |
| **Tiempo para K₁₀** | Horas/días | Milisegundos |
| **Uso de memoria** | Exponencial en recursión | Lineal |
| **Mejor caso** | O(k · n²) con k pequeño | O(n²) |
| **Peor caso** | O(n^n · n²) | O(n²) |

**Casos de uso recomendados:**

- **Fuerza Bruta:** 
  - Grafos con n ≤ 10
  - Cuando se necesita el número cromático exacto
  - Benchmarking de otros algoritmos
  - Problemas académicos pequeños

- **Codicioso First-Fit:**
  - Grafos con n > 10
  - Aplicaciones en tiempo real
  - Sistemas de asignación de recursos
  - Cuando velocidad > optimalidad perfecta

## Extensiones Opcionales (Bonus)

Si el tiempo lo permite, considerar:

1. **Algoritmo Welsh-Powell:** Variante del codicioso con ordenamiento específico
2. **Visualización:** Función para imprimir el grafo coloreado con ASCII art
3. **Benchmarking:** Script que compare tiempos de ejecución vs fuerza bruta
4. **Heurísticas adicionales:** DSATUR, RLF, etc.

## Referencias

- Documentación teórica: `implementaciones/codicioso.md`
- Implementación de referencia: `brute_force_coloring.py`
- Estructura de datos: `graph.py`
- Paper de referencia: Welsh & Powell (1967) - "An upper bound for the chromatic number of a graph and its application to timetabling problems"

---

## Tips de Implementación y Debugging

### Estrategia de Desarrollo Incremental

1. **Paso 1:** Implementar `__init__` con validaciones
2. **Paso 2:** Implementar `color_graph()` solo con orden natural
3. **Paso 3:** Probar con grafos simples (1 nodo, 2 nodos conectados)
4. **Paso 4:** Agregar soporte para orden por grado
5. **Paso 5:** Implementar métodos auxiliares (`get_num_colors`, etc.)
6. **Paso 6:** Escribir y ejecutar todas las pruebas

### Debugging Checklist

Si la coloración falla, verificar:

- [ ] ¿Los nodos se están procesando en el orden correcto?
- [ ] ¿Se están recolectando correctamente los colores de vecinos?
- [ ] ¿El conjunto `forbidden_colors` se construye bien?
- [ ] ¿El color mínimo se encuentra correctamente?
- [ ] ¿Todos los nodos tienen entrada en `self.coloring`?
- [ ] ¿Las aristas del grafo son bidireccionales?

### Pruebas Manuales Rápidas

```python
# Grafo mínimo: K₂ (dos nodos conectados)
graph = Graph()
a, b = Node("A"), Node("B")
graph.add_node(a)
graph.add_node(b)
graph.add_edge(a, b)

greedy = GreedyColoring(graph)
coloring = greedy.color_graph()

# Debe ser: A=1, B=2 (o A=1, B=1 si hay error)
print(coloring)  # Debug
assert coloring[a] != coloring[b], "Vecinos tienen el mismo color!"
```

### Common Pitfalls (Errores Comunes)

1. **Olvidar ordenar los nodos:** Resultados inconsistentes
2. **No copiar la lista de vecinos:** Mutación accidental
3. **Indexación desde 0:** Los colores deben empezar en 1, no en 0
4. **No manejar grafos vacíos:** Debe lanzar excepción en `__init__`
5. **Comparar objetos Node incorrectamente:** Usar `==` (ya implementado en `graph.py`)
6. **No validar la estrategia de orden:** Aceptar valores inválidos

---

## Preguntas Frecuentes (FAQ)

### P1: ¿Por qué los colores empiezan en 1 y no en 0?

**R:** Convención matemática estándar en teoría de grafos. Los colores se numeran 1, 2, 3, ... en la literatura académica. Además, facilita contar: "usar 3 colores" significa colores {1, 2, 3}, no {0, 1, 2}.

### P2: ¿Qué estrategia de ordenamiento es mejor: natural o por grado?

**R:** Depende del grafo:
- **Orden por grado (Welsh-Powell):** Generalmente usa menos colores en grafos densos
- **Orden natural:** Más simple, resultados predecibles, útil para debugging
- **Recomendación:** Implementar ambas y permitir al usuario elegir

### P3: ¿Puede el algoritmo codicioso encontrar el número cromático?

**R:** Sí, en ciertos casos:
- Grafos bipartitos: Encuentra χ(G) = 2
- Ciclos pares: Encuentra χ(G) = 2
- Algunos grafos regulares
**Pero NO está garantizado en general.** Es una heurística, no un algoritmo exacto.

### P4: ¿Cuántos colores extra puede usar el codicioso?

**R:** En el peor caso, hasta Δ(G) + 1 colores (donde Δ es el grado máximo), pero típicamente mucho menos en grafos reales. Ejemplo:
- Grafo con χ(G) = 3, Δ(G) = 10
- Codicioso podría usar entre 3 y 11 colores (depende del orden)

### P5: ¿Debería implementar validación de ciclos en el grafo?

**R:** No es necesario. El algoritmo funciona correctamente con cualquier grafo no dirigido, incluyendo aquellos con ciclos, árboles, grafos completos, etc.

### P6: ¿Cómo manejar grafos con componentes desconectados?

**R:** El algoritmo funciona naturalmente:
- Los nodos en componentes diferentes pueden usar los mismos colores
- No requiere lógica especial
- Ejemplo: Dos triángulos desconectados → 3 colores total (no 6)

### P7: ¿Debo reutilizar colores cuando sea posible?

**R:** Sí, esa es la esencia del first-fit:
- Siempre busca el **color más bajo** disponible
- Reutiliza colores anteriores cuando no hay conflicto
- No crea nuevos colores innecesariamente

### P8: ¿Qué hacer si `get_neighbors()` retorna una lista vacía?

**R:** Un nodo sin vecinos puede usar cualquier color. El algoritmo first-fit le asignará color 1 (el mínimo disponible).

---

## Checklist de Entrega

- [ ] `greedy_coloring.py` implementado y funcional
- [ ] `test_greedy.py` con todos los casos de prueba
- [ ] `GREEDY_README.md` completo
- [ ] Todas las pruebas pasan exitosamente
- [ ] Ejemplos ejecutables funcionan sin errores
- [ ] Código sigue convenciones del proyecto
- [ ] Documentación clara y educativa

---

**Nota Final:** Este prompt está diseñado para que un desarrollador pueda implementar el algoritmo de manera autónoma, manteniendo la coherencia con el proyecto educativo existente. El énfasis está en la claridad, simplicidad y valor educativo del código resultante.
