# Coloreo de Grafos - Proyecto Educativo

Un proyecto integral sobre **algoritmos de coloreo de grafos** que combina documentación teórica con implementaciones prácticas en Python.

## 📁 Estructura del Proyecto

```
coloreo-grafos/
├── README.md                          # Este archivo - guía general del proyecto
├── coloreo-de-grafos.md              # Documentación principal con teoría completa
├── graph.py                          # Clases base: Node y Graph (lista de adyacencia)
├── brute_force_coloring.py           # Algoritmo 1: Fuerza Bruta (búsqueda exhaustiva)
├── test_brute_force.py               # Tests unitarios para fuerza bruta
├── BRUTE_FORCE_README.md             # Documentación específica de fuerza bruta
├── presentacion.html                 # Presentación interactiva (Reveal.js)
└── implementaciones/                 # Carpeta con documentación de algoritmos
    ├── implementaciones.md           # Índice de algoritmos
    ├── fuerza-bruta.md              # Explicación teórica: Fuerza Bruta
    ├── codicioso.md                 # Explicación teórica: Algoritmo Codicioso
    └── welsh-powell.md              # Explicación teórica: Welsh-Powell
```

## 🎯 Descripción de Archivos Clave

### Documentación Teórica

| Archivo | Contenido |
|---------|----------|
| **coloreo-de-grafos.md** | Teoría completa: conceptos, aplicaciones, definiciones formales |
| **implementaciones/fuerza-bruta.md** | Explicación detallada del algoritmo de fuerza bruta |
| **implementaciones/codicioso.md** | Algoritmo codicioso y su heurística |
| **implementaciones/welsh-powell.md** | Algoritmo Welsh-Powell mejorado |
| **implementaciones/implementaciones.md** | Índice y comparativa de algoritmos |

### Código Python

| Archivo | Clase/Función Principal | Propósito |
|---------|------------------------|----------|
| **graph.py** | `Node`, `Graph` | Estructura de datos base para representar grafos con lista de adyacencia |
| **brute_force_coloring.py** | `BruteForceColoring` | Implementación del algoritmo exacto mediante búsqueda exhaustiva |

### Tests y Ejemplos

| Archivo | Descripción |
|---------|------------|
| **test_brute_force.py** | Tests unitarios para validar la implementación de fuerza bruta |
| **BRUTE_FORCE_README.md** | Documentación específica con ejemplos de uso |

### Presentación

| Archivo | Descripción |
|---------|------------|
| **presentacion.html** | Presentación interactiva con Reveal.js sobre coloreo de grafos |

## 🚀 Cómo Usar el Proyecto

### Ejecutar el Ejemplo de Fuerza Bruta

```bash
python brute_force_coloring.py
```

Este comando ejecuta ejemplos educativos:
- Colorea un grafo de 4 nodos
- Colorea un triángulo (K3)
- Muestra validaciones y números cromáticos

### Ejecutar Tests

```bash
python -m pytest test_brute_force.py -v
```

### Ver la Presentación

Abre `presentacion.html` en un navegador web para ver la presentación interactiva.

## 📚 Algoritmos Implementados

### 1. Fuerza Bruta (Brute Force)
- **Archivo**: `brute_force_coloring.py`
- **Tipo**: Algoritmo exacto
- **Complejidad**: O(k^n × E) donde k=colores, n=nodos, E=aristas
- **Características**: 
  - Encuentra siempre la solución óptima
  - Impractico para grafos grandes (>15-20 nodos)
  - Ideal para entender el problema fundamentalmente

### 2. Codicioso (Greedy) - En Desarrollo
- **Documentación**: `implementaciones/codicioso.md`
- **Tipo**: Algoritmo heurístico
- **Ventaja**: Rápido O(n²)
- **Desventaja**: No siempre óptimo

### 3. Welsh-Powell - En Desarrollo
- **Documentación**: `implementaciones/welsh-powell.md`
- **Tipo**: Algoritmo heurístico mejorado
- **Ventaja**: Generalmente mejor que codicioso
- **Desventaja**: Aún no es óptimo

## 🏗️ Estructura de Datos

### Clase `Node`
```python
node = Node("A", data=None)
# Representa un vértice del grafo
# Atributos: id, data (opcional)
```

### Clase `Graph`
```python
graph = Graph()
graph.add_node(node_a)
graph.add_edge(node_a, node_b)
graph.get_neighbors(node_a)
graph.get_degree(node_a)
```

Implementa lista de adyacencia para eficiencia O(1) en consultas de vecinos.

## 📖 Lectura Recomendada

1. **Empezar aquí**: `coloreo-de-grafos.md` para conceptos teóricos
2. **Entender algoritmos**: `implementaciones/implementaciones.md` para comparativa
3. **Estudiar código**: `brute_force_coloring.py` con ejemplos ejecutables
4. **Ver presentación**: `presentacion.html` para visualización interactiva

## 🎓 Propósito Educativo

Este proyecto está diseñado para:
- ✅ Entender conceptos fundamentales del coloreo de grafos
- ✅ Aprender diferentes estrategias algorítmicas (exactas vs heurísticas)
- ✅ Analizar complejidad computacional (NP-completitud)
- ✅ Experimentar con código ejecutable
- ✅ Ver aplicaciones prácticas en computación

## 💡 Temas Cubiertos

- Teoría de grafos básica
- Definición formal de coloreo de grafos
- Número cromático y cotas teóricas
- Aplicaciones prácticas (horarios, mapas, compiladores)
- Análisis de complejidad temporal y espacial
- Comparación de enfoques algorítmicos

## 🔧 Requisitos

- Python 3.7+
- `itertools` (incluido en stdlib)
- `pytest` (opcional, para ejecutar tests)

## 📝 Notas de Desarrollo

- **Idioma**: Español para documentación, inglés para código
- **Estilo**: Énfasis en claridad y propósito educativo
- **Código**: Ejemplos simples y bien documentados

## 🤝 Contribuciones

Para mantener consistencia:
- Seguir el estilo educativo existente
- Incluir análisis de complejidad
- Usar diagramas Mermaid para visualizaciones
- Documentar en español (teoría) e inglés (código)

---

**Última actualización**: 5 de noviembre de 2025
