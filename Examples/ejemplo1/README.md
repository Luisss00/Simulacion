# Reporte de Modificaciones - Parcial Simulación y Robótica

**Estudiante:** [HENRY CAMARGO]
**Fecha:** 6 de Mayo, 2026

## 1. Introducción
En este ejercicio se integró un objeto dinámico (`BeerBottle`) al entorno de simulación, vinculando su comportamiento al movimiento de un humanoide (`pedestrian1`). El reto principal consistió en mantener la botella en la mano del personaje utilizando álgebra matricial para transformar sistemas de referencia.

## 2. Razonamiento Lógico y Matemático

# A. Ubicación y Offset
Para que la botella no apareciera en el centro del personaje, definí un vector de desplazamiento local llamado `OFFSET_MANO`. 
* **Reto:** Como el personaje se mueve y rota, un valor fijo en coordenadas globales no servía. 
* **Solución:** El offset se definió relativo al origen del humanoide, ajustando los ejes para que coincidiera visualmente con la posición de su mano derecha.

# B. Uso de Matrices de Rotación ($R_z$ y $R_y$)
Para cumplir con el requerimiento de álgebra vectorial, implementé dos transformaciones clave:

1. **Transformación de Traslación:** Multipliqué el `OFFSET_MANO` por la matriz de rotación del personaje ($R_z$). Esto asegura que si el robot gira hacia la izquierda, la botella "orbite" con él y se mantenga en el mismo lado de su cuerpo. La fórmula aplicada fue: 
   $$P_{botella} = P_{humanoide} + (R_z(\theta) \cdot Offset_{local})$$

2. **Inclinación de la Botella:** Para darle más realismo, decidí que la botella no estuviera totalmente vertical. Apliqué una matriz de rotación en el eje Y ($R_y$) con un ángulo de $0.5$ radianes. Al multiplicar la rotación del personaje por esta inclinación, logré que la botella siempre se incline "hacia adelante" respecto al frente del robot.

# C. Conversión a Axis-Angle
Webots no acepta matrices directamente para el campo `rotation`. Por lo tanto, implementé un algoritmo para extraer el **Eje de rotación** y el **Ángulo (theta)** a partir de la matriz de rotación total resultante. Esto garantiza que la orientación de la botella sea matemáticamente exacta en cada paso de tiempo.

# 3. Conclusión
El controlador ahora sincroniza en cada ciclo la posición y orientación de ambos nodos. El uso de la librería `sympy` facilitó el manejo de las matrices, permitiendo que la lógica sea escalable para cualquier otro objeto que se quiera vincular al sistema de referencia del robot.