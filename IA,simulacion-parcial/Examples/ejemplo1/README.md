"# tarea_robotica" 
Para lograr que la botella se moviera junto con el personaje, se hicieron algunos cambios al controlador original. Antes, el programa solo se encargaba de mover al peatón con el teclado. La botella, en cambio, era un objeto estático, es decir, no reaccionaba a nada.

Lo primero que se hizo fue permitir que el programa “reconozca” la botella dentro del entorno de Webots robotics simulator. Para eso, se obtuvo una referencia al objeto usando su identificador (DEF beerbottle). Esto es como decirle al programa: “además del peatón , también quiero que tengas en cuenta este objeto”.

Después, en cada ciclo de la simulación (que ocurre muchas veces por segundo), se añadió un bloque de código que actualiza la posición de la botella. La idea es simple: si el peatón se mueve, la botella debe moverse con él.

Para lograrlo, el programa primero obtiene la posición actual del peatón. Luego, en lugar de colocar la botella exactamente en ese mismo punto (lo cual haría que se superpongan), se le suma una pequeña diferencia llamada offset. Ese offset representa la distancia entre el cuerpo del peatón y su mano, donde estaría la botella.

Además, no solo se copió la posición, sino también la rotación. Esto significa que cuando el peatón gira, la botella gira con él, manteniendo la ilusión de que la está sosteniendo.