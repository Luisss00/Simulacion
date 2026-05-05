from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# ---------- Obtener nodos ----------
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF 'pedestrian1'")

# Nodo botella
nodo_botella = supervisor.getFromDef("botella")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo de la botella")

# =======================================================
# POSICIÓN RELATIVA DE LA BOTELLA (MANO DERECHA)
# =======================================================
offset_x = -0.03
offset_y = 0.2
offset_z = -0.45

# ---------- Parámetros del peatón ----------
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# ---------- Activar teclado ----------
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# =======================================================
# FUNCIÓN DE TRASLACIÓN
# =======================================================
def trasladar(nodo, dx_local, dy_local):

    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()

    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    # Matriz de rotación
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [0, 0, 1]
    ])

    # Movimiento local
    d_local = Matrix([dx_local, dy_local, 0])

    # Convertir a coordenadas globales
    d_mundial = R_z * d_local

    # Nueva posición
    P_nueva = P_vieja + d_mundial

    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

# =======================================================
# FUNCIÓN DE ROTACIÓN
# =======================================================
def rotar_z(nodo, delta_angulo):

    campo_rotacion = nodo.getField("rotation")

    _, _, _, angulo_actual = campo_rotacion.getSFRotation()

    campo_rotacion.setSFRotation([
        0,
        0,
        1,
        angulo_actual + delta_angulo
    ])

# ---------- Instrucciones ----------
print("=== Control de teclado ===")
print("↑ / ↓  → Adelante / atrás")
print("← / →  → Izquierda / derecha")
print("Q / E  → Rotar")
print("==========================")
print("La botella permanece en la mano derecha")

# =======================================================
# BUCLE PRINCIPAL
# =======================================================
while supervisor.step(paso_tiempo) != -1:

    # ---------- Movimiento del humanoide ----------
    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:

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

    # ===================================================
    # BOTELLA PEGADA A LA MANO DERECHA
    # ===================================================
    if nodo_peaton is not None and nodo_botella is not None:

        pos = nodo_peaton.getField("translation").getSFVec3f()

        rot = nodo_peaton.getField("rotation").getSFRotation()

        angulo = rot[3]

        # Matriz de rotación
        R_z = Matrix([
            [cos(angulo), -sin(angulo), 0],
            [sin(angulo),  cos(angulo), 0],
            [0, 0, 1]
        ])

        # Offset relativo de la mano derecha
        offset_local = Matrix([
            offset_x,
            offset_y,
            offset_z
        ])

        # Transformación local → global
        offset_mundial = R_z * offset_local

        # Posición final de la botella
        pos_botella = [
            float(pos[0] + offset_mundial[0]),
            float(pos[1] + offset_mundial[1]),
            float(pos[2] + offset_mundial[2])
        ]

        # Actualizar botella
        nodo_botella.getField("translation").setSFVec3f(pos_botella)

        # Rotar botella junto al humanoide
        nodo_botella.getField("rotation").setSFRotation([
    1,
    0,
    0,
    1.57   # inclinación de lado (~90 grados)
])