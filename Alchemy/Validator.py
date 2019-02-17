import os
from collections import defaultdict
import xml.etree.ElementTree as ET

from ..RomUtilityScriptsBase.Utils import indent


all_items = defaultdict(dict)

duplicates = defaultdict(int)


def get_objects(root, file, fix_duplicate_subtypes=False):
    for child in root:
        id = child.find('Id')
        if id is not None:
            try:
                if all_items[id.attrib['Type']][id.attrib['Subtype']]:
                    print('\nItem already exists!', all_items[id.attrib['Type']][id.attrib['Subtype']], id.attrib['Type'], id.attrib['Subtype'], file)

                    if child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == 'MyObjectBuilder_CraftingRecipeDefinition':
                        if fix_duplicate_subtypes:
                            duplicates[all_items[id.attrib['Type']][id.attrib['Subtype']]] += 1
                            new_subtype = id.attrib['Subtype'] + '_' + str(duplicates[all_items[id.attrib['Type']][id.attrib['Subtype']]] + 1)
                            id.attrib['Subtype'] = new_subtype
                            print('incrementing ID to', new_subtype)
                    else:
                        print('\t\t!! Type is ', child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'])

            except KeyError:
                #  If above failed, then the item doesn't already exist. This is good.
                all_items[id.attrib['Type']][id.attrib['Subtype']] = child
            except AttributeError:
                # Items has not type or subtype. This is bad.
                print('No type or subtype found!', child, file)

        else:
            get_objects(child, file)

    indent(root)
    ET.ElementTree(root).write(file, xml_declaration=True, method="xml")


def parse_sbc(sbc_file):
    tree = ET.parse(sbc_file)
    root = tree.getroot()
    get_objects(root, sbc_file)


def validate_crafting(all_items, no_duplicate_warnings=True):
    crafting_data = all_items['MyObjectBuilder_CraftingRecipeDefinition']
    if no_duplicate_warnings:
        warnings = set()
    else:
        warnings = []
    missing_prepreqs = set()
    missing_results = set()

    for subtype in crafting_data:
        definition = crafting_data[subtype]

        prereqs = definition.find('Prerequisites')
        results = definition.find('Results')
        categories = definition.findall('Category')

        if prereqs is not None:
            for item in list(prereqs):
                try:
                    all_items[item.attrib['Type']][item.attrib['Subtype']]
                except KeyError:
                    missing_prepreqs.add((item.attrib['Type'], item.attrib['Subtype']))
                    if no_duplicate_warnings:
                        warnings.add('<{}: {}> Prereq definition does not exist!!!'.format(item.attrib['Type'], item.attrib['Subtype']))
                    else:
                        warnings.append('<{}: {}> Prereq definition does not exist!!! (from <{}: {}>)'.format(item.attrib['Type'], item.attrib['Subtype'], definition.find('Id').attrib['Type'], definition.find('Id').attrib['Subtype']))
        else:
            print('No prereqs!', subtype)

        if results is not None:
            for item in list(results):
                try:
                    all_items[item.attrib['Type']][item.attrib['Subtype']]
                except KeyError:
                    missing_results.add((item.attrib['Type'], item.attrib['Subtype']))
                    if no_duplicate_warnings:
                        warnings.add('<{}: {}> Result definition does not exist!!!'.format(item.attrib['Type'], item.attrib['Subtype']))
                    else:
                        warnings.append('<{}: {}> Result definition does not exist!!! (from <{}: {}>)'.format(item.attrib['Type'], item.attrib['Subtype'], definition.find('Id').attrib['Type'], definition.find('Id').attrib['Subtype']))
        else:
            print('No results!', subtype)

        if not categories:
            print('No categories!', subtype)

    for w in warnings:
        print(w)

    print(missing_prepreqs)
    print(missing_results)


output_files = []
for root, dirs, files in os.walk('Output'):
    for file in files:
        if file.endswith('.sbc'):
            output_files.append(os.path.join('Output', file))


for file in output_files:
    parse_sbc(file)

validate_crafting(all_items)


