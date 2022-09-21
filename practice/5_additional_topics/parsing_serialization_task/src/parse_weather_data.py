import json
import os
import statistics as stats
from typing import Union


def parse_json_data(source_data_dir: str) -> dict[str, list[dict[str, float]]]:
    cities_weather_data: dict = {}
    for directory in os.listdir(source_data_dir):
        for json_file in os.listdir('/'.join([source_data_dir, directory])):
            city_name: str = directory
            json_file_path: str = '/'.join([
                source_data_dir, directory,
                json_file
            ])
            with open(json_file_path, 'r') as jf:
                weather_data: dict = json.load(jf)
                cities_weather_data[city_name] = []
                for hour_entry in weather_data['hourly']:
                    cities_weather_data[city_name].append({
                        'temp': hour_entry['temp'],
                        'wind_speed': hour_entry['wind_speed']
                    })
    return cities_weather_data


def calculate_cities_weather_stats(
    weather_data: dict[str, list[dict[str, float]]]
) -> dict[str, dict[str, float]]:

    weather_stats = {}
    for city, raw_city_data in weather_data.items():
        city_stats = {}
        parsed_city_temp = [hour_entry['temp'] for hour_entry in raw_city_data]
        parsed_city_wind_speed = [
            hour_entry['wind_speed'] for hour_entry in raw_city_data
        ]
        city_stats['mean_temp'] = round(stats.mean(parsed_city_temp), 2)
        city_stats['max_temp'] = round(max(parsed_city_temp), 2)
        city_stats['min_temp'] = round(min(parsed_city_temp), 2)
        city_stats['mean_wind_speed'] = round(
            stats.mean(parsed_city_wind_speed), 2)
        city_stats['max_wind_speed'] = round(max(parsed_city_wind_speed), 2)
        city_stats['min_wind_speed'] = round(min(parsed_city_wind_speed), 2)
        weather_stats[city] = city_stats
    return weather_stats


def calculate_country_weather_stats(
    cities_weather_stats: dict[str, dict[str, float]]
) -> dict[str, Union[float, str]]:

    country_weather_stats = {}
    parsed_cities_temps = [
        (city, x['mean_temp']) for city, x in cities_weather_stats.items()
    ]
    parsed_cities_wind_speeds = [(
            city,
            x['mean_wind_speed']
        ) for city, x in cities_weather_stats.items()
    ]
    country_weather_stats['mean_temp'] = round(stats.mean(
        [x[1] for x in parsed_cities_temps]
    ), 2)
    country_weather_stats['mean_wind_speed'] = round(stats.mean(
        [x[1] for x in parsed_cities_wind_speeds]
    ), 2)
    country_weather_stats['coldest_place'] = min(
        parsed_cities_temps,
        key=lambda x: x[1]
    )[0]
    country_weather_stats['warmest_place'] = max(
        parsed_cities_temps,
        key=lambda x: x[1]
    )[0]
    # country_weather_stats['least_windy_city'] = min(
    #     parsed_cities_wind_speeds,
    #     key=lambda x: x[1]
    # )
    country_weather_stats['windiest_place'] = max(
        parsed_cities_wind_speeds,
        key=lambda x: x[1]
    )[0]
    return country_weather_stats


def parse_weather_data(
    source_data_path: str
    ) -> tuple[
        dict[str, dict[str, float]],
        dict[str, Union[float, str]]
        ]:
    weather_data = parse_json_data(source_data_path)
    cities_weather_stats = calculate_cities_weather_stats(weather_data)
    return cities_weather_stats, calculate_country_weather_stats(
        cities_weather_stats
    )


def main():
    print(parse_weather_data('./source_data')[0])


if __name__ == '__main__':
    main()
