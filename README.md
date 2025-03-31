## IMPLEMENTACIÓN EN PYTHON DE MÉTODOS EM Y OSEM PARA RECONSTRUCCIÓN DE IMAGEN PET ##

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
