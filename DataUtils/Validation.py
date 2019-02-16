import os
import glob
import re
import requests
from collections import defaultdict
from xml.etree.ElementTree import ElementTree as Et
from xml.etree import ElementTree
from DataUtils import GithubFiles


def get_model_files(mod_path):
    models = set()
    for file in glob.glob(mod_path + '/Models/**/*.mwm', recursive=True):
        models.add(file)
    return models


def get_model_usage(mod_path):
    models = defaultdict(list)
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = Et(file=file)
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
        tree = ElementTree.fromstring(req.text)
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
    icons = set()
    for file in glob.glob(mod_path + '/Textures/GUI/Icons/**/*.*', recursive=True):
        icons.add(file)
    return icons


def get_icon_usage(mod_path):
    icons = defaultdict(list)
    for file in glob.glob(mod_path + '/Data/**/*.sbc', recursive=True):
        tree = Et(file=file)
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
        tree = ElementTree.fromstring(req.text)
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

        file = os.path.relpath(file, mod_path)
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
    files_formatted = [os.path.relpath(x, mod_path).lower() for x in files]
    if game_content_path:
        game_files = get_model_files(game_content_path)
        game_files_formatted = [os.path.relpath(x, game_content_path).lower() for x in game_files]
        files_formatted += game_files_formatted

    missing = []
    for file in uses.keys():
        if file not in files_formatted:
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
        file = os.path.relpath(file, mod_path)
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
    files_formatted = [os.path.relpath(x, mod_path).lower() for x in files]
    if game_content_path:
        game_files = get_icon_files(game_content_path)
        game_files_formatted = [os.path.relpath(x, game_content_path).lower() for x in game_files]
        files_formatted += game_files_formatted

    missing = []
    for file in uses.keys():
        if file not in files_formatted:
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
