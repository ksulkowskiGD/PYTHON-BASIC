from lxml import etree
from typing import Union
from parse_weather_data import parse_weather_data


def generate_xml_file(
    cities_data: dict[str, dict[str, float]],
    country_data: dict[str, Union[float, str]],
    output_file_path: str
) -> None:
    root: etree._Element = etree.Element(
        'weather',
        country='Spain',
        date='2021-09-25'
        )
    summary: etree._Element = etree.Element('summary')
    for stat, value in country_data.items():
        summary.attrib[stat] = str(value)
    root.append(summary)
    cities: etree._Element = etree.Element('cities')
    for city_name, city_stats in cities_data.items():
        city_element: etree._Element = etree.SubElement(
            cities,
            city_name.replace(' ', '_')
        )
        for stat, value in city_stats.items():
            city_element.attrib[stat] = str(value)
    root.append(cities)
    root_str = etree.tostring(root, pretty_print=True).decode('utf-8')
    with open(output_file_path, 'w') as fh:
        fh.write(root_str)


def main():
    generate_xml_file(
        *parse_weather_data('./source_data'),
        './output/result.xml'
    )


if __name__ == '__main__':
    main()
