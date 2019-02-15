import os
import glob
from xml.etree.ElementTree import ElementTree as Et
from xml.etree import ElementTree


def get_defs_of_type(mod_path, type):
    raw_type = type.replace('MyObjectBuilder_', '')
    defs = set()
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = Et(file=file)
        for definition in tree.findall('Definition'):
            if definition.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'].replace('MyObjectBuilder_', '') == raw_type:
                defs.add(definition)
    return defs


def get_def_ids_of_type(mod_path, type, subtype_only=False):
    raw_type = type.replace('MyObjectBuilder_', '')
    def_names = set()
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = Et(file=file)
        for definition in tree.findall('Definition'):
            if definition.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'].replace('MyObjectBuilder_', '') == raw_type:
                if subtype_only:
                    def_names.add(definition.find('Id').attrib['Subtype'])
                else:
                    def_names.add((definition.find('Id').attrib['Type'], definition.find('Id').attrib['Subtype']))
    return def_names


def list_cubeblocks(mod_path):
    return get_def_ids_of_type(mod_path, "MyObjectBuilder_BuildableBlockDefinition", subtype_only=True)



p = "C:\\Users\PC\AppData\Roaming\MedievalEngineers\Mods\RoM"
print(list_cubeblocks(p))

