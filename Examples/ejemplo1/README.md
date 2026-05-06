\# Simulación Webots — Parcial Segundo Corte



\## Autor

Juan Rojano



\## Modificaciones realizadas



\### 1. Nodo BeerBottle agregado a la escena

Se agregó un nodo de tipo BeerBottle al árbol de escena del mundo t1.wbt,

proveniente de la librería estándar de Webots en projects/objects/drinks/protos.

Se le asignó el DEF: BEER\_BOTTLE para poder referenciarlo desde el controlador.



\### 2. Posición inicial de la botella

La botella fue posicionada manualmente cerca de la mano derecha del humanoide

ajustando el campo translation del nodo BeerBottle en el editor de Webots.



\### 3. Modificación del controlador

Se modificó my\_controller.py para que la botella permanezca siempre en la

mano derecha del humanoide independientemente de su movimiento.



Mecanismo matemático utilizado:

\- Se obtiene la posición del humanoide con getField("translation").getSFVec3f()

\- Se obtiene su ángulo de rotación con getField("rotation").getSFRotation()

\- Se construye la matriz de rotación R\_z(θ):



&#x20; R\_z(θ) = | cos θ  -sin θ  0 |

&#x20;           | sin θ   cos θ  0 |

&#x20;           |   0       0    1 |



\- Se define un offset fijo en el sistema LOCAL del humanoide que representa

&#x20; la posición de la mano derecha relativa al cuerpo.

\- Se transforma al sistema GLOBAL: offset\_global = R\_z \* offset\_local

\- La posición final es: P\_botella = P\_humanoide + offset\_global

\- Se llama resetPhysics() para anular la gravedad en cada frame.



Esta transformación garantiza que la botella siga tanto la posición

como la rotación del humanoide en todo momento.

