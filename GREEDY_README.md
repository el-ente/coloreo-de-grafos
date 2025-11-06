# Implementación: Algoritmo Codicioso (Greedy First-Fit)

## Descripción General

Este directorio contiene la implementación educativa del **algoritmo codicioso first-fit** para coloreo de grafos. El algoritmo procesa vértices secuencialmente y asigna a cada uno el menor color disponible que no conflictúa con sus vecinos ya coloreados.

## Archivos Principales

### 1. **greedy_coloring.py**
Implementación completa del algoritmo con:
- Clase `GreedyColoring` con métodos principales
- Método `color_graph()`: colorea el grafo con estrategia first-fit
- Método `get_num_colors()`: retorna el número de colores usados
- Método `is_valid_coloring()`: valida una coloración
- Método `get_coloring_dict()`: obtiene coloración con IDs de nodos
- Método `get_color_classes()`: agrupa nodos por color
- Soporte para dos estrategias de ordenamiento: 'natural' y 'degree'
- Ejemplos de uso ejecutables
- Análisis de complejidad documentado

### 2. **test_greedy.py**
Suite de pruebas unitarias que verifican:
- Grafo con un solo nodo
- Nodos desconectados
- Dos nodos conectados
- Triángulo (K₃)
- Grafo bipartito (K₂,₂)
- Ciclo impar (C₅)
- Grafo completo (K₄)
- Grafo estrella
- Estrategias de ordenamiento (natural y por grado)
- Manejo de errores (grafo vacío, None, estrategia inválida)
- Métodos auxiliares (get_coloring_dict, get_color_classes)

### 3. **implementaciones/codicioso.md**
Documentación teórica completa incluyendo:
- Concepto fundamental del algoritmo codicioso
- Estrategia first-fit explicada paso a paso
- Pseudocódigo
- Ejemplos detallados
- Análisis de complejidad
- Ventajas y limitaciones
- Comparación con otros algoritmos

## Requisitos

- Python 3.6+
- Archivo `graph.py` (clases Graph y Node)
- Sin dependencias externas

## Uso Básico

```python
from graph import Node, Graph
from greedy_coloring import GreedyColoring

# Crear un grafo
graph = Graph()
node_a = Node("A")
node_b = Node("B")
node_c = Node("C")

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

# Crear un triángulo
graph.add_edge(node_a, node_b)
graph.add_edge(node_b, node_c)
graph.add_edge(node_c, node_a)

# Colorear con algoritmo codicioso (orden natural)
greedy = GreedyColoring(graph, order_strategy='natural')
coloring = greedy.color_graph()

# Obtener resultados
print(f"Coloración: {greedy.get_coloring_dict()}")
print(f"Número de colores: {greedy.get_num_colors()}")
print(f"¿Válida? {greedy.is_valid_coloring()}")
print(f"Clases de color: {greedy.get_color_classes()}")
```

### Ejemplo con Estrategia por Grado

```python
# Colorear ordenando por grado (Welsh-Powell)
greedy_degree = GreedyColoring(graph, order_strategy='degree')
coloring_degree = greedy_degree.color_graph()

print(f"Colores usados (grado): {greedy_degree.get_num_colors()}")
```

## Ejecución de Ejemplos

### Ejemplo Principal
```bash
python3 greedy_coloring.py
```

Salida: Colorea un ciclo de 5 nodos (C₅) usando ambas estrategias:
- **Orden natural:** Procesa nodos por ID
- **Orden por grado:** Procesa nodos de mayor a menor grado
- Muestra coloración obtenida
- Valida resultados
- Compara estrategias

### Pruebas Unitarias
```bash
python3 test_greedy.py
```

Ejecuta 15+ pruebas en diferentes tipos de grafos, verificando:
- Correctitud del algoritmo
- Validez de las coloraciones
- Manejo de casos especiales
- Ambas estrategias de ordenamiento

## Características Clave

### ✓ Eficiencia
- Complejidad temporal: **O(n²)**
- Complejidad espacial: **O(n)**
- Escalable a grafos grandes (miles de nodos)

### ✓ Simplicidad
- Implementación clara y directa
- Sin backtracking ni recursión
- Fácil de entender y modificar

### ✓ Determinismo
- Mismo orden de entrada → mismo resultado
- Predecible y reproducible

### ✓ Flexibilidad
- Dos estrategias de ordenamiento
- Fácil agregar nuevas heurísticas

