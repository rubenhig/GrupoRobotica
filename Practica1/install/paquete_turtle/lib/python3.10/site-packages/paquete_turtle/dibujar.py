#!/usr/bin/env python3
import keyboard
from matplotlib.transforms import blended_transform_factory
from numpy import uint8
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
from turtlesim.srv import SetPen
from time import sleep
from threading import Thread
import random
from std_srvs.srv import Empty

class ClienteClear(Node):

    def __init__(self):
        super().__init__('ClienteClear')
        self.cliente_clear = self.create_client(Empty, 'clear')
        # Esperamos a que el servicio esté disponible
        while not self.cliente_clear.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')
        self.request_clear = Empty.Request()
    
    def peticion_c(self):

        self.futuro = self.cliente_clear.call_async(self.request_clear)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


class ClienteDibujar(Node):

    estadoPen = uint8
    r = uint8 
    g = uint8
    b = uint8
    width = uint8

    color_dinamico = False

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

        daemon = Thread(target=self.cambiar_color_dinamico, daemon=True, name='Color_lapiz')
        daemon.start()

        self.request = SetPen.Request()
        
    
    def cambiar_param_dibujar(self, red = None, green = None, blue = None, pen = None, width = None):
        self.r = red if red != None else self.r
        self.g = green if green != None else self.g
        self.b = blue if blue != None else self.b
        self.estadoPen = pen if pen != None else self.estadoPen
        self.width = width if width != None else self.width


        self.request.r = self.r
        self.request.g = self.g
        self.request.b = self.b
        self.request.width = self.width
        self.request.off = self.estadoPen

        self.futuro = self.cliente.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def peticion_set(self):
        self.get_logger().info(f"peticion lanzado  {self.estadoPen}")
        if(self.estadoPen == 0):
            self.cambiar_param_dibujar(pen=1)
            
            self.get_logger().info("Primera rama if")
        elif(self.estadoPen == 1):
            self.cambiar_param_dibujar(pen=0)
            
        else:
             self.get_logger().info("Problemas estado")
             #self.request.off = 0
        
    

    def cambiar_color_rand(self):
        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        self.cambiar_param_dibujar(red=r, green=g, blue=b)


    def set_color_dinamico( self):
        self.color_dinamico = not self.color_dinamico
        return 0

    def cambiar_color_dinamico(self):
        while True:
            if(self.color_dinamico):
                self.get_logger().info('dentro del while')
                self.get_logger().info(f'valor de fondo_dinamico: {self.color_dinamico}')
                self.cambiar_color_rand()
            sleep(0.1)

    def cambiar_thicc_mas(self):

        if self.width < 10:
            self.cambiar_param_dibujar(width= self.width +1)
        



    def cambiar_thicc_menos(self):

        if self.width > 0:
            self.cambiar_param_dibujar(width= self.width -1)

        



def main(args=None):
    try:
        rclpy.init(args=args)
        nodo_dibujar = ClienteDibujar()
        nodo_clear = ClienteClear()
 
        def on_press(key):
            pass



        def on_release(key):
            if(type(key) == KeyCode and key.char == ('v')):
                nodo_dibujar.get_logger().info("dentro if tecla: v")
                nodo_dibujar.set_color_dinamico()

            if(type(key) == Key and key == keyboard.Key.space):
                nodo_dibujar.get_logger().info("dentro if space")
                nodo_dibujar.peticion_set()
            
            if(type(key) == Key and key == keyboard.Key.up):
                nodo_dibujar.get_logger().info("dentro if flecha arriba")
                nodo_dibujar.cambiar_thicc_mas()

            if(type(key) == Key and key == keyboard.Key.down):
                nodo_dibujar.get_logger().info("dentro if flecha abajo")
                nodo_dibujar.cambiar_thicc_menos()


            if(type(key) == KeyCode and key.char == ('c')):
                nodo_clear.get_logger().info("dentro if tecla: C")
                nodo_clear.peticion_c()



        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

            
        rclpy.spin(nodo_dibujar)
        rclpy.spin(nodo_clear)
    finally:
        rclpy.shutdown()



if __name__ == '__main__':
    main()