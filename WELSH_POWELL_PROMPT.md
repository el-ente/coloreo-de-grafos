# Prompt: Implementación del Algoritmo Welsh-Powell en Python

## Objetivo
Implementar el algoritmo heurístico **Welsh-Powell** para coloreo de grafos en Python, siguiendo las convenciones del proyecto educativo y utilizando las estructuras de datos existentes definidas en `graph.py`.

## Contexto del Proyecto

Este es un proyecto **educativo** que explora algoritmos de coloreo de grafos. El código debe ser:
- **Simple y legible**: Priorizar claridad sobre optimización prematura
- **Bien documentado**: Docstrings en inglés, comentarios explicativos en español cuando sea necesario
- **Educativo**: El código debe ilustrar claramente el algoritmo descrito en `welsh-powell.md`

## Estructura de Datos Existente

El proyecto ya tiene definidas las clases `Node` y `Graph` en `graph.py`:

```python
class Node:
    - node_id: identificador único
    - data: datos opcionales del nodo
    
class Graph:
    - add_node(node): añade un nodo
    - add_edge(node1, node2): conecta dos nodos
    - get_nodes(): retorna todos los nodos
    - get_neighbors(node): retorna vecinos de un nodo
    - get_degree(node): retorna el grado de un nodo
    - has_edge(node1, node2): verifica si existe una arista
```

## Especificación del Algoritmo Welsh-Powell

### Descripción Conceptual
Welsh-Powell es una **heurística codiciosa** que mejora el coloreo básico mediante un ordenamiento inteligente: colorear primero los vértices con mayor grado (más conexiones), dejando los vértices más flexibles para el final.

### Pasos del Algoritmo
1. **Calcular grados**: Determinar el grado de cada vértice en el grafo
2. **Ordenar vértices**: Ordenar de mayor a menor grado
3. **Aplicar first-fit**: Para cada vértice en orden:
   - Examinar colores de vecinos ya coloreados
   - Asignar el primer color disponible (menor número positivo)
4. **Retornar resultado**: Diccionario {nodo: color}

### Complejidad
- **Tiempo**: O(n² + m) donde n = vértices, m = aristas
- **Espacio**: O(n) para almacenar coloreo y ordenamiento

## Requisitos de Implementación

### Archivo a Crear
**Nombre**: `welsh_powell_coloring.py`

### Función Principal
```python
def welsh_powell_coloring(graph):
    """
    Color a graph using the Welsh-Powell heuristic.
    
    This algorithm improves upon greedy first-fit by coloring
    high-degree vertices first, which are more constrained and
    harder to color later in the process.
    
    Args:
        graph: A Graph object with nodes and edges
        
    Returns:
        dict: A dictionary mapping each node to its assigned color (int)
              Colors start from 1 (not 0)
              
    Raises:
        ValueError: If graph is None or empty
        
    Example:
        >>> graph = Graph()
        >>> # ... add nodes and edges ...
        >>> coloring = welsh_powell_coloring(graph)
        >>> coloring[node_a]
        1
    """
```

### Algoritmo Paso a Paso

1. **Validación inicial**:
   - Verificar que el grafo no sea None
   - Verificar que el grafo tenga nodos
   - Lanzar ValueError con mensajes descriptivos si fallan

2. **Cálculo y ordenamiento**:
   - Obtener todos los nodos del grafo
   - Calcular el grado de cada nodo usando `graph.get_degree()`
   - Ordenar nodos en orden **descendente** por grado
   - En caso de empate en grados, mantener orden estable

3. **Coloreo greedy**:
   - Inicializar diccionario vacío para almacenar coloreo
   - Para cada nodo en la lista ordenada:
     - Obtener vecinos usando `graph.get_neighbors()`
     - Construir conjunto de colores usados por vecinos ya coloreados
     - Encontrar el primer color disponible (1, 2, 3, ...)
     - Asignar ese color al nodo actual

4. **Retorno**:
   - Devolver el diccionario completo {Node: int}

### Consideraciones de Implementación

**Variables clave**:
- `coloring = {}`: diccionario que mapea nodos a colores
- `sorted_nodes`: lista de nodos ordenados por grado descendente
- `neighbor_colors`: conjunto de colores de vecinos ya coloreados
- `color = 1`: variable para encontrar primer color disponible

**Lógica de asignación de color**:
```python
# Ejemplo de cómo encontrar el primer color disponible
color = 1
while color in neighbor_colors:
    color += 1
# color ahora contiene el primer entero positivo no usado
```

**Manejo de casos especiales**:
- Grafo vacío → ValueError
- Grafo con un solo nodo → color 1
- Nodos sin vecinos → pueden reutilizar color 1
- Grafo desconectado → funciona correctamente, cada componente se colorea independientemente