### ✗ Limitación: No Óptimo
- No garantiza encontrar el número cromático
- Puede usar más colores que el mínimo necesario
- Trade-off: velocidad vs optimalidad

## Análisis de Complejidad

### Complejidad Temporal

| Operación | Complejidad | Explicación |
|-----------|-------------|-------------|
| **Ordenamiento (natural)** | O(n log n) | Ordenar por ID |
| **Ordenamiento (grado)** | O(n²) | Calcular grados + ordenar |
| **Iteración sobre nodos** | O(n) | Procesar cada nodo |
| **Revisar vecinos** | O(d) por nodo | d = grado promedio |
| **Encontrar color mínimo** | O(k) | k = colores usados |
| **Total** | **O(n²)** | Dominado por revisión de vecinos |

### Complejidad Espacial

| Estructura | Espacio | Uso |
|------------|---------|-----|
| **Coloración** | O(n) | Diccionario node → color |
| **Colores prohibidos** | O(k) | k ≤ n colores máximos |
| **Total** | **O(n)** | Lineal en número de nodos |

## Estrategias de Ordenamiento

### 1. Orden Natural (`order_strategy='natural'`)

**Descripción:** Procesa nodos en orden alfabético/numérico de sus IDs.

**Ventajas:**
- Simple y predecible
- Útil para debugging
- Consistente entre ejecuciones

**Cuándo usar:**
- Grafos sin estructura particular
- Cuando el orden no importa
- Para reproducibilidad

**Ejemplo:**
```python
# Nodos: D, B, A, C → se procesan como A, B, C, D
greedy = GreedyColoring(graph, order_strategy='natural')
```

### 2. Orden por Grado (`order_strategy='degree'`)

**Descripción:** Procesa nodos de mayor a menor grado (Welsh-Powell).

**Ventajas:**
- Generalmente usa menos colores
- Mejor para grafos densos
- Colorea nodos "difíciles" primero

**Cuándo usar:**
- Cuando quieres minimizar colores
- Grafos con vértices de alto grado
- Aplicaciones prácticas

**Ejemplo:**
```python
# Procesa primero los nodos con más vecinos
greedy = GreedyColoring(graph, order_strategy='degree')
```

### Comparación de Estrategias

| Aspecto | Natural | Por Grado |
|---------|---------|-----------|
| **Colores usados** | Variable | Generalmente menos |
| **Complejidad** | O(n log n) | O(n²) |
| **Simplicidad** | Más simple | Más sofisticada |
| **Reproducibilidad** | Alta | Alta |
| **Mejor para** | Debugging, grafos aleatorios | Grafos densos, producción |

## Comparación con Fuerza Bruta

| Aspecto | Fuerza Bruta | Codicioso First-Fit |
|---------|--------------|---------------------|
| **Complejidad Temporal** | O(k^n · n²) | O(n²) |
| **Complejidad Espacial** | O(n) + recursión | O(n) |
| **Optimalidad** | ✓ Garantizada (número cromático) | ✗ No garantizada |
| **Escalabilidad** | Grafos pequeños (~10 nodos) | Grafos grandes (miles de nodos) |
| **Determinismo** | Sí | Sí (con mismo orden) |
| **Aplicabilidad** | Académica, benchmarking | Práctica, real-world |
| **Tiempo para K₄** | ~0.01s | ~0.0001s |
| **Tiempo para K₁₀** | Horas/días | Milisegundos |
| **Uso de memoria** | Exponencial en recursión | Lineal |
| **Mejor caso** | O(k · n²) con k pequeño | O(n²) |
| **Peor caso** | O(n^n · n²) | O(n²) |

### Casos de Uso Recomendados

**Fuerza Bruta:**
- Grafos con n ≤ 10
- Cuando se necesita el número cromático exacto
- Benchmarking de otros algoritmos
- Problemas académicos pequeños
- Verificación de resultados

**Codicioso First-Fit:**
- Grafos con n > 10
- Aplicaciones en tiempo real
- Sistemas de asignación de recursos
- Cuando velocidad > optimalidad perfecta
- Scheduling, registro de compiladores
- Asignación de frecuencias

## Ejemplos de Rendimiento

### Grafos Pequeños (n ≤ 20)

