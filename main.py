import os
import sys
import time

import ask
import cambios


#Función para limpiar la pantalla
def clean_consola():
  if os.name == 'posix':
    os.system('clear')

def main():
  while True:
    clean_consola()
    menu = '''
    Bienvenido\nSelecciona una opción:
    1.- Consultas recientes de cambios tasas
    2.- Historial de cambio de tasas
    3.- Consultar informacion de divisas
    4.- Conversiones de monedas 
    5.- Salir
    '''
    print(menu)
    opcion = ask.check_cant("Ingresa el número de la opción deseada: ")
    
    if opcion == 1:
      cambios.cambiosRecientes()
    elif opcion == 2:
      cambios.tasasHistoricas()
    elif opcion == 3:
      cambios.infoDivisa()
    elif opcion == 4:
      cambios.convertion()
    elif opcion == 5:
      print("Saliendo del programa...")
      time.sleep(3)
      exit()
    else:
      print("La opción no es válida, ingresa un número del menú: ")

if __name__ == "__main__":
  main()