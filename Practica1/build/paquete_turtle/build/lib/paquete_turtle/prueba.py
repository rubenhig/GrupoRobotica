#!/usr/bin/env python3
import keyboard
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput.keyboard import Key, Listener, KeyCode


class EmisorPosicion(Node):  
    def __init__(self):
        super().__init__('prueba')
        self.publisher_Radio = self.create_publisher(String, "radio", 10) 
        self.publisher_Pose = self.create_publisher(Twist, "/turtle1/cmd_vel", 100) 
        self.get_logger().info("Emisor lanzado")





def main(args=None):
    try:
        rclpy.init(args=args)
        nodo = EmisorPosicion() 

        posicion = Twist()
        vector = Vector3()
 
        def on_press(key):
            nonlocal nodo
            nodo.get_logger().info("Funcion on_press <<<<<<<<<<<<<")
            
            nodo.get_logger().info(str(key))

            msg = String()
            msg.data = str(key)
            nodo.publisher_Radio.publish(msg)

            if(type(key) == KeyCode and key.char == ('w')):
                nodo.get_logger().info("dentro del if")
                
                vector.x = 2.0
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo.publisher_Pose.publish(posicion)

            if(type(key) == KeyCode and key.char == ('s')):
                nodo.get_logger().info("dentro del if")
                vector.x = -2.0
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo.publisher_Pose.publish(posicion)
            

            if(type(key) == KeyCode and key.char == ('a')):
                nodo.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = 2.0
                posicion.angular = vector
                nodo.publisher_Pose.publish(posicion)


            if(type(key) == KeyCode and key.char == ('d')):
                nodo.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = -2.0
                posicion.angular = vector
                nodo.publisher_Pose.publish(posicion)


        def on_release(key):
            nonlocal nodo
            nodo.get_logger().info("Funcion on_release >>>>>>>>>>>>")
            
            nodo.get_logger().info(str(key))


            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.0
            posicion.linear = vector
            posicion.angular = vector
            nodo.publisher_Pose.publish(posicion)



            #parar movimientos



        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

            
        rclpy.spin(nodo)
    finally:
        rclpy.shutdown()



if __name__ == '__main__':
    main()