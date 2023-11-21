import os
import time

import requests

import ask  # Modulo nuestro
import consultas  # Modulo nuestro
import excel  # Modulo nuestro
import graphics  # Modulo nuestro
from main import clean_consola


# Opcion 1: Consultas recientes de cambios tasas
def cambiosRecientes():
  clean_consola()

  try:
    m_consulta = ask.check_nom(
        "Ingresa la moneda para consultar cambios recientes: ")
    ro1 = consultas.cambiosRecientes(m_consulta)

    if ro1 is not None:
      i = 1
      nombre_archivo = "res_op_1_" + str(i) + ".txt"
      while os.path.exists(nombre_archivo):
        i += 1
        nombre_archivo = "res_op_1_" + str(i) + ".txt"

      with open(nombre_archivo, 'w') as archivo:
        archivo.write(f'Ultimas tasas de cambio para: \n{m_consulta}')
        for otra_moneda, tasa in ro1.items():
          archivo.write(f'1 {m_consulta} = {otra_moneda} {tasa}\n')

      print('Se ha creado el archivo: ' + str(nombre_archivo))
      print("\nGenerando grafica, por favor espere...")
      time.sleep(3)

      graphics.graphDisp(m_consulta)
      decision = ask.check_binario(
          "¿Deseas realizar otra consulta? (1=Si/0=No): ")

      if decision == 1:
        cambiosRecientes()
      else:
        pass
    else:
      print("Apareció un error al consultar los cambios recientes de tasas")

  except requests.exceptions.RequestException as ex:
    print("Error en la solicitud: " + str(ex))
    time.sleep(3)
    return None
  except KeyError as ex:
    print("Error al procesar resultado: " + str(ex))
    time.sleep(3)
    return None


# Opcion 2: Historial de cambio de tasas
def tasasHistoricas():
  clean_consola()

  fecha = ask.check_fecha()
  divisa = ask.check_nom(
      "Ingresa la divisa en la que quieres consultar los cambios: ")
  host = 'api.frankfurter.app'
  url = f'https://{host}/{fecha}?from={divisa}'

  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    tasas_historicas = data["rates"]

    print(f"Tasas de cambio históricas para {fecha}: ")
    for x in tasas_historicas:
      print(f"{x} = {tasas_historicas[x]}")
    try:
      excel.guardarCambiosTasas(tasas_historicas, divisa, fecha)
    except Exception as er:
      print("No jalo excel: ", er)
    print("\nResultados guardados en el archivo: resultads.xlsx\n")
    decision = ask.check_binario(
        "¿Deseas realizar otra consulta? (1=Si/0=No): ")

    if decision == 1:
      tasasHistoricas()
    else:
      pass

  except requests.exceptions.RequestException as ex:
    print("Error en la solicitud: " + str(ex))
    time.sleep(3)
    return None
  except KeyError as ex:
    print("Error al procesar resultado: " + str(ex))
    time.sleep(3)
    return None

# Opcion 3: Consultar informacion de divisas
def infoDivisa():
  clean_consola()
  try:

    div = ask.check_nom("Introduce la nomenclatura de la divisa: ")
    if div in ask.dictionary():
      print(f"{div}: {ask.dictionary()[div]}")

      print(
          f"A continuación una grafica para observar el comportamiento de la divisa {div} en el ultimo año.\nPor favor espere..."
      )
      time.sleep(3)
      # Mostrar histograma en donde se vera la frecuencia en la que ha cambiado la divisa en el ultimo año
      graphics.graphHist(div)
      decision = ask.check_binario(
          "¿Deseas realizar otra consulta? (1=Si/0=No): ")

      if decision == 1:
        infoDivisa()
      else:
        pass
    else:
      print("Error, nomenclatura invalida.")
      time.sleep(2)
  except requests.exceptions.RequestException as ex:
    print("Error en la solicitud: " + str(ex))
    time.sleep(3)
    return None
  except KeyError as ex:
    print("Error al procesar resultado: " + str(ex))
    time.sleep(3)
    return None


# Irving Joseafat Rodriguez Gonzalez
# Opcion 4: Conversiones de divisas
def convertion():

  clean_consola()
  div = ask.check_nom("Introduce la divisa que deseas convertir: ")
  divChange = ask.check_nom("Introduce la divisa a la que deseas convertir: ")
  mount = ask.check_cant(
      f"Introduce la cantidad de {div} que deseas convertir: ")

  host = 'api.frankfurter.app'
  url = f'https://{host}/latest?amount={mount}&from={div}&to={divChange}'

  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    conversion = None
    if 'rates' in data:
      conversion = data['rates'][divChange]

    print(f"\t\t{mount} {div} son {conversion} {divChange}")
    excel.guardarConversiones(div, mount, conversion, divChange)

    print("Generando grafica, por favor espere...")
    time.sleep(3)
    graphics.graphArea(div, divChange)

    decision = ask.check_binario(
        "¿Deseas realizar otra conversión? (1=Si/0=No): ")

    if decision == 1:
      convertion()
    else:
      pass

  except requests.exceptions.RequestException as ex:
    print("Error en la solicitud: " + str(ex))
    input()
    return None
  except KeyError as ex:
    print("Error al procesar resultado: " + str(ex))
    return None
