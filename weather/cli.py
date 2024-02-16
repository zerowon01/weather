import requests
import logging


logger = logging.Logger("main-logger")

def process_json_endpoint(url:str):
   r = requests.get(url)
   if r.status_code == 200:
      return r.json()
   else:
       return None



def cli():
  lookup_ip = process_json_endpoint("https://api.ipify.org?format=json")
  if lookup_ip is None:
     logger.error("Couldn't retrieve IP address")
  logger.info("IP address is: ", lookup_ip["ip"])
  geo = process_json_endpoint(f"https://geo.ipify.org/api/v2/country,city?apiKey=at_xxxx&ipAddress={lookup_ip['ip']}")
  if geo is None:
     logger.error("Couldn't get LAT/LON for that IP")
  logger.info("Lat/lon: ", geo["location"]["lat"], "::", geo["location"]["lng"])
  weather = process_json_endpoint(f"https://api.open-meteo.com/v1/forecast?latitude={geo['location']['lat']}&longitude={geo['location']['lng']}&current_weather=true")
  if weather is None:
    logger.error("Couldn't get weather for that location.")
  return f"The temperature in {geo['location']['city']} is {weather['current_weather']['temperature']}"
  #print(r.json()["current_weather"]["temperature"])
  #else:
  # print("Open-Meteo is down!")

if __name__ == "__main__":
    cli()