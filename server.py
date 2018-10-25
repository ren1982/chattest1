from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)
port = int(os.environ["PORT"])
print(port)

@app.route('/', methods=['POST'])
def index():
  print(port)
  data = json.loads(request.get_data())

  # FETCH THE LOCATION, LATITUDE AND LONGITUDE
  loc = data['conversation']['memory']['location']['formatted']
  lat = str(data['conversation']['memory']['location']['lat'])
  lon = str(data['conversation']['memory']['location']['lng'])

  # FETCH WEATHER
  r = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&units=metric&APPID=6d3b7bcb7cc48d14f6d12d2633075a69")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': 'The weather in %s is %s. The current temperature is %f.' % (loc, r.json()['weather'][0]['description'], r.json()['main']['temp'])
    }]
  )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")
