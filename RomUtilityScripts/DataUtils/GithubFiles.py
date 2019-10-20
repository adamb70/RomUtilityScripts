from collections import defaultdict
from lxml import etree as ET
import requests
from github import Github
from ..RomUtilityScriptsBase import settings


def get_github_data_urls(dir="", limit_filetypes=None, filepaths_only=False):
    g = Github(settings.GITHUB_TOKEN)
    rom_repo = g.get_repo("adamb70/RoM")

    urls = set()
    contents = rom_repo.get_contents(dir)
    while len(contents) > 1:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(rom_repo.get_contents(file_content.path))
        else:
            if limit_filetypes and file_content.name.split('.')[-1] not in limit_filetypes:
                continue
            if filepaths_only:
                urls.add(file_content.path)
            else:
                urls.add(file_content.download_url)
    return urls


def get_data_urls():
    return get_github_data_urls("Data", limit_filetypes=['sbc'])

def get_model_paths():
    return get_github_data_urls("Models", filepaths_only=True)

def get_icon_paths():
    return get_github_data_urls("Textures/GUI/Icons", filepaths_only=True)


def get_items_by_types_git(types):
    raw_types = [t.replace('MyObjectBuilder_', '') for t in types]
    data_urls = get_data_urls()
    def_names = defaultdict(set)
    for url in data_urls:
        req = requests.get(url)
        tree = ET.fromstring(req.text)
        for definition in tree.findall('Definition'):
            if definition.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'].replace('MyObjectBuilder_', '') in raw_types:
                def_names[definition.find('Id').attrib['Type']].add(definition.find('Id').attrib['Subtype'])
    return def_names


def list_cubeblocks_git():
    return get_items_by_types_git(["BuildableBlockDefinition"])["Block"]
