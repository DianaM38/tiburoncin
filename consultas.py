import time

import requests

import excel  # Modulo nuestro 
import main  # Modulo nuestro


def getTasasDeCambio(moneda):
  url = f'https://api.frankfurter.app/latest?base={moneda}'

  try:
    response = requests.get(url)
    response.raise_for_status()  # Lanza una excepción para errores HTTP
    if response.status_code == 200:
      return response.json()
      
  except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
    time.sleep(2)
    main.main() 
    
def cambiosRecientes(moneda):
  print(f"Consultas recientes de cambios de tasas para la moneda {moneda}:\n")
  
  try:
    tasas = getTasasDeCambio(moneda)
    if tasas is not None:
      for otra_moneda, tasa in tasas['rates'].items():
        print(f"1 {moneda} = {tasa} {otra_moneda}")

      excel.guardarCambiosExcel(tasas['rates'], moneda)
     
      return tasas['rates']
    else:
      print('Hubo un error al consultar las tasas de cambio recientes.')
      return cambiosRecientes(moneda)
      
  except Exception as e:
    print(f"Error al realizar la solicitud: {e}")
    return None