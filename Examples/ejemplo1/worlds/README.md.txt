# Proyecto de Simulación Webots - Control de Peatón y una botella en la mano
**Estudiante:** Rina Marriaga
## Descripción del Parcial
Este parcial consiste en la implementación de un controlador de Webots utilizando Python para manejar un peatón (`pedestrian1`) mediante el teclado. Además, se implementó un objeto (`botella_en_mano`) y que este siga el movimiento y la rotación del peatón, simulando que este lo lleva en su mano derecha.
## Funcionalidades implementadas
* **Control por Teclado:** Movimiento hacia adelante, atrás, izquierda y derecha.
* **Rotación:** Rotación sobre el eje Z (teclas Q y E).
* **Transformación de Coordenadas:** Conversión de desplazamientos locales a mundiales para que el movimiento sea relativo a la orientación del peatón.
* **Acoplamiento Dinámico:** Cálculo de posición relativa en tiempo real para que la botella se mantenga fija respecto a la mano del peatón mientras este se mueve y gira.

Para este parcial, mi objetivo fue transformar un objeto que inicialmente era estático en algo que se moviera de forma dinámica con el personaje. Al principio, la botella estaba ahí en la escena, pero no reaccionaba a nada, así que lo primero que hice fue "presentársela" al programa. Usé el identificador DEF botella_en_mano para que el código la reconociera y pudiera darle órdenes. Además, le puse las físicas en NULL para que no se cayera por gravedad y yo pudiera controlar su posición exacta por código. 
El programa me permite mover al pedestrian1 con el teclado, pero el verdadero reto fue que la botella lo siguiera sin errores. Para eso, definí tres distancias (x, y, z) que representan el espacio entre el cuerpo del peatón y su mano. Fui ajustando estos valores hasta que cuadraron: 
# --- Desplazamiento local de la botella_en_mano respecto al peatón (mano derecha) ---
desp_x = 0.0   # adelante
desp_y = -0.25   # lateral
desp_z = -0.7  # altura
Lo complicado es que estas distancias son "locales", es decir, dependen de hacia dónde esté mirando el peatón. Si él gira, su "derecha" ya no es la misma que la del mapa, por lo que no podía simplemente sumar coordenadas fijas. Para solucionar esto, dentro del bucle de la simulación, el programa obtiene la posición y rotación del peatón muchas veces por segundo. Con esos datos, aplico una matriz de rotación (usando senos y cosenos descritos en el programa) para convertir ese desplazamiento local en coordenadas globales del mundo. 
Finalmente, para que la botella también girara junto al peatón, actualizaba continuamente su rotación utilizando el mismo ángulo del humanoide:
nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo_peaton])
El vector [0,0,1] representa el eje Z, que es el eje vertical sobre el que gira el peatón.
Todo esto se ejecuta dentro del ciclo principal de simulación, por lo que en cada fotograma la botella actualiza su posición y orientación. Gracias a eso el resultado final hace que parezca que la botella realmente está siendo sostenida por el humanoide mientras camina y rota en la escena y que esta reconozca el entorno y se mueva en tiempo real con precisión.
