import json
import os


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


def main():
    weather_data = parse_json_data('./source_data')
    print(weather_data)


if __name__ == '__main__':
    main()
