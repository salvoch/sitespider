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

    # Create Path object
    root_path = Path(root)

    # start clean, delete existing build
    delete_directories(Path(root))

    # Create directories
    root_path.mkdir()
    (root_path / "images").mkdir()
    (root_path / "scripts").mkdir()
    (root_path / "styles").mkdir()
    (root_path / "categories").mkdir()

    # Create sub category directories
    for category in config.categories:
        cat_name: str = list(category.keys())[0]
        (root_path / 'categories' / cat_name).mkdir()

    return root_path


def delete_directories(path: Path) -> None:
    '''Recursively delete directories,
    important to do since this can cause malformed websites'''

    if path.is_file():
        path.unlink()  # Delete file
    else:
        for child in path.iterdir():
            delete_directories(child)
        path.rmdir()  # Delete directory
