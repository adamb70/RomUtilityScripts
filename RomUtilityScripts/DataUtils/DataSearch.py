import os
import glob
from collections import defaultdict
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


def get_def_ids_of_types(mod_path, types):
    raw_types = [t.replace('MyObjectBuilder_', '') for t in types]
    def_names = defaultdict(set)
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = Et(file=file)
        for definition in tree.findall('Definition'):
            if definition.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'].replace('MyObjectBuilder_', '') in raw_types:
                def_names[definition.find('Id').attrib['Type']].add(definition.find('Id').attrib['Subtype'])
    return def_names


def list_cubeblocks(mod_path):
    return get_def_ids_of_types(mod_path, ["BuildableBlockDefinition"])["Block"]
