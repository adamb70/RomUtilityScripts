import os
import glob
import re
import requests
from collections import defaultdict
from lxml import etree as ET
from ..DataUtils import GithubFiles


def get_model_files(mod_path):
    """ Returns a set of all model paths in /Models/ """
    models = set()
    for file in glob.glob(mod_path + '/Models/**/*.mwm', recursive=True):
        models.add(os.path.relpath(file, mod_path).lower())
    return models


def get_model_usage(mod_path):
    models = defaultdict(list)
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = ET.ElementTree(file=file)
        for definition in tree.findall('Definition'):
            for node in definition.getiterator():
                if node.text and ".mwm" in node.text.lower():
                    models[node.text.lower()].append((node.tag, definition.find('Id').attrib.get('Type', ''),
                                                      definition.find('Id').attrib.get('Subtype', ''), file))
                elif node.tag == "BuildProgressModels":
                    for constr_model in node:
                        models[constr_model.attrib['File'].lower()].append((node.tag, definition.find('Id')
                                        .attrib.get('Type', ''), definition.find('Id').attrib.get('Subtype', ''), file))
    return models


def get_model_usage_git(data_urls=None):
    if not data_urls:
        data_urls = GithubFiles.get_data_urls()
    models = defaultdict(list)
    for url in data_urls:
        req = requests.get(url)
        tree = ET.fromstring(req.text)
        for definition in tree.findall('Definition'):
            for node in definition.getiterator():
                if node.text and ".mwm" in node.text.lower():
                    models[node.text.lower()].append((node.tag, definition.find('Id').attrib.get('Type', ''),
                                                      definition.find('Id').attrib.get('Subtype', ''), url))
                elif node.tag == "BuildProgressModels":
                    for constr_model in node:
                        models[constr_model.attrib['File'].lower()].append((node.tag, definition.find('Id')
                                        .attrib.get('Type', ''), definition.find('Id').attrib.get('Subtype', ''), url))
    return models


def get_icon_files(mod_path):
    """ Returns a set of all texture paths in /GUI/Icons """
    icons = set()
    for file in glob.glob(mod_path + '/Textures/GUI/Icons/**/*.*', recursive=True):
        icons.add(os.path.relpath(file, mod_path).lower())
    return icons


def get_icon_usage(mod_path):
    """ Returns a set of all texture paths in /GUI/Icons """
    icons = defaultdict(list)
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = ET.ElementTree(file=file)
        for definition in tree.findall('Definition'):
            for node in definition.findall('Icon'):
                if node.text:
                    icons[node.text.lower()].append((node.tag, definition.find('Id').attrib.get('Type', ''),
                                                     definition.find('Id').attrib.get('Subtype', ''), file))
    return icons


def get_icon_usage_git(data_urls=None):
    icons = defaultdict(list)
    for url in data_urls:
        req = requests.get(url)
        tree = ET.fromstring(req.text)
        for definition in tree.findall('Definition'):
            for node in definition.findall('Icon'):
                if node.text:
                    icons[node.text.lower()].append((node.tag, definition.find('Id').attrib.get('Type', ''),
                                                     definition.find('Id').attrib.get('Subtype', ''), url))
    return icons


def find_unused_models(mod_path):
    files = get_model_files(mod_path)
    uses = get_model_usage(mod_path)
    missing = []
    for file in files:
        # Ignore LOD files
        pattern = re.compile(r'_LOD\d\.mwm')
        if re.search(pattern, file):
            continue

        if not uses[file.lower()]:
            missing.append(file)
    return missing


def find_unused_models_git(data_urls):
    files = GithubFiles.get_model_paths()
    uses = get_model_usage_git(data_urls)
    missing = []
    for file in files:
        # Ignore LOD files
        pattern = re.compile(r'_LOD\d\.mwm')
        if re.search(pattern, file):
            continue

        if not uses[file.lower()]:
            missing.append(file)
    return missing


def find_missing_models(mod_path, game_content_path=None):
    files = get_model_files(mod_path)
    uses = get_model_usage(mod_path)
    if game_content_path:
        game_files = get_model_files(game_content_path)
        files.update(game_files)

    missing = []
    for file in uses.keys():
        if file not in files:
            missing.append(file)
    return missing


def find_missing_models_git(data_urls):
    files = GithubFiles.get_model_paths()
    uses = get_model_usage_git(data_urls)
    files_formatted = [x.lower() for x in files]

    missing = []
    for file in uses.keys():
        if file not in files_formatted:
            missing.append(file)
    return missing


def find_unused_icons(mod_path):
    files = get_icon_files(mod_path)
    uses = get_icon_usage(mod_path)
    missing = []
    for file in files:
        if not uses[file.lower()]:
            missing.append(file)
    return missing


def find_unused_icons_git(data_urls):
    files = GithubFiles.get_icon_paths()
    uses = get_icon_usage_git(data_urls)
    missing = []
    for file in files:
        if not uses[file.lower()]:
            missing.append(file)
    return missing


def find_missing_icons(mod_path, game_content_path=None):
    files = get_icon_files(mod_path)
    uses = get_icon_usage(mod_path)
    if game_content_path:
        game_files = get_icon_files(game_content_path)
        files.update(game_files)

    missing = []
    for file in uses.keys():
        if file not in files:
            missing.append(file)
            return
    return missing


def find_missing_icons_git(data_urls):
    files = GithubFiles.get_icon_paths()
    uses = get_icon_usage_git(data_urls)
    files_formatted = [x.lower() for x in files]

    missing = []
    for file in uses.keys():
        if file not in files_formatted:
            missing.append(file)
            return
    return missing


def find_duplicated_icons(mod_path, game_content_path):
    mod_icons = get_icon_files(mod_path)
    game_icons = get_icon_files(game_content_path)
    return set.intersection(mod_icons, game_icons)


def find_duplicated_models(mod_path, game_content_path):
    mod_icons = get_model_files(mod_path)
    game_icons = get_model_files(game_content_path)
    return set.intersection(mod_icons, game_icons)

