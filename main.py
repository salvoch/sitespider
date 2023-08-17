#!/Users/msalvoch/Personal/sitespider/.venv/bin/python3
import sys
from strip_elements import PandocStripper, ImageReference
from pathlib import Path
from dataclasses import dataclass
from parse_config import parse_config_file
from make_directories import make_directories
from render_html import Renderer
DEFAULT_OUTPUT_DIRECTORY = 'build'


@dataclass
class PageObject:
    md_path: Path | None
    html_path: Path
    images: list[ImageReference]
    title: str


@dataclass(kw_only=True)
class MainIndex(PageObject):
    pass


@dataclass(kw_only=True)
class CategoryIndex(PageObject):
    category_name: str


@dataclass(kw_only=True)
class SiteNote(PageObject):
    category_name: str


def main(output_build_directory: str = DEFAULT_OUTPUT_DIRECTORY) -> None:
    '''Execute the application'''

    # Create config and root paths
    config_file = parse_config_file()
    build_dir = make_directories(config_file, output_build_directory)

    # Render html
    renderer = Renderer(config_file, build_dir)
    renderer.render_index()
    renderer.render_categories()
    renderer.render_category_index()


if __name__ == '__main__':
    main(*sys.argv[1:])
    # TODO - proper CLI argument parsing (--build_directory, -f, etc)
