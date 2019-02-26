import csv
import xml.etree.ElementTree as ET


def csv_from_sbc(sbc_file):
    sbc = ET.ElementTree(file=sbc_file)
    root = sbc.find('Definition')

    for group in root.findall('ItemGroup'):
        group_name = group.attrib['Name']

        with open(f'./Output/{group_name}.csv', 'w', newline='') as csv_file:
            headers = ['Biomes', 'Materials', 'Slope Min', 'Slope Max', 'Height Min', 'Height Max', 'Type', 'Subtype',
                       'Density', 'MaxRoll', 'Latitude min', 'Latitude Max', 'Longitude Min', 'Longitude Max']
            writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
            writer.writeheader()

            for mapping in group.findall('Mapping'):
                biomes = [b.text for b in mapping.findall('Biome')]
                materials = [b.text for b in mapping.findall('Material')]
                slope = mapping.find('Slope')
                height = mapping.find('Height')
                lat = mapping.find('Latitude')
                long = mapping.find('Longitude')

                if slope is None:
                    slope = ET.Element('dummy')
                if height is None:
                    height = ET.Element('dummy')
                if lat is None:
                    lat = ET.Element('dummy')
                if long is None:
                    long = ET.Element('dummy')

                for item in mapping.findall('Item'):
                    ls = [','.join(biomes), ','.join(materials), slope.attrib.get('Min', ''),
                          slope.attrib.get('Max', ''),
                          height.attrib.get('Min', ''), height.attrib.get('Max', ''),

                          item.attrib['Type'], item.attrib['Subtype'], item.attrib.get('Density', ''),
                          item.attrib.get('Offset', ''), item.attrib.get('MaxRoll', ''),

                          lat.attrib.get('Min', ''), lat.attrib.get('Max', ''),
                          long.attrib.get('Min', ''), long.attrib.get('Max', '')]

                    writer.writerow(dict(zip(headers, ls)))
