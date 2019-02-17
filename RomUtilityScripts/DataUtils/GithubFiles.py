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