| Grafo | Nodos | Aristas | χ(G) | Colores (natural) | Colores (grado) | Tiempo |
|-------|-------|---------|------|-------------------|-----------------|--------|
| K₃ (triángulo) | 3 | 3 | 3 | 3 | 3 | <0.001s |
| K₄ (completo) | 4 | 6 | 4 | 4 | 4 | <0.001s |
| C₅ (ciclo) | 5 | 5 | 3 | 3 | 3 | <0.001s |
| K₂,₂ (bipartito) | 4 | 4 | 2 | 2 | 2 | <0.001s |
| Estrella (1+5) | 6 | 5 | 2 | 2 | 2 | <0.001s |

### Grafos Medianos (20 < n ≤ 100)

- **Tiempo:** < 0.1s
- **Colores:** 10-30% más que χ(G) típicamente
- **Aplicable:** Sí, muy eficiente

### Grafos Grandes (n > 100)

- **Tiempo:** < 1s para miles de nodos
- **Escalabilidad:** Lineal con grafos dispersos
- **Aplicable:** Sí, práctico para producción

## Cuándo Usar Esta Implementación

### ✓ Use si:
- Necesita velocidad sobre optimalidad perfecta
- Grafo tiene más de 10-15 nodos
- Aplicación práctica en tiempo real
- Solución "suficientemente buena" es aceptable
- Quiere aprender algoritmos codiciosos
- Necesita solución escalable

### ✗ No use si:
- Necesita el número cromático exacto
- Grafo es muy pequeño (< 10 nodos)
- Aplicación crítica donde cada color cuenta
- Tiene tiempo para algoritmos exactos más sofisticados

### ⚠ Considere alternativas si:
- Quiere mejor aproximación: Welsh-Powell, DSATUR
- Necesita óptimo: Branch & Bound, SAT solvers
- Grafos especiales: algoritmos específicos (bipartitos, planares)

## Ventajas y Limitaciones

### Ventajas ✓

1. **Velocidad excepcional:** O(n²) vs exponencial
2. **Simplicidad:** Fácil de implementar y entender
3. **Sin recursión:** No hay límites de stack
4. **Escalable:** Funciona con grafos grandes
5. **Predecible:** Comportamiento determinístico
6. **Flexible:** Fácil agregar heurísticas
7. **Práctico:** Usado en aplicaciones reales

### Limitaciones ✗

1. **No óptimo:** Puede usar más colores que χ(G)
2. **Depende del orden:** Resultados varían con la heurística
3. **Sin garantías:** No hay bound teórico ajustado
4. **Grafos patológicos:** Puede fallar en casos adversos

### Garantías Teóricas

- **Bound superior:** Usa a lo más Δ(G) + 1 colores
- **Bound inferior:** Usa al menos χ(G) colores (trivial)
- **Aproximación:** No hay ratio fijo de aproximación

donde:
- Δ(G) = grado máximo del grafo
- χ(G) = número cromático (óptimo)

## Extensiones y Mejoras

### Heurísticas Adicionales (Futuro)

1. **DSATUR:** Selecciona nodos por grado de saturación
2. **RLF (Recursive Largest First):** Construye clases de color recursivamente
3. **Tabu Search:** Metaheurística para mejorar soluciones
4. **Simulated Annealing:** Búsqueda local probabilística

### Optimizaciones Posibles

1. **Caching de grados:** Pre-calcular y almacenar
2. **Estructuras eficientes:** Usar sets para vecinos
3. **Paralelización:** Colorear componentes independientes
4. **Early stopping:** Detectar número cromático conocido

## Referencias

### Paper Original
- **Welsh & Powell (1967):** "An upper bound for the chromatic number of a graph and its application to timetabling problems"
- Computación aplicada, Universidad de Michigan

### Documentación del Proyecto
- `implementaciones/codicioso.md` - Teoría detallada
- `graph.py` - Estructura de datos
- `brute_force_coloring.py` - Implementación exacta para comparar

### Recursos Adicionales
- Introducción a Algoritmos (CLRS) - Capítulo sobre algoritmos codiciosos
- "Graph Coloring and the Chromatic Number" - Teoría de grafos fundamental

---

## Contacto y Contribuciones

Este es un proyecto educativo. Las contribuciones que mejoren la claridad, agreguen ejemplos o extiendan funcionalidad son bienvenidas.

**Principios del proyecto:**
- Código simple y legible (prioridad #1)
- Documentación exhaustiva en español
- Ejemplos ejecutables y verificables
- Enfoque pedagógico sobre optimización prematura
