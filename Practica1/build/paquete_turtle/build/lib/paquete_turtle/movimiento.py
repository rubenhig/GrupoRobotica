#!/usr/bin/env python3
import keyboard
from numpy import uint8
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
from turtlesim.srv import SetPen


class EmisorMovimiento(Node):  
    def __init__(self):
        super().__init__('Movimiento')
        self.publisher_Radio = self.create_publisher(String, "radio", 10) 
        self.publisher_Pose = self.create_publisher(Twist, "/turtle1/cmd_vel", 100) 
        self.get_logger().info("Emisor lanzado")




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