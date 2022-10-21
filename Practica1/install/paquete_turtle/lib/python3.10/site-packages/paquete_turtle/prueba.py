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


class ClienteDibujar(Node):

    estadoPen = uint8
    r = uint8 
    g = uint8
    b = uint8
    width = uint8

    def __init__(self):
        super().__init__('Dibujar')
        self.cliente = self.create_client(SetPen, 'turtle1/set_pen')
        self.estadoPen = 0
        self.r = 170
        self.g = 170
        self.b = 170
        self.width = 3


        while not self.cliente.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')
        self.request = SetPen.Request()
        
    
    def peticion_set(self):

        self.request.r = self.r
        self.request.g = self.g
        self.request.b = self.b
        self.request.width = self.width
        
         
        self.get_logger().info(f"peticion lanzado  {self.estadoPen}")
        if(self.estadoPen == 0):
            self.estadoPen = 1
            self.request.off = 1
            
            self.get_logger().info("Primera rama if")
        elif(self.estadoPen == 1):
            self.estadoPen = 0
            self.request.off = 0
            
        else:
             self.get_logger().info("Problemas estado")
             #self.request.off = 0
        
        


        # Llamada asíncrona
        self.futuro = self.cliente.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()



def main(args=None):
    try:
        rclpy.init(args=args)
        nodo_movimiento = EmisorMovimiento() 
        nodo_dibujar = ClienteDibujar()

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
                
                vector.x = 2.0
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo_movimiento.publisher_Pose.publish(posicion)

            if(type(key) == KeyCode and key.char == ('s')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = -2.0
                vector.y = 0.0
                vector.z = 0.0
                posicion.linear = vector
                nodo_movimiento.publisher_Pose.publish(posicion)
            

            if(type(key) == KeyCode and key.char == ('a')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = 2.0
                posicion.angular = vector
                nodo_movimiento.publisher_Pose.publish(posicion)


            if(type(key) == KeyCode and key.char == ('d')):
                nodo_movimiento.get_logger().info("dentro del if")
                vector.x = 0.0
                vector.y = 0.0
                vector.z = -2.0
                posicion.angular = vector
                nodo_movimiento.publisher_Pose.publish(posicion)

            if(type(key) == Key and key == keyboard.Key.space):
                nodo_dibujar.get_logger().info("dentro if space")
                nodo_dibujar.peticion_set()



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