# Excepciones para validar todo el rollo con queso
import re


# El diccionario que nos proporciona la api
def dictionary():
  divisas = {
    "AUD": "Australian Dollar",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Renminbi Yuan",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EUR": "Euro",
    "GBP": "British Pound",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Sheqel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "JPY": "Japanese Yen",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PHP": "Philippine Peso",
    "PLN": "Polish Złoty",
    "RON": "Romanian Leu",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "USD": "United States Dollar",
    "ZAR": "South African Rand"
  }
  return divisas

# Funcion para validar numeros flotantes
def check_cant(mensaje):
  try:
    cant = float(input(mensaje))
  except ValueError:
    print("Debes ingresar números")
    cant = check_cant(mensaje)
  return cant

# Funcion para verificar la fecha que introduce el usuario
def check_fecha():
  fecha = input("Ingresa la fecha en formato YYYY-MM-DD: ")
  re_fecha = re.compile(r"\d{4}-\d{2}-\d{2}")
  encon = re_fecha.findall(fecha)
  while encon == []:
    return check_fecha()
  #Elimina los "-" y separa en varias cadenas de texto
  partes = str.split(fecha, "-")

  if int(partes[0]) < 1999 or int(partes[0]) > 2030:
    return check_fecha()
  if int(partes[1]) < 1 or int(partes[1]) > 12:
    return check_fecha()
  if int(partes[2]) < 1 or int(partes[2]) > 31:
    return check_fecha()
  if int(partes[1]) == 2 and int(partes[2]) > 28 and int(partes[0]) % 4 != 0:
    partes[2] = "01"
    partes[1] = "03"
  if int(partes[1]) == 2 and int(partes[2]) > 29 and int(partes[0]) % 4 == 0:
    partes[2] = "01"
    partes[1] = "03"
  fecha = partes[0] + "-" + partes[1] + "-" + partes[2]
  return fecha

# Funcion para verificar la nomenclatura de las divisas
def check_nom(mensaje):
  nom = input(mensaje).upper()
  divisas = dictionary()

  if nom in divisas:
    return nom
  else:
    print("No esta disponible esa nomenclatura")
    print('Nomenclaturas disponibles:')

    for acro, nombre in divisas.items():
      print(f'{acro}: {nombre}')

    return check_nom(mensaje)


# Validar 0 y 1 para hacer los retornos al menu
def check_binario(mensaje):
  try:
    cant = int(input(mensaje))
    if cant == 1 or cant == 0:
      return cant
    else:
      check_binario(mensaje)
  except ValueError:
    print("Debes ingresar números")
