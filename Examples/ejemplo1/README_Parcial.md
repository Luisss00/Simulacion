# Paso a paso segundo parcial

## 1. Agregar el nodo BeerBottle en Webots

Primero se abrió el proyecto t1 en Webots. Luego se agregó el nodo BeerBottle
buscándolo en la ruta: `nodos > webots projects > objects > drinks > BeerBottle.

En el campo DEF se le asignó el nombre BOTELLA.



## 2. Modificar el archivo .wbt

Para evitar que la física de Webots moviera la botella libremente por la escena,
se modificó el nodo en el archivo t1.wbt desde Visual Studio Code.

Se agregó el EXTERNPROTO para que Webots pudiera cargar el modelo:

EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/drinks/protos/BeerBottle.proto"

Y se definió el nodo con locked TRUE para desactivar la física:


DEF BOTELLA BeerBottle {
  translation 0 0 1.0
  rotation 0 0 1 0
  locked TRUE
}


El campo locked TRUE le indica a Webots que el supervisor tendrá control
total sobre la posición del objeto, impidiendo que la gravedad lo afecte.

---

## 3. Modificaciones al controlador Python

### 3.1 Obtener el nodo de la botella

Se obtuvo el nodo BOTELLA desde el archivo .wbt usando su DEF,
siguiendo el mismo patrón con el que se obtiene el nodo del humanoide:


nodo_botella = supervisor.getFromDef("BOTELLA")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo BOTELLA")


Es importante que el nombre en getFromDef() coincida exactamente con
el DEF definido en el .wbt, incluyendo mayúsculas y minúsculas.

---

### 3.2 Función seguir_mano_derecha()

Para lograr que la botella siga siempre la mano derecha del humanoide,
se reutilizó la misma lógica matemática de la función trasladar() que
ya existía en el código base.

El principio matemático es el mismo:
P_botella = P_humano + R_z(θ) * d_mano_local

Donde:
- P_humano es la posición actual del humanoide en el mundo
- R_z(θ) es la matriz de rotación alrededor del eje Z con el ángulo actual del humanoide
- d_mano_local es un vector fijo que representa la posición de la mano derecha en el sistema local del humanoide

La matriz de rotación R_z(θ) es la misma que se usa en trasladar():
R_z(θ) = | cos θ  -sin θ  0 |
| sin θ   cos θ  0 |
|   0       0    1 |

**Diferencias con trasladar():**

| | trasladar() | seguir_mano_derecha() |
|---|---|---|
| Desplazamiento | Viene del teclado | Es un valor fijo (mano derecha) |
| Nodo que se mueve | El humano | La botella |
| Se llama cuando | Hay tecla presionada | Siempre, en cada paso |

Los valores del offset de la mano derecha que se pueden ajustar son:


dx_local = 0.3   # distancia lateral derecha (aumentar = más a la derecha)
dy_local = 0.0   # distancia adelante/atrás  (aumentar = más adelante)
dz       = 0.0   # altura de la mano         (aumentar = más arriba)


Además se agregó resetPhysics() al final de la función para cancelar
cualquier velocidad acumulada por la gravedad en cada paso de simulación,
manteniendo la botella estática en la mano:


nodo_botella.resetPhysics()


---

### 3.3 Llamada en el bucle principal

Se agregó la llamada a seguir_mano_derecha() **fuera del if** del teclado,
para que se ejecute en cada paso sin importar si el humano se mueve o no.
Esto garantiza que la botella nunca caiga ni se desplace de la mano:


    # La botella SIEMPRE sigue la mano derecha
      seguir_mano_derecha()


Si se pusiera dentro del if, la botella solo se actualizaría cuando
se presiona una tecla y la gravedad la jalaria hacia abajo en los pasos
donde no hay movimiento.