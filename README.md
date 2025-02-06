### Bot de bandas de Bollinger para Bybit

Este bot fue desarrollado para usar las bandas de bollinger en bybit, el bot abre operaciones simples con stop loss y take profit, lo puedes configurar como quieras. recuerda que debes usar las Apis de Bybit.

**Como usar el script**
- Descargar python [Aqui](https://www.python.org/ "Aqui")
- Descargar y modificar el Archivo .env, el archivo lo puedes modificar con sublime text, el cual puedes descargar [Aqui](https://www.sublimetext.com/ "Aqui")
- Agrega la API KEY y la API SECRET
```python
# Configuracion de la API
API_KEY=tu_api_key
API_SECRET=tu_api_secret
SYMBOL=XRPUSDT
TIMEFRAME=5
USDT=10
TP_PORCENT=0.2
SL_PORCENT=0.4
```
- Antes de ejecutar el Script deberas instalar la libreria de Python de Bybit pangas y python-dotenv
- `pip install pybit` 
- `pip install pandas` 
- `pip install python-dotenv`

- Una vez guardado el archivo debes ejecutarlo desde una terminal de windows o de tu sistema operativo que uses con el siguiente comando.
`python script.py`

**NOTA: Para que funcione bien no debes estar en modo Cobertura**
  

### Opción Docker

- Esta opción usando docker permite que el script se ejecute en cualquier sistema operativo sin importar la configuración del mismo.
- Ademas de que no necesitas instalar python ni las librerias necesarias. Docker lo hace todo por ti.
  
#### Instalación de Docker
- Descargar docker desktop desde https://www.docker.com/
##### Una vez Docker instalado
- Ejecutar el siguiente comando para hacer la instalacion del script y sus dependencias. Esta instruccion la debes ejecutar solo una vez, ya que la imagen se guardara en tu sistema.
```bash
docker build -t bot-bollinger-bybit .
```

- Una vez que la imagen este creada, puedes ejecutar el script con el siguiente comando.
```bash
docker run --rm -it --env-file .env bot-bollinger-bybit
```

- Si deseas modificar el archivo .env, puedes hacerlo con sublime text, el cual puedes descargar [Aqui](https://www.sublimetext.com/ "Aqui")














#### Contact
- Twitter: [https://twitter.com/ElGafasTrading](https://twitter.com/ElGafasTrading "https://twitter.com/ElGafasTrading")
- Instagram: [https://www.instagram.com/elgafastrading/](https://www.instagram.com/elgafastrading/ "https://www.instagram.com/elgafastrading/")
- Youtube: [https://www.youtube.com/@ElGafasTrading](https://www.youtube.com/@ElGafasTrading "https://www.youtube.com/@ElGafasTrading")
