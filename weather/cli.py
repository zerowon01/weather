import requests
import click
from typing import Any, Dict
import sys
import json
from importlib import metadata
import logging
import os
from dotenv import load_dotenv
# pulling this logger from external causes pipx:weather to fail
# from config import logger

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

def process_json_endpoint(url: str) -> Dict[str, Any] | None:
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None


def print_and_exit(message: str) -> None:
    logger.error(message)
    sys.exit(1)

# @click.version_option(pkg_resources.get_distribution("weather").version)
@click.version_option(metadata.version("weather"))

@click.command()
@click.option("--apikey", "-k")
@click.option("--fahrenheit", "-f", is_flag=True, default=False,
              required=False, help="Converts temperature to Fahrenheit")
@click.option("--json_format", "-j", is_flag=True, default=False,
              required=False, help="Ouputs the temperature as a json")
def cli(apikey:str, fahrenheit: bool, json_format: bool) -> None:
    """Easily get the curent temperature based on your IP address."""
    print("ENVar: ", os.environ.get("WEATHER_APIKEY"))
    try:
        lookup_ip = process_json_endpoint("https://api.ipify.org?format=json")
        if lookup_ip is None:
            print_and_exit("CouCould not retrieve your IP address")
        logger.info(f"My ip:  {lookup_ip['ip']}")
        geo = process_json_endpoint(
            f"https://geo.ipify.org/api/v2/country,city?apiKey={apikey}&ipAddress={lookup_ip['ip']}")
        if geo is None:
            print_and_exit("Could not get lat/lon!")
        weather = process_json_endpoint(
            f"https://api.open-meteo.com/v1/forecast?latitude={geo['location']['lat']}&longitude={geo['location']['lng']}&current_weather=true")
        if weather is None:
            print_and_exit("Could not get the weather")
        temp = weather["current_weather"]["temperature"]
        if fahrenheit:
            temp = temp * 1.8 + 32
        # Support outputing a human-friendly message or JSON
        if json_format:
            logger.info(json.dumps(
                {"temperature": temp, "unit": "F" if fahrenheit else "C"}))
        else:
            logger.info(
                f"The temperature in {geo['location']['city']} is {temp} {' F' if fahrenheit else ' C'  }")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli(auto_envvar_prefix="WEATHER")
