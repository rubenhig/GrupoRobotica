#!/usr/bin/env python3
import keyboard
from numpy import float32, uint8
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
from turtlesim.srv import TeleportAbsolute, SetPen


class EmisorMovimiento(Node): 
    #variables para el servicio pen:
    estadoPen = uint8
    r = uint8
    g = uint8
    b = uint8
    width = uint8

    # variables para el servicio reset:
    x = float32
    y = float32
    theta = float32


    def __init__(self):
        super().__init__('Movimiento')
        self.publisher_Radio = self.create_publisher(String, "radio", 10) 
        self.publisher_Pose = self.create_publisher(Twist, "/turtle1/cmd_vel", 100) 
        self.cliente_reset = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")
        self.cliente_lapiz = self.create_client(SetPen, "turtle1/set_pen")
        self.get_logger().info("Emisor lanzado")

        while not self.cliente_reset.wait_for_service(timeout_sec=1.0) and self.cliente_lapiz.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')
        self.request_reset = TeleportAbsolute.Request()
        self.request_lapiz = SetPen.Request()



    def set_estado_lapiz(self, estado):
        self.r = 170
        self.g = 170
        self.b = 170
        self.estadoPen = estado
        self.width = 3
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
        self.x = 5.544444561004639 # valor inicial
        self.y = 5.544444561004639
        self.theta = 0.0
        self.request_reset.x = self.x
        self.request_reset.y = self.y
        self.request_reset.theta = self.theta
        self.get_logger().info("peticion de reset lanzada")
        self.futuro_reset = self.cliente_reset.call_async(self.request_reset)
        rclpy.spin_until_future_complete(self, self.futuro_reset)
        return self.futuro_reset.result



def main(args=None):
    try:
        rclpy.init(args=args)
        nodo_movimiento = EmisorMovimiento() 

        velocidad = 3.0
        

        posicion = Twist()
        vector = Vector3()
 
        def on_press(key):
            nonlocal nodo_movimiento
            nodo_movimiento.get_logger().info("Funcion on_press <<<<<<<<<<<<<")
            
            nodo_movimiento.get_logger().info(str(key))

            msg = String()
            msg.data = str(key)
            nodo_movimiento.publisher_Radio.publish(msg)

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

            if(type(key) == KeyCode and key.char == ('r')):
                nodo_movimiento.get_logger().info("dentro del if del reset")
                nodo_movimiento.set_estado_lapiz(1)
                nodo_movimiento.peticion_reset()
                nodo_movimiento.set_estado_lapiz(0)



        def on_release(key):
            nonlocal nodo_movimiento
            nodo_movimiento.get_logger().info("Funcion on_release >>>>>>>>>>>>")
            
            nodo_movimiento.get_logger().info(str(key))


            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.0
            posicion.linear = vector
            posicion.angular = vector
            nodo_movimiento.publisher_Pose.publish(posicion)



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