from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener el nodo del humanoide
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF del humanoide")

# NUEVO: Obtener el nodo de la botella
nodo_botella = supervisor.getFromDef("botle")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo BOTTLE")

# Parámetros de movimiento
TAMANO_PASO = 0.05          # metros por paso
PASO_ANGULO = math.pi / 36  # 5 grados por paso

# NUEVO: Offset de la mano derecha en sistema local del humano
OFFSET_X = 0.0
OFFSET_Y = -0.2
OFFSET_Z = -0.5

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------------------------------------------------------------
# Desplazamiento en X o Y del sistema de referencia del humanoide
# ---------------------------------------------------------------
def trasladar(nodo, dx_local, dy_local):
    """
    P_nueva = P_vieja + R_z(θ) * d_local

    R_z(θ) = | cos θ  -sin θ  0 |   d_local = | dx_local |
              | sin θ   cos θ  0 |              | dy_local |
              |   0       0    1 |              |    0     |
    """
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

# ---------------------------------------------------------------
# Rotación alrededor de Z (horario / antihorario)
# ---------------------------------------------------------------
def rotar_z(nodo, delta_angulo):
    """
    R_nueva = R_z(Δθ) * R_z(θ) = R_z(θ + Δθ)
    """
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])

# NUEVO: Construye la matriz de rotación R_z(θ)
def calcular_Rz(angulo):
    """
    R_z(θ) = | cos θ  -sin θ  0 |
             | sin θ   cos θ  0 |
             |   0       0    1 |
    """
    return Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])

# NUEVO: Ancla la botella a la mano derecha del humano
def anclar_botella():
    """
    Calcula la posición mundial de la mano derecha y posiciona
    la botella allí en cada paso usando cambio de sistema de referencia:

        P_botella = P_humano + R_z(θ) * d_local

    donde d_local = [OFFSET_X, OFFSET_Y, 0] es el offset fijo
    de la mano derecha en el sistema local del humanoide.
    """
    if nodo_peaton is None or nodo_botella is None:
        return

    pos = nodo_peaton.getField("translation").getSFVec3f()
    P_humano = Matrix([pos[0], pos[1], pos[2]])

    _, _, _, angulo = nodo_peaton.getField("rotation").getSFRotation()
    Rz = calcular_Rz(angulo)

    d_local   = Matrix([OFFSET_X, OFFSET_Y, 0])
    P_botella = P_humano + Rz * d_local

    nodo_botella.getField("translation").setSFVec3f([
        float(P_botella[0]),
        float(P_botella[1]),
        float(pos[2] + OFFSET_Z)
    ])
    nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])
    nodo_botella.resetPhysics()

# ---------------------------------------------------------------
print("=== Control de teclado ===")
print("↑ / ↓  → Mover adelante / atrás    (eje X local)")
print("← / →  → Mover izquierda / derecha (eje Y local)")
print("Q / E  → Rotar antihorario / horario (alrededor de Z)")
print("==========================")

# ---------------------------------------------------------------
# Bucle principal - Tiempo - Simulación
# ---------------------------------------------------------------
while supervisor.step(paso_tiempo) != -1:

    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:

        # --- Traslación en eje X del humanoide (adelante / atrás) ---
        if tecla == Keyboard.UP:
            print("Adelante")
            trasladar(nodo_peaton, TAMANO_PASO, 0.0)

        elif tecla == Keyboard.DOWN:
            print("Atras")
            trasladar(nodo_peaton, -TAMANO_PASO, 0.0)

        # --- Traslación en eje Y del humanoide (izquierda / derecha) ---
        elif tecla == Keyboard.LEFT:
            print("Izquierda")
            trasladar(nodo_peaton, 0.0, TAMANO_PASO)

        elif tecla == Keyboard.RIGHT:
            print("Derecha")
            trasladar(nodo_peaton, 0.0, -TAMANO_PASO)

        # --- Rotación alrededor de Z ---
        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)

        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)

    # NUEVO: la botella SIEMPRE sigue la mano derecha
    anclar_botella()