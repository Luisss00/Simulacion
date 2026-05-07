Paso a paso de lo que hice en la simulación
Instalé y abrí Webots R2025a.
Creé un nuevo proyecto de simulación.
Dentro del proyecto se creó la carpeta worlds y el archivo t1.wbt.
Agregué el fondo y la iluminación usando:
TexturedBackground
TexturedBackgroundLight
Añadí una arena rectangular para usarla como piso de la simulación.
Inserté un humanoide tipo Pedestrian en la escena.
Cambié la posición y rotación inicial del humanoide para colocarlo dentro de la arena.
Agregué una botella BeerBottle cerca del personaje.
Creé un robot supervisor invisible.
Activé la opción:
supervisor TRUE

Esto permitió controlar objetos de la escena desde Python.

Creé el controlador my_controller.py.
Importé las librerías necesarias:
from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math
Inicialicé el supervisor y el teclado.
Busqué el nodo del humanoide usando:
supervisor.getFromDef("pedestrian1")
Programé el movimiento del personaje usando traslaciones y rotaciones.
Configuré las teclas del teclado:
Arriba → avanzar
Abajo → retroceder
Izquierda → girar izquierda
Derecha → girar derecha
Implementé una función para mover el humanoide según su orientación actual.
Actualicé la posición del personaje en cada paso de simulación.
Probé la simulación presionando Play en Webots.
Verifiqué que el humanoide se moviera correctamente dentro de la arena junto con la botella.