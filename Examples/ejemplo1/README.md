# Parcial 2 - Simulación y Robótica

**Estudiante:** Andres Charry Lopez 
**Materia:** Simulación y Robótica  
**Institución:** UNICARIBE
**Fecha:** 7 de mayo de 2026

---

## 1. Descripción del Proyecto
Este repositorio contiene la solución técnica al segundo parcial. Se desarrolló un controlador en **Webots** para un robot humanoide que permite el desplazamiento mediante teclado y la gestión de un objeto (botella) mediante **transformaciones solidarias**.

## 2. Fundamentación Matemática (Álgebra Lineal)
El núcleo del proyecto es el uso de matrices para garantizar que la botella siga el movimiento del robot sin desfases, incluso durante la rotación.

### Vector de Posición Relativa (Offset)
Se definió un vector local $\vec{d}_{local}$ que representa la ubicación de la mano derecha respecto al origen del robot:
$$\vec{d}_{local} = \begin{bmatrix} 0.2 \\ -0.20 \\ -0.50 \end{bmatrix}$$

### Matriz de Rotación ($R_z$)
Para que la botella orbite correctamente cuando el robot gira, se aplica una matriz de rotación sobre el eje vertical (Z):
$$R_z(\theta) = \begin{bmatrix} \cos(\theta) & -\sin(\theta) & 0 \\ \sin(\theta) & \cos(\theta) & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

### Ecuación de Transformación
La posición mundial de la botella se recalcula en cada frame usando la fórmula:
$$P_{botella}^{global} = P_{robot}^{global} + (R_z(\theta) \cdot \vec{d}_{local})$$

---

## 3. Instrucciones de Control
La simulación se controla en tiempo real con el teclado:
* **Flechas Direccionales:** Traslación en los ejes X e Y locales.
* **Teclas Q / E:** Rotación horaria y antihoraria (Eje Z).
* **Inclinación:** La botella cuenta con un ajuste de inclinación en el eje X para un agarre más realista.

## 4. Requisitos
* **Software:** Webots R2025a.
* **Lenguaje:** Python 3.12. en adelante
* **Librerías:** `controller`, `sympy`, `math`.

---
*Este proyecto es parte de la evaluación correspondiente al corte 2.*