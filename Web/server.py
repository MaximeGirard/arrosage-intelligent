import socketserver
import random
import json
import meteo as mt
import database as db

meteoReference = {
            "light_rain": 500,
            "rain": {"max":781},
            "clear": {"min":800}
        }

openWeatherMapUrl = "https://api.openweathermap.org/data/2.5/weather?"
openWeatherMapForecastUrl = "https://api.openweathermap.org/data/2.5/forecast?"
parameters = "lat=43.265283&lon=-0.206671&units=metric&appid="
apiKey = "f36081df884d8d7856c4b60e9aa8df65"

config = {
    'user':'root',
    'password':'max',
    'host':'localhost',
    'database':'ArrosageIntelligent'
}

weatherDatas = {
    "temperature1" : 0,
    "temperature2" : 0,
    "humidity"     : 0,
    "moisture"     : 0,
    "pressure"     : 0,
    "rain"         : 0,
    "nextRain"     : 0,
    "lastRain"     : 0,
    "lastWatering" : 0,
    "watered"      : 0
}

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        weatherDatas = json.loads(self.data.decode())

        # Sauvegarde des données dans la base de données
        result = mt.getContent(openWeatherMapForecastUrl + parameters + apiKey)
        nextRain = mt.nextRain(result, meteoReference)

        cnx = db.initConnexion(config)

        lastRain = db.getLastRain(cnx)
        lastWatering = db.getLastWatering(cnx)

        datas = {
            "temperature1" : weatherDatas["temperature1"],
            "temperature2" : weatherDatas["temperature2"],
            "humidity"     : weatherDatas["humidity"],
            "moisture"     : weatherDatas["moisture"],
            "pressure"     : weatherDatas["pressure"],
            "rain"         : weatherDatas["rain"],
            "nextRain"     : nextRain,
            "lastRain"     : lastRain,
            "lastWatering" : lastWatering,
            "watered"      : 0
        }

        db.addDataToDatabase(cnx, datas)

        cnx.commit()

        print("MESSAGE ENTRANT !")
        print(weatherDatas)
        # just send back the same data, but upper-cased
        self.request.sendall(b"[DATAS]" + self.server.server_address[0].encode() + b": Message recu\n")

HOST, PORT = "192.168.1.81", 8080

# Create the server, binding to localhost on port 8080
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()