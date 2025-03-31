## IMPLEMENTACIÓN EN PYTHON DE MÉTODOS EM Y OSEM PARA RECONSTRUCCIÓN DE IMAGEN PET ##

El archivo pet_data_for_python.mat se genera ejecutando el script generate_data.m en MATLAB, aunque lo incluimos aquí para que no sea necesario hacer este paso previo. De forma similar, incluimos los gráficos que se generaron en la última ejecución del código en la carpeta plots, aunque se puede ejecutar main.py para volverlos a generar.

# Requisitos
Tener Python3 instalado.

# Instalación de dependencias
Abrir una consola en la carpeta del proyecto y ejecutar el comando 
```bash
pip install -r requirements.txt
```
Esto instalará todas las dependencias necesarias para ejecutar el código del proyecto.

Como alternativa, se puede ejecutar este comando tras crear un entorno virtual Python, con el objetivo de no sobreescribir las versiones de las librerías que se tengan instaladas en el entorno del usuario. Para más información sobre esto, visitar https://docs.python.org/es/3.8/library/venv.html

# Ejecución
El programa se ejecuta desde el archivo main.py. Para correrlo, navegar a la carpeta del proyecto, abrir una consola y escribir el comando
```bash
python main.py
```
El archivo pet_data_for_python.mat se genera ejecutando el script generate_data.m en MATLAB, aunque lo incluimos aquí para que no sea necesario hacer ese paso previo. De forma similar, incluimos los gráficos que se generaron en la última ejecución del código en la carpeta plots, aunque se puede ejecutar main.py para volverlos a generar.

# Opcional: generar pet_data_for_python.mat
El script generate_data.m emplea internamente funciones auxiliares implementadas en el archivo comprimido "Código de la práctica" de Moodle. Dado que no lo hemos desarrollado nosotros, hemos considerado prudente no incluirlo en el repositorio junto con lo que sí. Bastaría con incluir la carpeta que contiene este archivo comprimido dentro de aquella en de este proyecto para que funcione generate_data.m.

En caso de que, aun habiéndola incluido, dé error, se deberá seleccionar la opción "Set path" del menú "Home" de Matlab. Una vez allí, escoger la opción "Add with subfolders", seleccionar la carpeta _Codigo_Practica_ReconstruccionPET_ y presionar "Done".
