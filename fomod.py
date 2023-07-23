import os.path
import xml.etree.ElementTree


def read_fomod(path: str):
    info = os.path.normcase(path + "fomod/info.xml")
    mod_info = get_mod_info(info)
    print(mod_info)

    module_config = os.path.normcase(path + "fomod/moduleconfig.xml")
    # TODO: make a module_config_reader...


def get_mod_info(info: str):
    tree = xml.etree.ElementTree.parse(info)
    root = tree.getroot()
    name = root.find("Name").text
    author = root.find("Author").text
    version = root.find("Version").text
    website = root.find("Website").text
    return [name, author, version, website]
