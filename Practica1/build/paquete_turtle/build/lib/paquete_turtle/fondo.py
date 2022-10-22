#!/usr/bin/env python3
import keyboard
from numpy import integer, uint8
from sympy import Integer
import rclpy
from rclpy.node import Node
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
import random
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
from time import sleep
from threading import Thread


class ParamFondo(Node):

    r = ParameterType.PARAMETER_INTEGER
    g = ParameterType.PARAMETER_INTEGER
    b = ParameterType.PARAMETER_INTEGER 

    fondo_dinamico = False

    def __init__(self):
        super().__init__('Fondo')
        self.cliente = self.create_client(SetParameters, 'turtlesim/set_parameters')
        
        self.r = 0
        self.g = 0
        self.b = 0

        while not self.cliente.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interruped while waiting for the server.')
                return
            else:
                self.get_logger().info('Server not available, waiting again...')

        daemon = Thread(target=self.cambiar_fondo_dinamico, daemon=True, name='Fondo_background')
        daemon.start()

        self.request = SetParameters.Request()

    def cambiar_fondo_rand(self):
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)

        parametro_r = Parameter(name = 'background_r',  value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.r))
        parametro_g = Parameter(name = 'background_g', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.g))
        parametro_b = Parameter(name = 'background_b', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.b))

        parametros = [parametro_r, parametro_g, parametro_b]
        self.request.parameters = parametros

        self.futuro = self.cliente.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def cambiar_fondo_blanco(self):
        self.r = 255
        self.g = 255
        self.b = 255

        parametro_r = Parameter(name = 'background_r',  value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.r))
        parametro_g = Parameter(name = 'background_g', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.g))
        parametro_b = Parameter(name = 'background_b', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.b))

        parametros = [parametro_r, parametro_g, parametro_b]
        self.request.parameters = parametros

        self.futuro = self.cliente.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def cambiar_fondo_negro(self):
        self.r = 0
        self.g = 0
        self.b = 0

        parametro_r = Parameter(name = 'background_r',  value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.r))
        parametro_g = Parameter(name = 'background_g', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.g))
        parametro_b = Parameter(name = 'background_b', value = ParameterValue(type = ParameterType.PARAMETER_INTEGER, integer_value = self.b))

        parametros = [parametro_r, parametro_g, parametro_b]
        self.request.parameters = parametros

        self.futuro = self.cliente.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.futuro)
        return self.futuro.result()


    def set_fondo_dinamico( self):
        self.fondo_dinamico = not self.fondo_dinamico
        return 0

    def cambiar_fondo_dinamico(self):
        while True:
            if(self.fondo_dinamico):
                self.get_logger().info('dentro del while')
                self.get_logger().info(f'valor de fondo_dinamico: {self.fondo_dinamico}')
                self.cambiar_fondo_rand()
            sleep(0.5)
        
            


def main(args=None):
    try:
        rclpy.init(args=args)
        nodo_fondo = ParamFondo()
 
        def on_press(key):
            pass

        def on_release(key):
            if(type(key) == Key and key == keyboard.Key.backspace):
                nodo_fondo.get_logger().info("dentro if backspace")
                nodo_fondo.cambiar_fondo_rand()

            if(type(key) == KeyCode and key.char == ('b')):
                nodo_fondo.get_logger().info("dentro if tecla: B ")
                nodo_fondo.cambiar_fondo_blanco()


            if(type(key) == KeyCode and key.char == ('n')):
                nodo_fondo.get_logger().info("dentro if tecla: N")
                nodo_fondo.cambiar_fondo_negro()


            if(type(key) == KeyCode and key.char == ('m')):
                nodo_fondo.get_logger().info("dentro if tecla: M")
                nodo_fondo.set_fondo_dinamico()
            

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
            
        rclpy.spin(nodo_fondo)
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()