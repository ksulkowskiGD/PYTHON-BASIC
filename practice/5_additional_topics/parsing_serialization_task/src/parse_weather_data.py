import json
import os
import statistics as stats


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


def calculate_weather_stats(weather_data: dict[str, list[dict[str, float]]]) -> dict[str, dict[str, float]]:
    weather_stats = {}
    for city, raw_city_data in weather_data.items():
        city_stats = {}
        parsed_city_temp = [hour_entry['temp'] for hour_entry in raw_city_data]
        parsed_city_wind_speed = [
            hour_entry['wind_speed'] for hour_entry in raw_city_data
        ]
        city_stats['mean_temp'] = stats.mean(parsed_city_temp)
        city_stats['max_temp'] = max(parsed_city_temp)
        city_stats['min_temp'] = min(parsed_city_temp)
        city_stats['mean_wind_speed'] = stats.mean(parsed_city_wind_speed)
        city_stats['max_wind_speed'] = max(parsed_city_wind_speed)
        city_stats['min_wind_speed'] = min(parsed_city_wind_speed)
        weather_stats[city] = city_stats
    return weather_stats


def main():
    weather_data = parse_json_data('./source_data')
    weather_stats = calculate_weather_stats(weather_data)
    print(weather_stats)


if __name__ == '__main__':
    main()
