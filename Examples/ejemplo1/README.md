# Parcial Segundo Corte - Simulación Webots

## ¿Qué se hizo?

Se partió del código base que controlaba un humanoide en Webots mediante
teclado. El objetivo fue agregar una botella de cerveza (BeerBottle) que
permanezca siempre en la mano derecha del humanoide, independientemente
de su movimiento o rotación.

---

## Cambios en el archivo t1.wbt

Se registró el modelo de la botella agregando su EXTERNPROTO al inicio
del archivo, junto a los demás prototipos:

EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/objects/drinks/protos/BeerBottle.proto"


Se definió el nodo con DEF BOTTLE y locked TRUE para que el supervisor
tenga control total sobre su posición y la física no la desplace:

DEF BOTTLE BeerBottle {
  translation 0 0 1.0
  rotation 0 0 1 0
  locked TRUE
}



## Cambios en el controlador Python

### 1. Obtener el nodo de la botella

Se agregó la obtención del nodo botle desde el .wbt usando su DEF,
siguiendo el mismo patrón con el que ya se obtenía el nodo del humanoide:

python
nodo_botella = supervisor.getFromDef("botle")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo BOTTLE")




### 2. Función matriz_rotacion()

Se extrajo la matriz R_z(θ) como función independiente y reutilizable.
En el código original esta matriz se repetía dentro de cada función.
Ahora se centraliza en un solo lugar para evitar duplicación:


def matriz_rotacion(angulo):
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




### 3. Constantes del offset de la mano derecha

Se definieron como constantes globales los valores del offset de la mano
derecha en el sistema local del humanoide, para facilitar su ajuste:


OFFSET_X = 0.0   # sin desplazamiento adelante/atrás
OFFSET_Y = -0.2  # hacia la derecha del humano
OFFSET_Z = -0.5  # altura de la mano




### 4. Función anclar_botella()

Es la función principal nueva. Calcula la posición mundial de la mano
derecha del humano y posiciona la botella allí en cada paso.

Reutiliza el mismo principio matemático de trasladar() que ya existía
en el código base:
P_botella = P_humano + R_z(θ) * d_local

Donde d_local es el vector fijo [OFFSET_X, OFFSET_Y, 0] que representa
la posición de la mano derecha en el sistema local del humanoide.

La diferencia con trasladar() es que aquí el desplazamiento no viene
del teclado sino que es constante, y el resultado se aplica al nodo de
la botella en lugar del humano.

Al final se llama resetPhysics() para cancelar velocidades acumuladas
por la gravedad en cada paso:


def anclar_botella():
    if nodo_peaton is None or nodo_botella is None:
        return

    pos = nodo_peaton.getField("translation").getSFVec3f()
    P_humano = Matrix([pos[0], pos[1], pos[2]])

    _, _, _, angulo = nodo_peaton.getField("rotation").getSFRotation()
    Rz = matriz_rotacion(angulo)

    d_local   = Matrix([OFFSET_X, OFFSET_Y, 0])
    P_botella = P_humano + Rz * d_local

    nodo_botella.getField("translation").setSFVec3f([
        float(P_botella[0]),
        float(P_botella[1]),
        float(pos[2] + OFFSET_Z)
    ])
    nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])
    nodo_botella.resetPhysics()




### 5. Llamada en el bucle principal

Se llama anclar_botella() fuera del if del teclado para que se ejecute
en **cada paso** sin importar si el humano se mueve o no:


    # NUEVO: la botella SIEMPRE sigue la mano derecha
    anclar_botella()


Si estuviera dentro del if, la gravedad jalaría la botella hacia abajo
en los pasos donde no se presiona ninguna tecla.



## Concepto matemático clave

El cambio de sistema de referencia es el mismo que usa trasladar() para
desplazar al humano. La diferencia es que aquí el vector d_local es
fijo y representa un punto anatómico del humanoide (su mano derecha),
mientras que en trasladar() el vector viene del teclado.

Esto garantiza que sin importar hacia dónde rote o se traslade el humano,
la botella siempre calcula su posición mundial correctamente aplicando
la rotación actual del humanoide al offset local.