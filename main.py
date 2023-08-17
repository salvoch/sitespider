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

    # Generate SiteNotes Objects
    # -- Main Index
    index_md_path = Path(config_file.index)
    index_stripper = PandocStripper(index_md_path)
    html_path = build_dir / "index.html"
    index: MainIndex = MainIndex(md_path=index_md_path,
                                 html_path=html_path,
                                 images=index_stripper.strip_local_image_locations(),
                                 title=index_stripper.strip_title()
                                 )

    # -- Category Indices
    categories: list[CategoryIndex] = []
    for category_dict in config_file.categories:
        for category_title in category_dict.keys():
            html_path = build_dir / category_title / "index.html"
            categories.append(
                CategoryIndex(
                    md_path=None,
                    html_path=html_path,
                    images=[],
                    title=category_title,
                    category_name=category_title
                )
            )

    # -- Site Note Objects
    site_notes: list[SiteNote] = []
    for category_dict in config_file.categories:
        for category_title, notes in category_dict.items():
            for note in notes:
                note_path = Path(note)
                note_stripper = PandocStripper(note_path)
                html_path = build_dir / category_title / (Path(note).stem+".html")
                site_notes.append(
                    SiteNote(
                        md_path=note_path,
                        html_path=html_path,
                        images=note_stripper.strip_local_image_locations(),
                        title=note_stripper.strip_title(),
                        category_name=category_title
                    )
                )

    # TEST PRINT RM
    print(f'index = {index}')
    print(f'categories = {categories}')
    print(f'site notes = {site_notes}')

    # Render html
    renderer = Renderer(config_file, build_dir)
    renderer.render_index()
    renderer.render_categories()
    renderer.render_category_index()


if __name__ == '__main__':
    main(*sys.argv[1:])
    # TODO - proper CLI argument parsing (--build_directory, -f, etc)
