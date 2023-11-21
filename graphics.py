# Irving estuvo aquí sufriendo bastante
# Las graficas seran importadas desde aqui hacia cambios.py en sus respectivas opciones.

from datetime import datetime, timedelta  # Para las fechas

import matplotlib.pyplot as plt
import requests

from ask import dictionary  # El diccionario <3

# Grafica 1: Grafica de dispersion en la opción 1 principal
"""
DIVIDIMOS LOS PAISES POR CONTINENTES, HACEMOS UNA GRAFICA EN CADA CONTINENTE Y
AL FINAL LAS MOSTRAMOS TODAS EN UNA SOLA IMAGEN NO SIN ANTES GUARDARLAS
EN IMAGENES PNG
"""
def graphDisp(div):
  
  divisas = dictionary()
  continentes = {
      'Asia': ['CNY', 'HKD', 'IDR', 'INR', 'JPY', 'KRW', 'MYR', 'PHP', 'SGD', 'THB', 'TRY'],
      'Europa': ['BGN', 'CZK', 'DKK', 'EUR', 'GBP', 'HUF', 'NOK', 'PLN', 'RON', 'SEK', 'CHF'],
      'Oceanía y África': ['AUD', 'NZD', 'ZAR'],
      'América': ['BRL', 'CAD', 'MXN', 'USD'],
  }

  url = f"https://api.frankfurter.app/latest?base={div}"
  
  response = requests.get(url)
  tasasCambio = response.json()['rates']

  # Con esto creamos las graficas para cada continente
  for continente, paises in continentes.items():
      plt.figure(figsize=(12, 6))
      plt.title(f"Tasas de Cambio ({continente})", fontsize=18, color='navy', fontweight='bold')
      plt.xlabel("País", fontsize=14, color='darkgreen')
      plt.ylabel("Tasa de Cambio", fontsize=14, color='darkgreen')

      tasas = [tasasCambio.get(pais, 0) for pais in paises]
      nombres_paises = [divisas[pais] for pais in paises]

      bars = plt.bar(nombres_paises, tasas, color='skyblue', edgecolor='black')

      # Mostrar los valores en las barras
      for bar in bars:
          yval = bar.get_height()
          plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 4),
                   ha='center', va='bottom', color='darkred', fontweight='bold', fontsize=10)

      # Añadir una línea de tendencia
      plt.plot(nombres_paises, tasas, color='orange', label='Línea de Tendencia', linestyle='--', linewidth=2)

      plt.xticks(rotation=45, ha="right", fontsize=10, fontweight='bold', color='darkblue')
      plt.yticks(fontsize=10, fontweight='bold', color='darkblue')
      plt.grid(axis='y', linestyle='--', alpha=0.7)
      plt.tight_layout()
      plt.savefig(f'graficaDe{continente}.png')  # Guardar cada gráfica en un archivo PNG
      plt.show()

  # Aquí combinamos todas las gráficas en una sola imagen
  plt.figure(figsize=(15, 8))
  plt.suptitle("Tasas de cambio por continente (MXN)", fontsize=22, color='purple', fontweight='bold')

  for i, (continente, paises) in enumerate(continentes.items(), 1):
      plt.subplot(2, 3, i)
      plt.title(continente, fontsize=16, color='green', fontweight='bold')

      tasas = [tasasCambio.get(pais, 0) for pais in paises]
      nombres_paises = [divisas[pais] for pais in paises]

      bars = plt.bar(nombres_paises, tasas, color='skyblue', edgecolor='black')

      # Mostrar los valores en las barras
      for bar in bars:
          yval = bar.get_height()
          plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 4),
                   ha='center', va='bottom', color='darkred', fontweight='bold', fontsize=8)

      # Añadir una línea de tendencia
      plt.plot(nombres_paises, tasas, color='orange', label='Línea de Tendencia', linestyle='--', linewidth=2)

      plt.xticks(rotation=45, ha="right", fontsize=10, fontweight='bold', color='darkblue')
      plt.yticks(fontsize=10, fontweight='bold', color='darkblue')
      plt.grid(axis='y', linestyle='--', alpha=0.7)

  plt.tight_layout(rect=[0, 0.03, 1, 0.95])
  plt.savefig('TodasLasGraficasOP1.png')
  plt.show()

