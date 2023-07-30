import pandoc
from pathlib import Path
from parse_config import ConfigFile


class Renderer():
    '''Class that renders .md files to .html'''

    def __init__(self, config: ConfigFile, root: Path) -> None:
        self.config = config
        self.root = root

    def render_index(self) -> None:
        '''Render the main index file'''

        html_dest = self.root / 'index.html'
        convert_md_file_to_html(Path(self.config.index), html_dest)

    def render_categories(self) -> None:
        '''Render the files under each category'''

        # Render each post under each category
        for category in self.config.categories:
            for category_name, post_list in category.items():
                for post in post_list:
                    html_dest = self.root / 'categories' / category_name / post.stem / '.html'
                    convert_md_file_to_html(Path(post), html_dest)

    def render_category_index(self) -> None:
        '''Render the index.html files for each category'''

        pass


def convert_md_file_to_html(md_path: Path, html_destination: Path) -> None:
    '''Convert single .md file to HTML. Must provide Path objects'''

    # Check to make sure file exists
    if not md_path.exists():
        raise Exception  # TODO - create actual exception

    # Check to make sure .md file was passed
    if md_path.suffix != ".md":
        raise Exception  # TODO - create actual exception

    # Convert file to html
    with md_path.open() as file:
        read_file = file.read()
        pan_doc = pandoc.read(read_file, format="markdown")
        pandoc.write(pan_doc, html_destination, "html")
