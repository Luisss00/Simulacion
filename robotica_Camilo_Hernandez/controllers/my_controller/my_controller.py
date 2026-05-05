"""
Supervisor principal:
- Controla el movimiento de un peatón con el teclado.
- Un dron sigue una trayectoria circular alrededor del peatón.
"""

from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

# =========================================================
# 1. CREACIÓN DEL SUPERVISOR
# =========================================================
simulador = Supervisor()
TIME_STEP = int(simulador.getBasicTimeStep())

# =========================================================
# 2. OBTENER NODOS DEL MUNDO
# =========================================================
persona = simulador.getFromDef("pedestrian1")
uav = simulador.getFromDef("dron")

if persona is None:
    print("No existe el nodo DEF 'pedestrian1'")

if uav is None:
    print("No existe el nodo DEF 'dron'")

# =========================================================
# 3. CONFIGURACIÓN GENERAL
# =========================================================

# ----- Parámetros del dron -----
ALTURA_PERSONA = 1.8
DISTANCIA_ORBITA = 0.5
RAPIDEZ_GIRO = 2.2
AJUSTE_ALTURA = -1.3

# ----- Parámetros de movimiento -----
VELOCIDAD = 0.05
GIRO = math.pi / 36

# =========================================================
# 4. CONFIGURAR TECLADO
# =========================================================
keyboard = simulador.getKeyboard()
keyboard.enable(TIME_STEP)

# =========================================================
# 5. FUNCIONES AUXILIARES
# =========================================================
def mover_localmente(objeto, avance_x, avance_y):
    """
    Desplaza el objeto según sus ejes locales.
    """

    field_pos = objeto.getField("translation")
    posicion = field_pos.getSFVec3f()

    x_actual = posicion[0]
    y_actual = posicion[1]
    z_actual = posicion[2]

    field_rot = objeto.getField("rotation")
    _, _, _, angulo = field_rot.getSFRotation()

    matriz_rotacion = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [0, 0, 1]
    ])

    movimiento_local = Matrix([avance_x, avance_y, 0])

    movimiento_global = matriz_rotacion * movimiento_local

    nueva_posicion = Matrix([
        x_actual,
        y_actual,
        z_actual
    ]) + movimiento_global

    field_pos.setSFVec3f([
        float(nueva_posicion[0]),
        float(nueva_posicion[1]),
        float(nueva_posicion[2])
    ])


def girar(objeto, cambio):
    """
    Aplica una rotación sobre el eje Z.
    """

    rotacion = objeto.getField("rotation")

    eje_x, eje_y, eje_z, angulo_actual = rotacion.getSFRotation()

    nuevo_angulo = angulo_actual + cambio

    rotacion.setSFRotation([eje_x, eje_y, eje_z, nuevo_angulo])


# =========================================================
# 6. CONTROL DEL DRON
# =========================================================
def mover_dron(tiempo):
    """
    Hace que el dron orbite alrededor del peatón.
    """

    if persona is None or uav is None:
        return

    posicion_persona = persona.getField("translation").getSFVec3f()

    px = posicion_persona[0]
    py = posicion_persona[1]
    pz = posicion_persona[2]

    centro_z = pz + ALTURA_PERSONA

    angulo = RAPIDEZ_GIRO * tiempo

    offset_x = DISTANCIA_ORBITA * math.cos(angulo)
    offset_y = DISTANCIA_ORBITA * math.sin(angulo)

    posicion_dron = [
        px + offset_x,
        py + offset_y,
        centro_z + AJUSTE_ALTURA
    ]

    uav.getField("translation").setSFVec3f(posicion_dron)

# =========================================================
# 7. MENSAJES EN CONSOLA
# =========================================================
print("=" * 45)
print("CONTROLES DISPONIBLES")
print("Flechas: mover peatón")
print("Q / E : rotar peatón")
print("=" * 45)
print("El dron se mueve automáticamente alrededor del peatón.")

# =========================================================
# 8. BUCLE PRINCIPAL
# =========================================================
while simulador.step(TIME_STEP) != -1:

    tecla = keyboard.getKey()

    if persona is not None and tecla != -1:

        if tecla == Keyboard.UP:
            mover_localmente(persona, VELOCIDAD, 0)

        elif tecla == Keyboard.DOWN:
            mover_localmente(persona, -VELOCIDAD, 0)

        elif tecla == Keyboard.LEFT:
            mover_localmente(persona, 0, VELOCIDAD)

        elif tecla == Keyboard.RIGHT:
            mover_localmente(persona, 0, -VELOCIDAD)

        elif tecla == ord('Q'):
            girar(persona, GIRO)

        elif tecla == ord('E'):
            girar(persona, -GIRO)

    # Movimiento automático del dron
    mover_dron(simulador.getTime())