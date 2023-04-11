def obtenerCotizaciones(tipo, desde, hasta, invertir = False):
    import requests

    tipos = {
        "CCL" : "dolarrava/cl/grafico",
        "MEP" : "dolarrava/mep/grafico",
        "BLUE" : "dolar/informal/historico-general"
    }

    response = requests.get('https://mercados.ambito.com/' + tipos[tipo] + '/' + desde + '/' + hasta, headers = { 'Accept' : 'application/json' })
    data = response.json()
    data.pop(0)

    if invertir == True:
        data.reverse()

    return data

##############################
##### ▲ AREA FUNCIONAL ▲ #####
##############################

##############################
##### ▼ AREA PRINCIPAL ▼ #####
##############################

import csv
cabecera = ['fecha', "ccl", "mep", "informal"]

usdCCL = obtenerCotizaciones("CCL", "2010-01-01", "2023-04-11")
usdMEP = obtenerCotizaciones("MEP", "2010-01-01", "2023-04-11")
usdBlue = obtenerCotizaciones("BLUE", "2010-01-01", "2023-04-11", True)

cotizaciones = [ *usdCCL ]

for cotizacion in cotizaciones:

    fecha = cotizacion[0]

    for mep in usdMEP:
        if mep[0] == fecha and len(cotizacion) < 3: # ◀ (1) Evita duplicados por fecha (*)

            cotizacion.append( mep[1] )

    if len(cotizacion) < 3: # ◀ (2) Asigna 0 en caso de no haber cotizacion en la fecha
        cotizacion.append( 0 )

    for blue in usdBlue:
        if blue[0] == fecha and len(cotizacion) < 4: # ◀ (1)

            valor = blue[1].replace(',', '.')

            cotizacion.append( float(valor) )

    if len(cotizacion) < 4: # ◀ (2)
        cotizacion.append( 0 )


with open('historical_ARS_USD_price.csv', 'w', encoding='UTF8') as file:
    writer = csv.writer(file, delimiter = ',')

    writer.writerow(cabecera)

    for cotizacion in cotizaciones:
        writer.writerow(cotizacion)
