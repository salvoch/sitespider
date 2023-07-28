'''
This module forms the output structure of the website, generates
the structure of the html, css, js, etc
'''

import pathlib
from parse_config import ConfigFile


def make_directories(config: ConfigFile, root: str = "build") -> pathlib.Path:
    '''Generate the directory structure, by default makes it in a
    /build directory where the script is running,
    if it already exists, skip it'''

    # start clean, delete existing build
    delete_directories(pathlib.Path(root))

    # Create directories
    pathlib.Path(root).mkdir()
    pathlib.Path(root+"/images").mkdir()
    pathlib.Path(root+"/scripts").mkdir()
    pathlib.Path(root+"/styles").mkdir()
    pathlib.Path(root+"/categories").mkdir()

    # Create sub category directories
    for category in config.categories:
        cat_name: str = list(category.keys())[0]
        pathlib.Path(root+"/categories/"+cat_name).mkdir()

    return pathlib.Path(root)


def delete_directories(path: pathlib.Path) -> None:
    '''Recursively delete directories,
    important to do since this can cause malformed websites'''

    if path.is_file():
        path.unlink()  # Delete file
    else:
        for child in path.iterdir():
            delete_directories(child)
        path.rmdir()  # Delete directory
