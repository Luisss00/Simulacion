# Parcial de Simulaci�n - Juan Noguera

Razonamiento de las modificacionesArchivo

Implementación de la Botella y Solución de Errores

El objetivo principal fue lograr que la botella (BeerBottle) se mantuviera fija en la mano del humanoide.
Durante el proceso surgieron varios retos que se solucionaron así:

1.  El error de la "Botella Lluvia":Al principio, cada vez que el robot se movía, la botella aparecía en la mano pero inmediatamente caía del cielo o rebotaba como si estuviera lloviendo. Esto pasaba porque la gravedad de Webots intentaba tirarla al suelo mientras el código intentaba subirla a la mano.

Solución: Se eliminó el nodo de física (physics) en Webots y se agregó el comando nodo\*botella.resetPhysics() en el código. Con esto, la botella ignora la gravedad y se queda "pegada" donde el código le ordena

2. Calibración del Offset (La botella en el hombro):Al principio la botella aparecía incrustada en el hombro o flotando muy arriba.Solución: Ajustamos manualmente los valores del vector offset_local hasta encontrar el punto exacto de la mano derecha, bajando el valor de Z a -0.5.3. Lógica Matemática (Matriz de Rotación):Para que la botella no se quedara atrás cuando el robot giraba, aplicamos una matriz de rotación en Z
