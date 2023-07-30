#!/Users/msalvoch/Personal/sitespider/.venv/bin/python3
import sys
from parse_config import parse_config_file
from make_directories import make_directories
from render_html import Renderer
DEFAULT_OUTPUT_DIRECTORY = 'build'


def main(output_root_directory: str = DEFAULT_OUTPUT_DIRECTORY) -> None:
    '''Execute the application'''

    # Create config and root paths
    config_file = parse_config_file()
    root = make_directories(config_file, output_root_directory)

    # Render html
    renderer = Renderer(config_file, root)
    renderer.render_index()
    renderer.render_categories()
    renderer.render_category_index()


if __name__ == '__main__':
    main(*sys.argv[1:])
    # TODO - proper CLI argument parsing (--build_directory, -f, etc)
