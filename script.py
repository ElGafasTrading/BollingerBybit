from pybit.unified_trading import HTTP
import pandas as pd
import math
from decimal import Decimal, ROUND_DOWN, ROUND_FLOOR
import time

# Configuracion de la API
api_key = "APIKEY"
api_secret = "APISECRET"
symbol = "XRPUSDT"
timeframe = "5"  # Intervalo de tiempo 1,3,5,15,30,60,120,240,360,720,D,M,W
usdt = 10  # Cantidad de dolares para abrir posicion.

tp_porcent = 0.2  # Take profit porcentaje
sl_porcent = 0.4  # Stop loss porcentaje

client = HTTP(api_key=api_key, api_secret=api_secret, testnet=False)

# Datos de la moneda precio y pasos.
step = client.get_instruments_info(category="linear", symbol=symbol)
ticksize = float(step['result']['list'][0]['priceFilter']['tickSize'])
scala_precio = int(step['result']['list'][0]["priceScale"])
precision_step = float(step['result']['list'][0]["lotSizeFilter"]["qtyStep"])

def obtener_datos_historicos(symbol, interval, limite=200):
    """obtener datos de las velas"""
    response = client.get_kline(symbol=symbol, interval=interval, limite=limite)
    if "result" in response:
        data = pd.DataFrame(response['result']['list']).astype(float)
        data[0] = pd.to_datetime(data[0], unit='ms')
        data.set_index(0, inplace=True)
        data = data[::-1].reset_index(drop=True)
        return data
    else:
        raise Exception("Error al obtener datos historicos: " + str(response))


def calcular_bandas_bollinger(data, ventana=20, desviacion=2):
    data['MA'] = data[4].rolling(window=ventana).mean()
    data['UpperBand'] = data['MA'] + (data[4].rolling(window=ventana).std() * desviacion)
    data['LowerBand'] = data['MA'] - (data[4].rolling(window=ventana).std() * desviacion)
    return data.iloc[-1]

def qty_precision(qty, precision):
    qty = math.floor(qty / precision) * precision
    return qty

def qty_step(price):
    precision = Decimal(f"{10 ** scala_precio}")
    tickdec = Decimal(f"{ticksize}")
    precio_final = (Decimal(f"{price}") * precision) / precision
    precide = precio_final.quantize(Decimal(f"{1 / precision}"), rounding=ROUND_FLOOR)
    operaciondec = (precide / tickdec).quantize(Decimal('1'), rounding=ROUND_FLOOR) * tickdec
    result = float(operaciondec)

    return result

def crear_orden(symbol, side, order_type, qty):
    response = client.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType=order_type,
        qty=qty,
        timeInForce="GoodTillCancel"
    )
    print("Orden creada con exito:", response)

def establecer_stop_loss(symbol, sl):
    sl = qty_step(sl)

    order = client.set_trading_stop(
        category="linear",
        symbol=symbol,
        stopLoss=sl,
        slTriggerB="LastPrice",
        positionIdx=0
    )

    return order

def establecer_take_profit(symbol, tp, side, qty):
    price = qty_step(tp)

    order = client.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Limit",
        reduceOnly=True,
        qty=qty,
        price=price
    )

    return order

stop = False
tipo = ""
qty = 0
while True:
    try:
        posiciones = client.get_positions(category="linear", symbol=symbol)
        if float(posiciones['result']['list'][0]['size']) != 0:
            print("Hay una posicion abierta en " + symbol)
            if not stop:
                precio_de_entrada = float(posiciones['result']['list'][0]['avgPrice'])
                if posiciones['result']['list'][0]['side']  == 'Buy':
                    stop_loss_price = precio_de_entrada * (1 - sl_porcent / 100)
                    take_profit_price = precio_de_entrada * (1 + tp_porcent / 100)
                    establecer_stop_loss(symbol, stop_loss_price)
                    establecer_take_profit(symbol,take_profit_price, "Sell", qty)
                    print("Stop loss y Take profit activados")
                    stop = True
                else:
                    stop_loss_price = precio_de_entrada * (1 + sl_porcent / 100)
                    take_profit_price = precio_de_entrada * (1 - tp_porcent / 100)
                    establecer_stop_loss(symbol, stop_loss_price)
                    establecer_take_profit(symbol, take_profit_price, "Buy", qty)
                    print("Stop loss y Take profit activados")
                    stop = True
        else:
            stop = False
            qty = 0
            # Obtener datos historicos
            data = obtener_datos_historicos(symbol, timeframe)
            # Calcular bandas de bollinger
            data = calcular_bandas_bollinger(data)
            precio = client.get_tickers(category='linear', symbol=symbol)
            precio = float(precio['result']['list'][0]['lastPrice'])

            if precio >= data['UpperBand']:
                precision = precision_step
                qty = usdt / precio
                qty = qty_precision(qty, precision)
                if qty.is_integer():
                    qty = int(qty)
                print("Cantidad de monedas: " + str(qty))
                if tipo == "long" or tipo == "":
                    crear_orden(symbol,"Sell", "Market", qty)
                    tipo = "short"

            if precio <= data['LowerBand']:
                precision = precision_step
                qty = usdt / precio
                qty = qty_precision(qty, precision)
                if qty.is_integer():
                    qty = int(qty)
                print("Cantidad de monedas: " + str(qty))
                if tipo == "short" or tipo == "":
                    crear_orden(symbol,"Buy", "Market", qty)
                    tipo = "long"
    except Exception as e:
        print(f"Error en el bot: {e}")
        time.sleep(60)


