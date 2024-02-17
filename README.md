PhidgetInterfaceKit 8/8/8 w/6 Port Hub


## Instalacion via apt (solo si son necesarias):

- sudo apt update && sudo apt install git
- sudo apt update && sudo apt upgrade -y
- sudo apt install python3-pip
- sudo apt install screen
- sudo apt-get install python3-venv (Solo si requiere instalar un ambiente aparte)

## Clonar repositorio
- git clone https://github.com/uwulises/irrigation_inia_indoor.git
- cd irrigation_inia_indoor

# Instalacion via pip:

- pip install Phidget22 (quizas tengas que instalar manualmente https://www.phidgets.com/docs/OS_-_Linux#Package_Install-0 )
- pip install pandas

# Librerias:
- numpy == 1.26.4
- pandas == 2.2.0
- openpyxl (para crear excel)