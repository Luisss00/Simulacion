import sys
import os
from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math


supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener nodos
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella = supervisor.getFromDef("BOTELLA")

if nodo_peaton is None or nodo_botella is None:
    print("ERROR: Verifica que los DEF sean 'pedestrian1' y 'BOTELLA' en el árbol de Webots")

# Parámetros de movimiento
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# --- OFFSET DE LA MANO (CALIBRACIÓN FINAL) ---
# [X: adelante, Y: lado (derecha es negativo), Z: altura]
# Bajamos el valor de Z para que llegue a la mano. 
offset_mano_local = Matrix([0.02, -0.20, -0.50])

teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def trasladar(nodo, dx_local, dy_local):
    campo_tras = nodo.getField("translation")
    pos = campo_tras.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rot = nodo.getField("rotation")
    rot = campo_rot.getSFRotation()
    angulo = rot[3]

    # Matriz de rotación R_z(θ)
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,             0, 1]
    ])

    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial

    campo_tras.setSFVec3f([float(P_nueva[0]), float(P_nueva[1]), float(P_nueva[2])])

def rotar_z(nodo, delta_angulo):
    campo_rot = nodo.getField("rotation")
    rot = campo_rot.getSFRotation()
    angulo_actual = rot[3]
    campo_rot.setSFRotation([0, 0, 1, angulo_actual + delta_angulo])

def actualizar_botella():
    if nodo_peaton and nodo_botella:
        # Reset de física para evitar que la botella rebote por colisiones
        nodo_botella.resetPhysics()

        pos_robot = nodo_peaton.getField("translation").getSFVec3f()
        rot_robot = nodo_peaton.getField("rotation").getSFRotation()
        angulo = rot_robot[3]

        # Matriz de rotación actual del robot
        R_z = Matrix([
            [cos(angulo), -sin(angulo), 0],
            [sin(angulo),  cos(angulo), 0],
            [          0,             0, 1]
        ])

        P_robot = Matrix([pos_robot[0], pos_robot[1], pos_robot[2]])
        
        # TRANSFORMACIÓN MATRICIAL SOLIDARIA (Punto c.iv)
        # Calculamos la posición de la botella: P_w = P_robot + R_z * offset_local
        P_botella_mundial = P_robot + (R_z * offset_mano_local)

        # Aplicar posición calculada a la botella
        nodo_botella.getField("translation").setSFVec3f([
            float(P_botella_mundial[0]), 
            float(P_botella_mundial[1]), 
            float(P_botella_mundial[2])
        ])
        
        # Sincronizar la rotación de la botella con la del humanoide
        nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])

print("=== Controlador Iniciado - Movimiento Sincronizado ===")

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()

    if tecla != -1:
        if tecla == Keyboard.UP:
            trasladar(nodo_peaton, TAMANO_PASO, 0.0)
        elif tecla == Keyboard.DOWN:
            trasladar(nodo_peaton, -TAMANO_PASO, 0.0)
        elif tecla == Keyboard.LEFT:
            trasladar(nodo_peaton, 0.0, TAMANO_PASO)
        elif tecla == Keyboard.RIGHT:
            trasladar(nodo_peaton, 0.0, -TAMANO_PASO)
        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)
        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)

    # Actualización constante de la posición de la botella
    actualizar_botella()