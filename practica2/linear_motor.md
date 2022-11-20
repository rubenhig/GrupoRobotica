
# Motor Lineal

## Descripción general 

Un motor lineal es un motor eléctrico cuyo estator y rotor están distribuidos de tal forma que produce una fuerza lineal en vez de torque o fuerza rotacional. Suelen emplearse en aplicaciones de alta precisión ya que permiten eliminar mecanismos de transmision como poleas, engranajes o acoplamientos que introducen imprecisión.

Se pueden distinguir dos categorías, motores de alta aceleración y motores de baja aceleración. Los motores de alta aceleración suelen ser cortos y están diseñados para acelerar objetos a muy altas velocidades. Este tipo se motores se están empleando para desarrollar cañones electromagnéticos por ejemplo. Los motores de baja aceleración se usan en los trenes de levitación magnética (maglev).

En Webots existe el nodo *LinearMotor* que es un derivado del nodo abstracto *Motor*. Los motores lineales en Webots pueden usarse como mecanismo de propulsión para un nodo *SliderJoint* o para un nodo *Track*.  El nodo *LinearMotor* tiene *maxForce* como único parámetro especifico y establece un límite superior, así como el valor por defecto de *available force*. Los demás parámetros son heredados del nodo abstracto *Motor*. Estos parámetros heredados son:

* **Acceleration [m/s²] :** aceleración por defecto del controlador P. Para que la aceleración no este limitada por el controlador P, asignar el valor -1 (infinito).
* **consumtionFactor :** Define la cantidad de energía que consume el motor.
* **controlPID [P, I, D] :** Define los parámetros P (ganancia proporcional), I (ganancia integral) y D (ganancia derivativa) del controlador PID del motor.
* **minPosition y maxPosition :** Define los “soft limits” de la posición del motor. Un “soft limit” permite establecer un limite software de tal manera que el controlador PID no intentara hacer movimientos pasado ese límite. Sin embargo, no evitan que una fuerza externa pueda hacer que el motor sobrepase los límites establecidos.
* **maxVelocity [m/s] :** Establece un límite superior, así como el valor por defecto de la velocidad del motor.
* **Multiplier :** Cuando el controlador llama a las funciones que controlan la posición, velocidad o fuerza, los parámetros de estas funciones son multiplicados por “multiplier”.
* **Sound :** Url que contiene el sonido que producirá el motor.
* **muscles :** define uno o más nodos muscle que muestran gráficamente la contracción de un musculo artificial.

---
## Real vs Webots

Los motores lineales reales pueden ser ironcore, ironless, tubulares y piezoelectricos entre otros. Además, dentro de cada tipo, existen motores de características, limites y desventajas muy variadas.

En Webots los motores lineales son completamente configurables en cuanto a prestaciones, tamaño y funcionamiento y cuentan con menos o ninguna restricción. 

---

##  Forma de uso

Los motores lineales en Webots pueden usarse como mecanismo de propulsión para un nodo SliderJoint o para un nodo Track. El nodo SliderJoint puede usarse para modelar una articulación que solo permite movimientos de translación en un determinado eje. A su vez el nodo Track puede usarse para modelar cintas transportadoras o vehículos oruga.

Los motores suelen usarse dentro de un nodo Robot y controlarse mediante el controlador de este.

**Pasos para usar un motor lineal como método de propulsión de un nodo SliderJoint:**
>1. Crear un nodo Robot.
>2. Añadir un nodo SliderJoint en children. Los nodos SliderJoint tienen tres componentes: jointParameter, devide y endPoint.
>3. Añadir un nodo JointParameters en jointParameters.
>4. Añadir un nodo LinearMotor en device.
>5. Añadir un nodo Solid en endPoint.
>6. Dentro del nodo Solid añadir un nodo Shape en children para darle la forma deseada.
>7. Crear y añadir un controlador.


**Pasos para usar un motor lineal como método de propulsión de un nodo Track:**
>1. Crear un nodo Robot
>2. Añadir un nodo Track en children.
>3. Añadir un nodo Shape en children y seleccionar la forma deseada.
>4. Añadir un nodo LinearMotor en device
>5. Reusar el Shape creado anterior mente como boundingObject
>6. Añadir un nodo Physics a physics.
>7. Crear y añadir un controlador.



Independientemente de el dispositivo que propulse, el motor tiene tres **modos de control:**

##### Control por posición
Es la manera estándar de controlar un Motor. El usuario especifica la posición deseada y el controlador PID, teniendo en cuenta la aceleración , velocidad y fuerza establecidas en los parametros Acceleration, maxVelocity y maxForce, se encarga de conseguir la posición deseada.

Para usar el control por posición hay que llamar a la función wb_motor_set_position de la siguiente manera:

    #include <webots/motor.h>
    wb_motor_set_position(tagMotor, position);      //position --> m
##### Control por velocidad

En el modo de control por velocidad, cuando el usuario selecciona la velocidad deseada, el motor iniciará un movimiento continuo la velocidad establecida teniendo en cuenta la aceleración y fuerza establecidas.

Para usar el control por velocidad hay que llamar a la funciones wb_motor_set_position y wb_motor_set_velocity de la siguiente manera:

    wb_motor_set_position(tagMotor, INFINITY);
    wb_motor_set_velocity(tagMmotor, velocidad);     // velocidad --> m/s
##### Control por fuerza
En este último modo de control, el usuario elige directamente la fuerza que quiere que el motor aplique. La fuerza se aplica de manera continua por lo que el motor acelerara infinitamente si no se controla.

Para usar el control por fuerza hay que llamar a la función wb_motor_set_force de la siguiente manera:

    wb_motor_set_force(tagMotor, fuerza);           // fuerza --> m/s²  