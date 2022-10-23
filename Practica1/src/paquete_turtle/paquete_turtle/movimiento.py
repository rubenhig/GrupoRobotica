#!/usr/bin/env python3
import keyboard
from numpy import float32, uint8
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
from turtlesim.srv import SetPen, TeleportRelative, TeleportAbsolute
import math


class EmisorMovimiento(Node): 
    #variables para el servicio pen:
    estadoPen = uint8
    r = 170
    g = 170
    b = 170
    width = 3

    # variables para el servicio reset:
    x = 5.544444561004639
    y = 5.544444561004639
    theta = math.pi / 2



    def __init__(self):
        super().__init__('Movimiento')
        self.publisher_Radio = self.create_publisher(String, "radio", 10)               # Quitar---------------
        self.publisher_Pose = self.create_publisher(Twist, "/turtle1/cmd_vel", 100) 
        
        self.cliente_lapiz = self.create_client(SetPen, "turtle1/set_pen")
        self.request_lapiz = SetPen.Request()

        self.cliente_relativo = self.create_client(TeleportRelative, 'turtle1/teleport_relative')
        self.request_relativo = TeleportRelative.Request()

        self.cliente_absoluto = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.request_absoluto = TeleportAbsolute.Request()

        while not self.cliente_lapiz.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')
        
        while not self.cliente_relativo.wait_for_service(timeout_sec=1.0) and self.cliente_absoluto.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')


        self.get_logger().info("Emisor lanzado")

    
    def avanzar_linear(self, tamaño):
        self.request_relativo.linear = tamaño
        self.request_relativo.angular = 0.0

        self.futuro = self.cliente_relativo.call_async(self.request_relativo)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def avanzar_angular(self, angulo):
        self.request_relativo.angular = angulo
        self.request_relativo.linear = 0.0

        self.futuro = self.cliente_relativo.call_async(self.request_relativo)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def hacer_poligono(self, tamaño, num_lados):
        angulo = 360.0 / num_lados
        for i in range(num_lados):
            self.avanzar_linear(tamaño)
            self.avanzar_angular(math.radians(angulo))

    def hacer_poligonos(self):
        for i in range(3 ,11):
            self.hacer_poligono(i/5.0, i)
    
    def mover_absoluto(self, x, y):
        self.request_absoluto.x = x
        self.request_absoluto.y = y
        self.request_absoluto.theta = math.pi / 2

        self.futuro = self.cliente_absoluto.call_async(self.request_absoluto)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()



    def set_estado_lapiz(self, estado):

        self.estadoPen = estado
        self.request_lapiz.r = self.r
        self.request_lapiz.g = self.g
        self.request_lapiz.b = self.b
        self.request_lapiz.off = self.estadoPen
        self.request_lapiz.width = self.width

        self.futuro_lapiz = self.cliente_lapiz.call_async(self.request_lapiz)
        rclpy.spin_until_future_complete(self, self.futuro_lapiz)
        
        self.get_logger().info("termianado set_estado_lapiz: " + str(estado))
        return self.futuro_lapiz.result

    def peticion_reset(self):

        self.mover_absoluto(5.544444561004639, 5.544444561004639)
        
        self.get_logger().info("peticion de reset lanzada")


    


def main(args=None):
    try:
        rclpy.init(args=args)
        nodo_movimiento = EmisorMovimiento() 

        velocidad = 3.0
        tamaño = 2.0
        

        posicion = Twist()
        vector = Vector3()
 
        def on_press(key):
            nonlocal nodo_movimiento
            nodo_movimiento.get_logger().info("Funcion on_press <<<<<<<<<<<<<")
            
            nodo_movimiento.get_logger().info(str(key))

            msg = String()                                      # Quitar---------------
            msg.data = str(key)                                 # Quitar---------------
            nodo_movimiento.publisher_Radio.publish(msg)        # Quitar---------------

            if(type(key) == KeyCode and key.char == ('w')):
                nodo_movimiento.get_logger().info("dentro del if")
                
                vector.x = velocidad
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo_movimiento.publisher_Pose.publish(posicion)

            if(type(key) == KeyCode and key.char == ('s')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = -velocidad
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo_movimiento.publisher_Pose.publish(posicion)
            

            if(type(key) == KeyCode and key.char == ('a')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = velocidad
                posicion.angular = vector
                nodo_movimiento.publisher_Pose.publish(posicion)


            if(type(key) == KeyCode and key.char == ('d')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = -velocidad
                posicion.angular = vector
                nodo_movimiento.publisher_Pose.publish(posicion)

            
            
            if(type(key) == KeyCode and key.char == ('p')):
                nodo_movimiento.get_logger().info("dentro del if")

                
                posicion.linear.x = 2.0
                posicion.linear.y = 0.0
                posicion.linear.z = 0.0
                posicion.angular.x = 0.0
                posicion.angular.y = 0.0
                posicion.angular.z = 1.0
                nodo_movimiento.publisher_Pose.publish(posicion)


                
            



        def on_release(key):
            nonlocal nodo_movimiento
            nodo_movimiento.get_logger().info("Funcion on_release >>>>>>>>>>>")
            
            nodo_movimiento.get_logger().info(str(key))


            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.0
            posicion.linear = vector
            posicion.angular = vector
            nodo_movimiento.publisher_Pose.publish(posicion)


            #if(type(key) == Key and key == keyboard.Key.alt):
             #   nodo_movimiento.get_logger().info("dentro if alt")
              #  nodo_movimiento.hacer_cuadrado(3.0) 

            if(type(key) == KeyCode and key.char == ('1')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligonos()

            if(type(key) == KeyCode and key.char == ('3')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 3)

            if(type(key) == KeyCode and key.char == ('4')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 4)

            if(type(key) == KeyCode and key.char == ('5')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 5)
            
            if(type(key) == KeyCode and key.char == ('6')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 6)

            if(type(key) == KeyCode and key.char == ('7')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 7)
            
            if(type(key) == KeyCode and key.char == ('8')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 8)
            
            if(type(key) == KeyCode and key.char == ('9')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 9)
            
            if(type(key) == KeyCode and key.char == ('0')):
                nodo_movimiento.get_logger().info("dentro if 1")
                nodo_movimiento.hacer_poligono(tamaño, 10)

            if(type(key) == KeyCode and key.char == ('k')):
                nodo_movimiento.get_logger().info("dentro if k")
                nodo_movimiento.mover_absoluto(0.0, 0.0)
                nodo_movimiento.mover_absoluto(11.0, 0.0)
                nodo_movimiento.mover_absoluto(0.0, 11.0)
                nodo_movimiento.mover_absoluto(11.0, 11.0)
                nodo_movimiento.mover_absoluto()

            if(type(key) == KeyCode and key.char == ('r')):
                nodo_movimiento.get_logger().info("dentro del if del reset")
                nodo_movimiento.set_estado_lapiz(1)
                nodo_movimiento.peticion_reset()
                nodo_movimiento.set_estado_lapiz(0)
                


            #parar movimientos



        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

            
        rclpy.spin(nodo_movimiento)
    finally:
        rclpy.shutdown()



if __name__ == '__main__':
    main()