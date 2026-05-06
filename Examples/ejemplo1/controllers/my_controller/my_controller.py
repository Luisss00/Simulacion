from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener el nodo del humanoide
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF del humanoide")

# AGREGADO: Obtener el nodo de la botella
nodo_botella = supervisor.getFromDef("BEER_BOTTLE")
if nodo_botella is None:
    print("ADVERTENCIA: No se encontró el nodo BEER_BOTTLE")

# Parámetros de movimiento
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])
    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial
    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])

# AGREGADO: Mantener botella en mano derecha usando algebra matricial
def actualizar_botella():
    if nodo_botella is None or nodo_peaton is None:
        return
    pos = nodo_peaton.getField("translation").getSFVec3f()
    P_humanoide = Matrix([pos[0], pos[1], pos[2]])
    _, _, _, angulo = nodo_peaton.getField("rotation").getSFRotation()
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])
    offset_local = Matrix([0.1, -0.3, -0.5])
    offset_global = R_z * offset_local
    P_botella = P_humanoide + offset_global
    nodo_botella.getField("translation").setSFVec3f([
        float(P_botella[0]),
        float(P_botella[1]),
        float(P_botella[2])
    ])
    nodo_botella.resetPhysics()

print("=== Control de teclado ===")
print("↑ / ↓  → Mover adelante / atrás")
print("← / →  → Mover izquierda / derecha")
print("Q / E  → Rotar antihorario / horario")
print("==========================")

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()
    if nodo_peaton is not None and tecla != -1:
        if tecla == Keyboard.UP:
            print("Adelante")
            trasladar(nodo_peaton, TAMANO_PASO, 0.0)
        elif tecla == Keyboard.DOWN:
            print("Atras")
            trasladar(nodo_peaton, -TAMANO_PASO, 0.0)
        elif tecla == Keyboard.LEFT:
            print("Izquierda")
            trasladar(nodo_peaton, 0.0, TAMANO_PASO)
        elif tecla == Keyboard.RIGHT:
            print("Derecha")
            trasladar(nodo_peaton, 0.0, -TAMANO_PASO)
        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)
        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)
    # AGREGADO: botella sigue mano derecha en cada frame
    actualizar_botella()