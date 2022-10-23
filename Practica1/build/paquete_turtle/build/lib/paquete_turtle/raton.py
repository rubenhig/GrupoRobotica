#!/usr/bin/env python3
import keyboard
from numpy import uint8
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist, Vector3
from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener, KeyCode
from pynput.mouse import Listener, Button
from turtlesim.srv import SetPen, TeleportRelative, TeleportAbsolute
import math
import pyautogui                        #es necesario instalar pyautogui
from time import sleep
from threading import Thread



class NodoRaton(Node):  

    x = 0.0
    y = 0.0

    pintar_raton = False

    def __init__(self):
        super().__init__('Raton')

        self.cliente_relativo = self.create_client(TeleportRelative, 'turtle1/teleport_relative')
        self.request_relativo = TeleportRelative.Request()

        self.cliente_absoluto = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.request_absoluto = TeleportAbsolute.Request()

        daemon = Thread(target=self.mover_absoluto_periodico, daemon=True, name='pintar_raton')
        daemon.start()

        self.get_logger().info("Emisor lanzado")

    
    
    
    def mover_absoluto(self, x, y, theta):
        self.request_absoluto.x = x  
        self.request_absoluto.y = y
        self.request_absoluto.theta = theta


        self.futuro = self.cliente_absoluto.call_async(self.request_absoluto)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()

    def mover_absoluto_periodico(self):

        while True:
            if(self.pintar_raton and (self.x != 0.0) and (self.y != 0.0)):
                self.get_logger().info(f'Llamada a mover_absoluto: {self.x}, {self.y}')
                self.mover_absoluto(self.x, self.y, 0.0)
            sleep(0.1)
        

    def set_posicion(self, x, y):
        self.x = x
        self.y = y
    
    def set_pintar(self, pintar):
        self.pintar_raton = pintar
    


def main(args=None):
    try:
        rclpy.init(args=args)


        nodo_raton = NodoRaton() 

        ancho, alto = pyautogui.size()

        x_turtle = 0.0
        y_turtle = 0.0

        pintar_raton = False

        nodo_raton.get_logger().info(f"Tamaño pantalla : ({ancho},{alto})")


        def on_move(x, y):
            nonlocal x_turtle, y_turtle
            if(pintar_raton):
                x_turtle = float((11 * x) / ancho)
                y_turtle= 11.0 - float((11 * y ) / alto)
                nodo_raton.set_posicion(x_turtle, y_turtle)
                #nodo_raton.get_logger().info(f"Posicion del raton : ({x},{y})")
            

        def on_click(x, y, button, pressed):
            nonlocal pintar_raton
            if(button == Button.right and pressed):
                nodo_raton.get_logger().info("dentro if boton")
                pintar_raton = not pintar_raton
                nodo_raton.set_pintar(pintar_raton)
            

            nodo_raton.get_logger().info(f"Posicion del raton : ({x},{y})")
            

        with mouse.Listener(
                on_move = on_move,
                on_click=on_click) as listener_raton:
            listener_raton.join()

            
        rclpy.spin(nodo_raton)
    finally:
        rclpy.shutdown()



if __name__ == '__main__':
    main()