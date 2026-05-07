import sys
import os

# --- ARREGLO DE RUTA PARA SYMPY ---
ruta_libs = r'C:\Users\juanc\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\python312\site-packages'
if ruta_libs not in sys.path:
    sys.path.append(ruta_libs)
# --------------------------------------------------------------------------------

from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

# Inicializar el Supervisor
supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener los nodos
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella = supervisor.getFromDef("BOTELLA")

if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF 'pedestrian1'")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo con DEF 'BOTELLA'")

# Parámetros de movimiento
TAMANO_PASO = 0.05          
PASO_ANGULO = math.pi / 36  

# Offset local: [Adelante, Lado, Arriba] 
# Ajustado para que calce mejor en la mano derecha
offset_local = Matrix([0.08, -0.22, -0.5])

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rotacion = nodo.getField("rotation")
    rot = campo_rotacion.getSFRotation()
    angulo = rot[3]

    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])

    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial

    campo_traslacion.setSFVec3f([float(P_nueva[0]), float(P_nueva[1]), float(P_nueva[2])])

def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    rot = campo_rotacion.getSFRotation()
    angulo_actual = rot[3]
    campo_rotacion.setSFRotation([0, 0, 1, angulo_actual + delta_angulo])

def actualizar_botella():
    if nodo_peaton and nodo_botella:
        # --- SOLUCIÓN AL REBOTE: Reseteamos la física para que no caiga ---
        nodo_botella.resetPhysics()
        
        pos_robot = nodo_peaton.getField("translation").getSFVec3f()
        rot_robot = nodo_peaton.getField("rotation").getSFRotation()
        angulo = rot_robot[3]

        R_z = Matrix([
            [cos(angulo), -sin(angulo), 0],
            [sin(angulo),  cos(angulo), 0],
            [          0,            0, 1]
        ])

        P_robot = Matrix([pos_robot[0], pos_robot[1], pos_robot[2]])
        P_botella_mundial = P_robot + (R_z * offset_local)

        nodo_botella.getField("translation").setSFVec3f([
            float(P_botella_mundial[0]), 
            float(P_botella_mundial[1]), 
            float(P_botella_mundial[2])
        ])
        
        nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])

print("=== Control de teclado activo ===")

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:
        if tecla == Keyboard.UP: trasladar(nodo_peaton, TAMANO_PASO, 0.0)
        elif tecla == Keyboard.DOWN: trasladar(nodo_peaton, -TAMANO_PASO, 0.0)
        elif tecla == Keyboard.LEFT: trasladar(nodo_peaton, 0.0, TAMANO_PASO)
        elif tecla == Keyboard.RIGHT: trasladar(nodo_peaton, 0.0, -TAMANO_PASO)
        elif tecla == ord('Q'): rotar_z(nodo_peaton, PASO_ANGULO)
        elif tecla == ord('E'): rotar_z(nodo_peaton, -PASO_ANGULO)

    actualizar_botella()