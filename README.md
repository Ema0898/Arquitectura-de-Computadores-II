# Arquitectura-de-Computadores-II

## Coherencia de Caché

Este repositorio corresponde con el Proyecto #1 del curso Arquitectura de Computadores II del carrera Ingeniería en Computadores del Instituto Tecnológico de Costa Rica.

En el presente proyecto se implementa un simulador de un sistema multiprocesador con dos niveles de caché, los procesadores se organizan en dos chips de dos procesadores cada uno. La caché L1 es privada para cada procesador, su coherencia se implementa mediante el protocolo de monitoreo y la caché L2 es propia de cada chip, su coherencia se implementa mendiante el protocolo basado en directorios. Ambas caché utilizan el protocolo MSI y la política de escritura write-through

### Instalación
Para poder ejecutar este proyecto es necesario tener instalado Python 3.X en el sistema. Si se desea ejecutarlo en alguna distribución de Linux es necesario editar el archivo gui.py de la carpeta src. Se debe cambiar la línea 205 de root.attributes('-fullscreen', True) a root.attributes('-zoomed', True). Para ejectuarlo en Windows no es necesario realizar cambios.

#### Numpy
Para ejecutar el programa es necesario tener instalado la biblioteca numpy en el sistema, para ello se debe ejecutar el siguiente comando
```
pip install numpy
```

Si se está en Linux y se tiene instalado Python 2.7 y Python 3.X se debe ejecutar el siguiente comando en la raíz del proyecto
```
pip3 install numpy
```

#### Tkinter
Para ejecutar el programa es necesario tener instalado la biblioteca tkinter en el sistema, para ello se debe ejecutar el siguiente comando
```
pip install tkinter
```

Si se está en Linux y se tiene instalado Python 2.7 y Python 3.X se debe ejecutar el siguiente comando en la raíz del proyecto
```
pip3 install tkinter
```

### Ejecución
Para ejecutar el programa se debe ejecutar el siguiente comando en la terminal de la raíz del proyecto
```
python src/gui.py
```

Si se está en Linux y se tiene instalado Python 2.7 y Python 3.X se debe ejecutar el siguiente comando en la raíz del proyecto
```
python3 src/gui.py
```

### Historial
* 1.0.0
  * Se agrega la versión funcional del proyecto.
