#!/Users/msalvoch/Personal/sitespider/.venv/bin/python3
import sys
from pathlib import Path
from parse_config import parse_config_file
from make_directories import make_directories
from render_html import MainIndex, CategoryIndex, SiteNote
DEFAULT_OUTPUT_DIRECTORY = 'build'


def main(output_build_directory: str = DEFAULT_OUTPUT_DIRECTORY) -> None:
    '''Execute the application'''

    # Create config and root paths
    config_file = parse_config_file()
    build_dir = make_directories(config_file, output_build_directory)

    # Generate SiteNotes Objects
    # -- Main Index
    index: MainIndex = MainIndex(md_path=Path(config_file.index),
                                 build_dir=build_dir)

    # -- Category Indices
    categories: list[CategoryIndex] = []
    for category_dict in config_file.categories:
        for category_title in category_dict.keys():
            categories.append(
                CategoryIndex(category_name=category_title,
                              build_dir=build_dir))

    # -- Site Note Objects
    site_notes: list[SiteNote] = []
    for category_dict in config_file.categories:
        for category_title, notes in category_dict.items():
            for note in notes:
                note_path = Path(note)
                site_notes.append(
                    SiteNote(
                        md_path=note_path,
                        category_name=category_title,
                        build_dir=build_dir
                    )
                )

    # Render pages
    index.render()
    for category in categories:
        category.render()
    for page in site_notes:
        page.render()

    # PRITNS - # NOTE - Remove
    print(index)
    for category in categories:
        print(category)
    for page in site_notes:
        print(page)


if __name__ == '__main__':
    main(*sys.argv[1:])
    # TODO - proper CLI argument parsing (--build_directory, -f, etc)