### Funciones Auxiliares (Opcional pero Recomendado)

```python
def get_sorted_nodes_by_degree(graph):
    """
    Sort graph nodes in descending order by degree.
    
    Helper function that encapsulates the sorting logic,
    making the main algorithm more readable.
    
    Args:
        graph: Graph object
        
    Returns:
        list: Nodes sorted by degree (highest first)
    """
    # Implementación aquí
```

```python
def get_first_available_color(neighbor_colors):
    """
    Find the smallest positive integer not in the set.
    
    Args:
        neighbor_colors: Set of integers representing used colors
        
    Returns:
        int: First available color (starting from 1)
    """
    # Implementación aquí
```

## Testing y Ejemplos

### Archivo de Pruebas
**Nombre**: `test_welsh_powell.py`

Debe incluir pruebas para:

1. **Grafo vacío**: Debe lanzar ValueError
2. **Grafo de un nodo**: Debe retornar {nodo: 1}
3. **Grafo triángulo** (K₃): Debe usar exactamente 3 colores
4. **Grafo bipartito**: Debe usar exactamente 2 colores
5. **Grafo estrella**: Debe usar 2 colores (centro y hojas)
6. **Grafo lineal** (cadena): Debe usar máximo 2 colores
7. **Comparación con greedy básico**: Welsh-Powell debe usar ≤ colores que greedy sin ordenamiento

### Ejemplo de Uso en Main

```python
if __name__ == "__main__":
    # Crear grafo de ejemplo (ciclo de 5 vértices)
    graph = Graph()
    
    nodes = [Node(f"v{i}") for i in range(1, 6)]
    for node in nodes:
        graph.add_node(node)
    
    # Crear ciclo: v1-v2-v3-v4-v5-v1
    graph.add_edge(nodes[0], nodes[1])
    graph.add_edge(nodes[1], nodes[2])
    graph.add_edge(nodes[2], nodes[3])
    graph.add_edge(nodes[3], nodes[4])
    graph.add_edge(nodes[4], nodes[0])
    
    # Aplicar Welsh-Powell
    coloring = welsh_powell_coloring(graph)
    
    # Mostrar resultados
    print("Welsh-Powell Coloring:")
    print(f"Graph: {graph}")
    
    for node in sorted(coloring.keys(), key=lambda n: n.id):
        degree = graph.get_degree(node)
        color = coloring[node]
        print(f"  {node.id} (degree {degree}): Color {color}")
    
    # Verificar corrección
    num_colors = len(set(coloring.values()))
    print(f"\nTotal colors used: {num_colors}")
    
    # Validar que no hay vecinos con el mismo color
    is_valid = True
    for node in graph.get_nodes():
        node_color = coloring[node]
        for neighbor in graph.get_neighbors(node):
            if coloring[neighbor] == node_color:
                print(f"ERROR: {node.id} and {neighbor.id} have same color!")
                is_valid = False
    
    if is_valid:
        print("✓ Coloring is valid (no adjacent nodes share colors)")
```

## Criterios de Calidad

### Código
- ✅ Usa las clases `Node` y `Graph` de `graph.py`
- ✅ Nombres de variables en inglés, descriptivos
- ✅ Docstrings completos en inglés siguiendo convenciones del proyecto
- ✅ Comentarios en español solo donde ayuden a la comprensión educativa
- ✅ Manejo de errores con mensajes claros
- ✅ Código simple y directo (evitar optimizaciones prematuras)

### Documentación
- ✅ Docstrings con Args, Returns, Raises, Example
- ✅ Explicación del propósito educativo del algoritmo
- ✅ Referencias a la complejidad computacional
- ✅ Ejemplos de uso ejecutables

### Testing
- ✅ Casos edge: grafos vacíos, nodos aislados, grafos triviales
- ✅ Casos típicos: grafos completos, bipartitos, ciclos
- ✅ Verificación de corrección: no vecinos con mismo color
- ✅ Verificación de optimalidad relativa: compara con número cromático conocido

## Entregables

1. **`welsh_powell_coloring.py`**: Implementación completa del algoritmo
2. **`test_welsh_powell.py`**: Suite de pruebas comprehensiva
3. **Documentación inline**: Docstrings y comentarios explicativos

## Referencias

- Documentación teórica: `implementaciones/welsh-powell.md`
- Estructura de datos: `graph.py`
- Ejemplo de implementación similar: `brute_force_coloring.py` (para convenciones de estilo)

---

**Nota final**: Este es un proyecto educativo. El código debe ser una herramienta de aprendizaje clara y accesible, no una implementación optimizada para producción. Prioriza la legibilidad y la correspondencia directa con la explicación teórica en `welsh-powell.md`.
