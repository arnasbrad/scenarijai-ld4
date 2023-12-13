#!/usr/bin/python3

import requests
import sys


def fetch_current_weather(city_name):
    """
    Fetches the current weather for a given city.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: Temperature and last updated time if successful, or (None, None) if not.
    """
    api_key = "2d351b25a5ec46fab0694510221411"
    weather_api_url = "http://api.weatherapi.com/v1/current.json"

    params = {"key": api_key, "q": city_name}

    try:
        response = requests.get(weather_api_url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        weather_data = response.json()
        temperature_celsius = weather_data["current"]["temp_c"]
        last_updated_time = weather_data["current"]["last_updated"]
        return temperature_celsius, last_updated_time
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <city_name>")
        sys.exit(1)

    city_name = sys.argv[1]
    temperature, last_updated_time = fetch_current_weather(city_name)

    if temperature is not None:
        print(
            f"Current temperature in {city_name} is {temperature}°C. Last updated: {last_updated_time}."
        )
    else:
        print("Failed to retrieve weather data.")


if __name__ == "__main__":
    main()