# Grafica 2: Histograma en la opcion 3 principal
"""
Esta es una grafica que visualmente es de dispersion pero la manera en la que estan ordenados los datos y el como se relacionan con los ejes es la de un histograma (lo decidimos hacer asi porque en barras queda muy desagradable para la vista).
"""
def graphHist(div):
  
  # Las fechas son del ultimo año
  hoy = datetime.now()
  fechaInicio = (hoy - timedelta(days=365)).strftime('%Y-%m-%d')
  fechaFin = hoy.strftime('%Y-%m-%d')

  try:
    
    if div == "MXN":
      url = f'https://www.frankfurter.app/{fechaInicio}..{fechaFin}?from=MXN'
    else:
      url = f'https://www.frankfurter.app/{fechaInicio}..{fechaFin}?from={div}&to=MXN'
      
    response = requests.get(url)
    datos = response.json()
    tasas = datos['rates']

    # Obtener las tasas de cambio
    tasasCambio = datos.get('rates', {})
    
    fechas = []
    tasas = []
    # Aqui obtenemos las fechas y las tasas
    for fecha, tasasDiarias in tasasCambio.items():
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        fechas.append(fecha_dt)
        tasas.append(tasasDiarias['MXN'])
    # Ajustar el tamaño de la figura
    plt.figure(figsize=(15, 8))

    # Crear el gráfico de dispersión con etiquetas
    plt.plot(fechas, tasas, marker='*', color='purple', linestyle='-')
    
    for i, txt in enumerate(tasas):
        plt.annotate(f'{txt:.4f}', (fechas[i], tasas[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='black')

    # Decoramos un poco la grafica
    plt.title('Histograma de cambio de tasas en el ultimo año')
    plt.xlabel('Fecha')
    plt.ylabel('Tasa de Cambio a MXN')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("Histograma.png")
    plt.show()

  except requests.exceptions.RequestException as ex:
        print("Error en la solicitud:", str(ex))
  except KeyError as ex:
        print("Error al procesar resultado:", str(ex))

# Grafica 3: Grafica de area en la opcion 4 principal
    
def graphArea(div, divChange):
  # Fechas de inicio y fin para obtener tasas de cambio desde el año 2010 hasta 2022
  fechaInicio = "2010-01-01"
  fechaFin = "2022-12-31"

  # URL de la API de Frankfurter para obtener tasas de cambio
  url = f'https://www.frankfurter.app/{fechaInicio}..{fechaFin}?from={div}&to={divChange}'

  try:
      # Realizar la solicitud a la API
      response = requests.get(url)
      datos = response.json()

      # Obtener las fechas y tasas de cambio
      fechas = list(datos['rates'].keys())
      tasas = [valor[divChange] for valor in datos['rates'].values()]
  
      plt.figure(figsize=(15, 6))
  
      # Crear el gráfico de área
      plt.fill_between([datetime.strptime(fecha, "%Y-%m-%d") for fecha in fechas], 0, tasas, color='skyblue', alpha=0.4, label='Conversiones en la ultima decada')
  
      # Añadir una línea de tendencia
      plt.plot([datetime.strptime(fecha, "%Y-%m-%d") for fecha in fechas], tasas, color='orange', label='Linea de tendencia')
  
      # Decorar la gráfica
      plt.title(f'Conversiones en la ultima decada ({div} a {divChange})', fontsize=16)
      plt.xlabel('Fecha', fontsize=12)
      plt.ylabel(f'Tasa de cambio a {divChange}', fontsize=12)
      plt.xticks(rotation=45, ha='right', fontsize=10)
      plt.yticks(fontsize=10)
      plt.grid(axis='y', linestyle='--', alpha=0.7)
  
      plt.legend(loc = "upper left")
      plt.tight_layout()
      plt.savefig(f"Conversiones {divChange}.png")
      plt.show()

  except requests.exceptions.RequestException as ex:
      print("Error en la solicitud:", str(ex))
  except KeyError as ex:
      print("Error al procesar resultado:", str(ex))