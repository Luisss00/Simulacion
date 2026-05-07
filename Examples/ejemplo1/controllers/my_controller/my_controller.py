from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# --- Parámetros de movimiento (constantes) ---
PASO = 0.05
ANGULO_STEP = math.pi / 36

# --- Desplazamiento local de la botella_en_mano respecto al peatón (mano derecha) ---
desp_x = 0.0   # adelante
desp_y = -0.25   # lateral
desp_z = -0.7  # altura

# --- Nodos del mundo ---
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella_en_mano = supervisor.getFromDef("botella_en_mano")

if nodo_peaton is None:
    print("ERROR: No se encontró el peatón 'pedestrian1'")
if nodo_botella_en_mano is None:
    print("ERROR: No se encontró el botella_en_mano")

# --- Teclado ---
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def trasladar(nodo, dx_local, dy_local):
    """Convierte desplazamiento local a mundial y mueve el nodo."""
    pos = nodo.getField("translation").getSFVec3f()
    angulo = nodo.getField("rotation").getSFRotation()[3]
    cos_a = math.cos(angulo)
    sin_a = math.sin(angulo)
    dx_mundo = dx_local * cos_a - dy_local * sin_a
    dy_mundo = dx_local * sin_a + dy_local * cos_a
    nueva_pos = [pos[0] + dx_mundo, pos[1] + dy_mundo, pos[2]]
    nodo.getField("translation").setSFVec3f(nueva_pos)

def rotar_eje_z(nodo, delta):
    """Rota el nodo en su eje Z el ángulo dado (radianes)."""
    campo = nodo.getField("rotation")
    x, y, z, angulo = campo.getSFRotation()
    campo.setSFRotation([x, y, z, angulo + delta])

# ---------- Instrucciones ----------
print("=== Control de teclado ===")
print("↑ / ↓  → Adelante / atrás")
print("← / →  → Izquierda / derecha")
print("Q / E  → Rotar")
print("==========================")

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()
    if nodo_peaton and tecla != -1:
        if tecla == Keyboard.UP:
            trasladar(nodo_peaton, PASO, 0)
        elif tecla == Keyboard.DOWN:
            trasladar(nodo_peaton, -PASO, 0)
        elif tecla == Keyboard.LEFT:
            trasladar(nodo_peaton, 0, PASO)
        elif tecla == Keyboard.RIGHT:
            trasladar(nodo_peaton, 0, -PASO)
        elif tecla == ord('Q'):
            rotar_eje_z(nodo_peaton, ANGULO_STEP)
        elif tecla == ord('E'):
            rotar_eje_z(nodo_peaton, -ANGULO_STEP)

    # --- Acoplar el balón al peatón (misma orientación) ---
    if nodo_peaton and nodo_botella_en_mano:
        pos_peaton = nodo_peaton.getField("translation").getSFVec3f()
        angulo = nodo_peaton.getField("rotation").getSFRotation()[3]
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        dx_mundo = desp_x * cos_a - desp_y * sin_a
        dy_mundo = desp_x * sin_a + desp_y * cos_a
        pos_botella_en_mano = [
            pos_peaton[0] + dx_mundo,
            pos_peaton[1] + dy_mundo,
            pos_peaton[2] + desp_z
        ]
        nodo_botella_en_mano.getField("translation").setSFVec3f(pos_botella_en_mano)
        nodo_botella_en_mano.getField("rotation").setSFRotation([0, 0, 1, angulo])