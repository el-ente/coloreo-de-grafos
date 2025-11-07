# Script de Comparación de Algoritmos

## Descripción

`compare_algorithms.py` es un script educativo que compara el rendimiento y la calidad de tres algoritmos de coloreo de grafos:

1. **Fuerza Bruta** - Algoritmo exacto que garantiza la solución óptima
2. **Greedy First-Fit** - Algoritmo heurístico rápido pero potencialmente subóptimo
3. **Welsh-Powell** - Heurística mejorada que ordena por grado antes de colorear

## Uso

```bash
python3 compare_algorithms.py
```

## Ejemplos de Salida

El script prueba automáticamente varios tipos de grafos:

- **Ciclos (pares e impares)**: Demuestran cómo la paridad afecta el número cromático
- **Grafos completos (cliques)**: Muestran el peor caso (χ = n)
- **Grafos estrella**: Ejemplifican grafos fáciles de colorear (χ = 2)
- **Grafos bipartitos**: Casos donde todos los algoritmos encuentran la solución óptima

Para cada grafo, el script muestra:
- ⏱️ **Tiempo de ejecución** de cada algoritmo
- 🎨 **Número de colores** utilizados
- ✅ **Validez** del coloreo
- 📊 **Análisis comparativo** de optimalidad y velocidad

## Medición de Tiempo

Cada algoritmo ahora incluye medición precisa de tiempo:

### Brute Force
```python
bf = BruteForceColoring(graph)
coloring = bf.color_graph()
tiempo = bf.get_execution_time()
```

### Greedy
```python
greedy = GreedyColoring(graph)
coloring = greedy.color_graph()
tiempo = greedy.get_execution_time()
```

### Welsh-Powell
```python
coloring, tiempo = welsh_powell_coloring(graph)
```

## Resultados Típicos

Para un ciclo C5 (5 nodos):
- **Brute Force**: ~0.00006s, 3 colores (óptimo)
- **Greedy**: ~0.00001s, 3 colores (óptimo en este caso)
- **Welsh-Powell**: ~0.00001s, 3 colores (óptimo)

Para un grafo completo K5 (5 nodos):
- **Brute Force**: ~0.0006s, 5 colores (óptimo)
- **Greedy**: ~0.00001s, 5 colores (óptimo)
- **Welsh-Powell**: ~0.00002s, 5 colores (óptimo)

## Insights Educativos

El script demuestra claramente:

1. **Brute Force se vuelve impracticable** para grafos >10 nodos
2. **Greedy y Welsh-Powell son muy rápidos** incluso para grafos grandes
3. **Welsh-Powell generalmente usa igual o menos colores** que Greedy básico
4. La diferencia de velocidad es **dramática**: los algoritmos heurísticos pueden ser 40-50x más rápidos

## Propósito Educativo

Este script es ideal para:
- Entender trade-offs entre optimalidad y eficiencia
- Visualizar crecimiento exponencial vs polinomial
- Comparar algoritmos exactos vs heurísticos
- Aprender cuándo usar cada enfoque en la práctica
