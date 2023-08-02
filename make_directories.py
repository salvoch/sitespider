'''
This module forms the output structure of the website, generates
the structure of the html, css, js, etc
'''

from pathlib import Path
from parse_config import ConfigFile


def make_directories(config: ConfigFile, build: str = "build") -> Path:
    '''Generate the directory structure, by default makes it in a
    /build directory where the script is running,
    if it already exists, skip it'''

    # Create Path object
    build_path = Path(build)

    # start clean, delete existing build
    delete_directories(build_path)

    # Create directories
    build_path.mkdir()
    (build_path / "images").mkdir()
    (build_path / "scripts").mkdir()
    (build_path / "styles").mkdir()
    (build_path / "categories").mkdir()

    # Create sub category directories
    for category in config.categories:
        cat_name: str = list(category.keys())[0]
        (build_path / 'categories' / cat_name).mkdir()

    return build_path


def delete_directories(path: Path) -> None:
    '''Recursively delete directories,
    important to do since this can cause malformed websites'''

    if path.is_file():
        path.unlink()  # Delete file
    else:
        for child in path.iterdir():
            delete_directories(child)
        path.rmdir()  # Delete directory
