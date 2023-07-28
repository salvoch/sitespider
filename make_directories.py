'''
This module forms the output structure of the website, generates
the structure of the html, css, js, etc
'''

from pathlib import Path
from parse_config import ConfigFile


def make_directories(config: ConfigFile, root: str = "build") -> Path:
    '''Generate the directory structure, by default makes it in a
    /build directory where the script is running,
    if it already exists, skip it'''

    # start clean, delete existing build
    delete_directories(Path(root))

    # Create directories
    Path(root).mkdir()
    Path(root+"/images").mkdir()
    Path(root+"/scripts").mkdir()
    Path(root+"/styles").mkdir()
    Path(root+"/categories").mkdir()

    # Create sub category directories
    for category in config.categories:
        cat_name: str = list(category.keys())[0]
        Path(root+"/categories/"+cat_name).mkdir()

    return Path(root)


def delete_directories(path: Path) -> None:
    '''Recursively delete directories,
    important to do since this can cause malformed websites'''

    if path.is_file():
        path.unlink()  # Delete file
    else:
        for child in path.iterdir():
            delete_directories(child)
        path.rmdir()  # Delete directory
