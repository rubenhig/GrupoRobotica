# Display

## Descripción

El nodo [Display](https://cyberbotics.com/doc/reference/display) consta de un vector de pixeles controlable por una API simple. El resultado se puede renderizar sobre una capa 2D de una vista 3D, en una textura 2D de cualquier nodo de clase [Figura](https://cyberbotics.com/doc/reference/shape). La información representada por el [Display](https://cyberbotics.com/doc/reference/display)  puede ser un grafo, texto, trayectoria de un robot, imagen de una camara, etc.

## Modo de uso

Para crear un diplay integrado el primer hijo del nodo [Display](https://cyberbotics.com/doc/reference/display)  deberá ser un nodo de tipo [Figura](https://cyberbotics.com/doc/reference/shape) que consta de la apariencia y del nodo [ImageTexture](https://cyberbotics.com/doc/reference/appearance), después la textura interna de [ImageTexture](https://cyberbotics.com/doc/reference/appearance) es reemplazada por la textura del [Display](https://cyberbotics.com/doc/reference/display).

Ambos nodos [Appearance](https://cyberbotics.com/doc/reference/appearance) y [PBRAppearance](https://cyberbotics.com/doc/reference/pbrappearance) son compatibles y pueden reemplazar al nodo hijo ateriormente explicado.

En caso de usar [PBRAppearance](https://cyberbotics.com/doc/reference/pbrappearance), <code>PBRAppearance.baseColorMap</code> o <code>PBRAppearance.emissiveColorMap</code>  el nodo [ImageTexture](https://cyberbotics.com/doc/reference/appearance) debería estar definido. En el caso de que ambos esten definidos ambas texturas serán reemplazadas por la textura del [Display](https://cyberbotics.com/doc/reference/display)

Si el nodo usado es [Appearance](https://cyberbotics.com/doc/reference/appearance) es recomendado cambiar el campo <code> Material.emissiveColor</code> al valor <code>(1,1,1)</code> para que la textura cargada mantenga los colores originales. Adicionalmente, será necesario cambiar el campo <code> filtering </code> del nodo [ImageTexture](https://cyberbotics.com/doc/reference/appearance) al valor 0 para prevenir errores visales al distanciarse de él.

## Atributos
El [Display](https://cyberbotics.com/doc/reference/display) tiene dos atributos: 

- <code>witdh</code>: longitud de la anchura del display en pixeles.
- <code>height</code>: longitud de la altura del display en pixeles.

## Sistemas de coordenadas
Al apuntar a un pixel concreto del [Display](https://cyberbotics.com/doc/reference/display) dentro de la interfaz de Webots, en la barra debajo de la consola conocida como barra de estado, se mostrará el valor RGBA (4X8 bits). 

Las coordenadas coincidirán con el numero de pixeles que tiene el [Display](https://cyberbotics.com/doc/reference/display) de altura y anchura teniendo como referencia el pixel de arriba a la izquierda siendo este el <code>(0,0)</code> y el pixel de abajo a la derecha será <code>(width-1,height-1)</code>

## Interfaz de la imagen
Es posible mostrar la imagen del [Display](https://cyberbotics.com/doc/reference/display) superpuesto en la ventana 3D de Webots dentro de un recuadro cian al cual se puede mover y reajustar el tamaño. El boton para cerrar este recuadro está arriba a la derechar del mismo.

Es posible sacar la imagen del [Display](https://cyberbotics.com/doc/reference/display) en una ventana externa haciendo doble click sobre ella. Al cerrar la ventana volverá a mostrarse en el recuadro cian en la posición anterior.

![N|Solid](https://raw.githubusercontent.com/cyberbotics/webots/released/docs/reference/images/display_overlay.png)

## Funciones de contexto
El [Display](https://cyberbotics.com/doc/reference/display) posee dos funciones contextuales que consisten en :
  
- <code>wb_display_set_*</code> : sirve para establecer el estado actual del display en diferentes aspectos.
- <code>wb_display_draw_*</code> : sirve para dibujar formas sencillas como por ejemplo lineas o cuadrados.

## Funciones del Display

- <code>getWidth(self)</code> : 
  
  Devuelve la anchura del Display
- <code>getHeight(self)</code> : 
  
  Devuelve la altura del Display
- <code>setColor(self, color)</code> :
  
  Cambia el color que será usado para las acciones de dibujar y rellenar. El valor que se le dará es de tipo hexadecimal representando cada 8 bits un color siendo el orden de izquierda a derecha rojo, verde y azul en acorde al estándar RGB.
  
  Ejemplos:
  ```
  0x00FF00 --> Verde
  0xFF00FF --> Morado
  0x000000 --> Negro
  0xFFFFFF --> Blanco
  ```

- <code>setAlpha(self, alpha)</code> :
  
  El valor alfa define la transparencia del pixel en el Display. Este valor se deberá modificar si se trata con Displays especiales que puedan ser transparentes o semitransparentes.
  El valor a dar está dentro del rango <code>[0.0,1.0]</code>.
- <code>setOpacity(self, opacity)</code> :
  
  Esta función define la opacidad de los pixeles nuevos por dibujar. El valor que se le puede asignar está dentro del rango <code>[0.0,1.0]</code>.
  Solo el color de verá afectado en acorde a la siguiente formula:

  ![N|Solid](https://raw.githubusercontent.com/cyberbotics/webots/released/docs/reference/images/display_opacity.png)


- <code>setFont(self, font, size, antiAliasing)</code> :
  
  En caso de imprimir texto en el Display esta funcion premitirá cambiar la fuente de la letra. A continuacion la lista de fuentes:
  ```sh
   - Arial
   - Arial Black
   - Comic Sans MS
   - Courier New
   - Georgia
   - Impact
   - Lucida Console
   - Lucida Sans Unicode
   - Palatino Linotype
   - Tahoma
   - Times New Roman
   - Trebuchet MS
   - Verdana
    ```
 
- <code>attachCamera(Camera camera)</code> :
    
    En caso de contar con una camara en el proyecto puedes enlazarla con el display.

- <code>detachCamera()</code> :

    En caso de contar con una camara en el proyecto puedes desenlazarla con el display.

- <code>drawPixel(self, x, y)</code> :

    Esta función dibuja un pixel del lienzo en las coordenadas (x,y).
- <code>drawLine(self, x1, y1, x2, y2)</code> :

    Esta función traza una línea en el lienzo desde las coordenadas (x1,y1) a (x2,y2). 
- <code>drawRectangle(self, x, y, width, height)</code> :

    Esta función dibuja un rectangulo de anchura "width" y altura "height" tomando como referencia el pixel de arriba a la izquierda de coordenadas (x,y).
- <code>drawOval(self, cx, cy, a, b)</code> :

    Esta función dibuja un óvalo cuyo centro esta en las coordenadas (cx,cy) y los valores a y b indican la longitud del eje horizontal y vertical respectivamente.

- <code>drawPolygon(self, x, y)</code> :

    Esta función dibuja un polígono donde x e y son vectores que concretan las coordenadas de los vertices.

- <code>drawText(self, text, x, y)</code> :

    Esta función imprime un texto ASCII desde la coordenada (x,y) con la fuente por defecto o definida por la función <code>setFont</code>.

- <code>fillRectangle(self, x, y, width, height)</code> :

    Esta función un rectángulo al igual que <code>drawRectangle</code> con la diferencia de que lo rellena del color definido.

- <code>fillOval(self, cx, cy, a, b)</code> :

    Esta función un óvalo al igual que <code>drawOval</code> con la diferencia de que lo rellena del color definido.

- <code>fillPolygon(self, x, y)</code> :

    Esta función un polígono al igual que <code>drawPoligon</code> con la diferencia de que lo rellena del color definido.

- <code>imageNew(self, data, format, width=None, height=None)</code> :

    Esta función crea una nueva imagen de anchura "width" y altura "height". "data" es la informaión de la imagen y "format" el formato. La imagen es guardada en el portapapeles.

- <code>imageLoad(self, filename)</code> :

    Esta funcion crea una nueva imagen basada en el archivo en formato de imagen dado como parametro. La imagen es guardada en el portapapeles.

- <code>imageCopy(self, x, y, width, height)</code> : 

    Esta función copia la imagen de una fuente externa, como por ejemplo un fotograma de una camara. La imagen es guardada en el portapapeles.

- <code>imagePaste(self, ir, x, y, blend=False)</code> : 

    Esta función pega la imagen copiada por la función anterior.

- <code>imageSave(self, ir, filename)</code> : 

    Esta función guarda la imagen guardada en el portapapeles, o si no hay ninguna guardada será el fotograma actual que esté en el display, en el host.

- <code>imageDelete(self, ir)</code> : 

    Esta función borra la imagen guardada en el portapapeles. Se recomienda que una vez ya no se use una imagen del portapapeles se borre de inmediato.


## Webots Display VS. IRL Display
Los displays son muy parecidos en cuanto a funcionalidad con los de la vida real. Una pantalla que consta de pixeles que representan la información que les entra.

La única diferencia que le veo es la ventana estilo pop-up que aparece en la ventana de la simulación, no te aparece una ventana flotando en la vida real de lo que está viendo una camara de seguridad como en las pelis de sci-fi con hackers y dispositivos superavanzados. Una pena.