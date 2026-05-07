from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# ---------------------------------------------------------------
# Obtener nodos de la escena
# ---------------------------------------------------------------
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella = supervisor.getFromDef("botella")

if nodo_peaton is None:
    print("ERROR: No se encontró el nodo 'pedestrian1'")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo 'botella'")

# ---------------------------------------------------------------
# Desactivar física de la botella para que no caiga por gravedad
# ---------------------------------------------------------------
if nodo_botella is not None:
    campo_fisica = nodo_botella.getField("physics")
    if campo_fisica is not None:
        campo_fisica.setSFNode(None)

# ---------------------------------------------------------------
# Guardar la altura Z original del humanoide (nunca debe cambiar)
# ---------------------------------------------------------------
Z_FIJO = nodo_peaton.getField("translation").getSFVec3f()[2]

# ---------------------------------------------------------------
# Parámetros de movimiento
# ---------------------------------------------------------------
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36  # 5 grados

# ---------------------------------------------------------------
# Offset de la mano derecha en el sistema LOCAL del humanoide
# [adelante, derecha, altura]
# ---------------------------------------------------------------
OFFSET_MANO_DERECHA = Matrix([-0.10, -0.22, -0.45])

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)


# ---------------------------------------------------------------
# Construye la matriz homogénea 4x4 del humanoide
#
#       | cos θ  -sin θ  0  Px |
#  T =  | sin θ   cos θ  0  Py |
#       |   0      0     1  Pz |
#       |   0      0     0   1 |
#
# Transforma puntos del sistema LOCAL al sistema MUNDIAL
# ---------------------------------------------------------------
def obtener_T_humanoide(nodo):
    pos = nodo.getField("translation").getSFVec3f()
    Px, Py, Pz = pos[0], pos[1], pos[2]

    _, _, _, angulo = nodo.getField("rotation").getSFRotation()

    T = Matrix([
        [cos(angulo), -sin(angulo), 0, Px],
        [sin(angulo),  cos(angulo), 0, Py],
        [          0,            0, 1, Pz],
        [          0,            0, 0,  1]
    ])
    return T


# ---------------------------------------------------------------
# Calcula la posición mundial de la mano derecha
#
# P_mundial = T_humanoide * [ox, oy, oz, 1]^T
#
# Al multiplicar el offset local por la matriz homogénea,
# obtenemos la posición correcta en el mundo sin importar
# hacia dónde esté rotado o trasladado el humanoide.
# ---------------------------------------------------------------
def calcular_posicion_mano(nodo):
    T = obtener_T_humanoide(nodo)

    offset_h = Matrix([
        OFFSET_MANO_DERECHA[0],
        OFFSET_MANO_DERECHA[1],
        OFFSET_MANO_DERECHA[2],
        1
    ])

    P_mundial = T * offset_h
    return [float(P_mundial[0]), float(P_mundial[1]), float(P_mundial[2])]


# ---------------------------------------------------------------
# Trasladar humanoide conservando Z fijo para evitar caída
# P_nueva = P_vieja + R_z(θ) * d_local
# ---------------------------------------------------------------
def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], Z_FIJO])

    _, _, _, angulo = nodo.getField("rotation").getSFRotation()

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
        Z_FIJO
    ])


# ---------------------------------------------------------------
# Rotar humanoide alrededor del eje Z
# R_nueva = R_z(θ + Δθ)
# ---------------------------------------------------------------
def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])


# ---------------------------------------------------------------
# Instrucciones
# ---------------------------------------------------------------
print("=== Control de teclado ===")
print("↑ / ↓  → Adelante / Atrás")
print("← / →  → Izquierda / Derecha")
print("Q / E  → Rotar antihorario / horario")
print("La botella sigue la mano derecha automáticamente.")
print("==========================")


# ---------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------
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

    # -----------------------------------------------------------
    # Actualizar posición de la botella en cada paso de tiempo.
    # Garantiza que la botella permanezca en la mano derecha
    # independientemente del movimiento del humanoide.
    # -----------------------------------------------------------
    if nodo_peaton is not None and nodo_botella is not None:
        pos_mano = calcular_posicion_mano(nodo_peaton)
        nodo_botella.getField("translation").setSFVec3f(pos_mano)
        # Rotar la botella para que quede como si la mano la sostuviera
        # Rotación: eje X, 90 grados (pi/2) para ponerla horizontal
        nodo_botella.getField("rotation").setSFRotation([-0.5, 0.2, 0, math.pi / 2])
        nodo_botella.resetPhysics()