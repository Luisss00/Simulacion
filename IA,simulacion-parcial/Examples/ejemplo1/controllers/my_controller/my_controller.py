from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# ---------- Obtener nodos ----------
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF 'pedestrian1'")

nodo_dron = supervisor.getFromDef("drone_mosca")
if nodo_dron is None:
    print("ERROR: No se encontró el nodo con DEF del dron")

# NUEVO: botella
nodo_botella = supervisor.getFromDef("beerbottle")
if nodo_botella is None:
    print("ERROR: No se encontró la botella (DEF 'beerbottle')")

# =======================================================
#   PARÁMETROS DEL DRON
# =======================================================
altura_cabeza_peaton = 1.8
radio_orbita = 0.2
velocidad_orbita = 2.0
altura_extra_sobre_cabeza = -1.3
velocidad_giro_dron = 2.5

# ---------- Parámetros del peatón ----------
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# NUEVO: offset de la botella
offset_local = [0.0439, -0.276, -0.39]  # adelante, lado, altura

# ---------- Activar teclado ----------
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------- Funciones para mover al peatón ----------
def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()

    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    # Conversión de coordenadas locales a globales (rotación en Z)
    dx_mundo = dx_local * math.cos(angulo) - dy_local * math.sin(angulo)
    dy_mundo = dx_local * math.sin(angulo) + dy_local * math.cos(angulo)

    nueva_pos = [
        pos[0] + dx_mundo,
        pos[1] + dy_mundo,
        pos[2]
    ]

    campo_traslacion.setSFVec3f(nueva_pos)


def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    x, y, z, angulo_actual = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([x, y, z, angulo_actual + delta_angulo])

# ---------- Instrucciones ----------
print("=== Control de teclado ===")
print("↑ / ↓  → Mover adelante / atrás")
print("← / →  → Mover izquierda / derecha")
print("Q / E  → Rotar")
print("==========================")
print("Dron orbitando y girando sobre sí mismo")

# ---------- Bucle principal ----------
while supervisor.step(paso_tiempo) != -1:

    # 1. Control del peatón
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

    # =======================================================
    # NUEVO: Movimiento de la botella
    # =======================================================
    if nodo_peaton is not None and nodo_botella is not None:

        # Posición del peatón
        campo_pos = nodo_peaton.getField("translation")
        px, py, pz = campo_pos.getSFVec3f()

        # Rotación del peatón
        campo_rot = nodo_peaton.getField("rotation")
        rx, ry, rz, angulo = campo_rot.getSFRotation()

        # Convertir offset local → mundo
        dx = offset_local[0] * math.cos(angulo) - offset_local[1] * math.sin(angulo)
        dy = offset_local[0] * math.sin(angulo) + offset_local[1] * math.cos(angulo)
        dz = offset_local[2]

        nueva_pos_botella = [
            px + dx,
            py + dy,
            pz + dz
        ]

        nodo_botella.getField("translation").setSFVec3f(nueva_pos_botella)

        # Copiar rotación
        nodo_botella.getField("rotation").setSFRotation([rx, ry, rz, angulo])

    # =======================================================
    # 2. Movimiento del dron
    # =======================================================
    if nodo_peaton is not None and nodo_dron is not None:

        pos_peaton = nodo_peaton.getField("translation").getSFVec3f()
        px, py, pz = pos_peaton

        # Centro de la órbita (cabeza del peatón)
        centro_x = px
        centro_y = py
        centro_z = pz + altura_cabeza_peaton

        t = supervisor.getTime()

        # Movimiento circular
        dx = radio_orbita * math.cos(velocidad_orbita * t)
        dy = radio_orbita * math.sin(velocidad_orbita * t)

        pos_dron = [
            centro_x + dx,
            centro_y + dy,
            centro_z + altura_extra_sobre_cabeza
        ]

        nodo_dron.getField("translation").setSFVec3f(pos_dron)

        # Rotación sobre su propio eje
        angulo = velocidad_giro_dron * t
        nodo_dron.getField("rotation").setSFRotation([0, 0, 1, angulo])