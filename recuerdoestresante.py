import requests

# ESTE PEDO MORIRA PERO NO LO BORREN

#Modulo para manejo de informacion
"""
   Funciones del modulo:
   -get_cambio:
      Funcion que devuelve la tasa de cambio de la moneda solicitada
   -get_cambios_res:
      Funcion que devuelve los cambios recientes de la divisa solicitada
   -get_Conversion:
      Funcion que devuelve la conversion de dos divisas dadas
"""
def get_cambio(moneda):
  """
  Funcion que devuelve la tasa de cambio de la moneda solicitada

  Recibe: La divisa solicitada
  
  Devuelve: La tasa de cambio de la divisa solicitada
  """
  
  url = f'https://api.frankfurter.app/latest?base={moneda}'
  headers = {'Content-Type': 'application/json; charset=utf-8'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza una excepción para errores HTTP
    datos = response.json()
    return datos

  except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
    return None

def get_cambios_res(moneda):
  """
  Funcion que devuelve los cambios recientes de la divisa solicitada
  
  Recibe: La divisa solicitada
  
  Devuelve: Los cambios recientes de la divisa solicitada
  """
  
  print(f"Consultas recientes de cambios de tasas para la moneda {moneda}:\n")

  tasas = get_cambio(moneda)

  if tasas:
    for otra_moneda, tasa in tasas['rates'].items():
      print(f"1 {moneda} = {tasa} {otra_moneda}")
      
  else:
    print('Hubo un error al consultar las tasas de cambio recientes.')


def get_conversion(cantidad, de_moneda, a_moneda):
  """
  Funcion que devuelve la conversion de dos divisas dadas

  Recibe: La cantidad, la divisa de origen y la divisa de destino

  Devuelve: La conversion de dos divisas dadas
  """
  
  host = 'api.frankfurter.app'
  url = f'https://{host}/latest?amount={cantidad}&from={de_moneda.upper()}&to={a_moneda.upper()}'
  
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    tasa_conversion = data['rates'][a_moneda.upper()]
    resultado = cantidad * tasa_conversion
    return resultado
    
  except requests.exceptions.RequestException as ex:
    print("Error en la solicitud" + str(ex))
    return None
    
  except KeyError as ex:
    print("Error al procesar resultado" + str(ex))
    return None
