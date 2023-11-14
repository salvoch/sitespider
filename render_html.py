from abc import ABC, abstractmethod
from pathlib import Path
import pandoc
from pandoc.types import Pandoc
from strip_elements import PandocStripper, ImageReference

# TODO -
    # Have to create two additional page types potentially
        # - Sub index (the page below the index, this has a list of categories and top 3 posts
        # - About page (thing on the left hand - can we make it optional?)
    # We have to pass a list of categories/posts to:
        # The sub index (the categories, and the latest 3 posts)
        # Category index (Just the posts in its own category)
    # Can we pass a list of objects to these?
    # Complete the three image functions
        # Locate images
        # Move images
        # Update refs to images


class PageObject(ABC):
    '''Generic page class'''

    def __init__(self, md_path: Path, build_dir: Path) -> None:

        # Exception checking
        # Check to make sure passed file was an .md file
        if md_path.suffix != ".md":
            raise Exception  # TODO - create actual exception

        # Passed data
        self.md_path: Path = md_path
        self.build_dir: Path = build_dir

        # Generated data
        self.title: str = self.generate_title()
        self.html_path: Path = self.generate_html_path()

        # Empty data
        self.images: list[ImageReference] = []
        self.pandoc_page: Pandoc | None = None

    @abstractmethod
    def generate_title(self) -> str:
        '''Generate title, strip it from the file, or use generic'''
        ...

    @abstractmethod
    def generate_html_path(self) -> Path:
        '''Generate the destination path '''
        ...

    @abstractmethod
    def render(self) -> None:
        '''Render the page, the result of this will be the final .html placed onto its destination'''
        ...

    def find_images(self) -> None:
        '''Find all images in an .md file, save them in self.images'''
        stripper = PandocStripper(self.md_path)
        self.images = stripper.strip_local_image_locations()

    def move_images(self, page: Pandoc) -> None:
        '''move images to the build directory'''
        ...

    def update_image_ref(self, page: Pandoc) -> Pandoc:
        '''Update the image references in a .md file to point to the new location under build/image
        update self.pandoc_page (or return it?)'''
        # Figure out a good structure for this.
        ...


class MainIndex(PageObject):
    '''Class for the main index page'''

    def __init__(self, md_path: Path, build_dir: Path) -> None:
        super().__init__(md_path, build_dir)

    def generate_title(self) -> str:
        stripper = PandocStripper(self.md_path)
        return stripper.strip_title()

    def generate_html_path(self) -> Path:
        return self.build_dir / "index.html"

    def render(self) -> None:
        # Convert file to html
        # TODO - should we make this a try?
        with self.md_path.open() as file:
            read_file = file.read()
            self.pandoc_page = pandoc.read(read_file, format="markdown")

            # Get list of images
            # Move images
            # Update image locations
            # Templetize

            pandoc.write(self.pandoc_page, self.html_path, "html")

    def __str__(self) -> str:
        return_str = f'''Page Type: MainIndex
        md_path = {self.md_path}
        build_dir = {self.build_dir}
        title = {self.title}
        html_path = {self.html_path}
        images = {self.images}
        pandoc_page = {self.pandoc_page}'''
        return return_str


class CategoryIndex(PageObject):
    '''Class for the category index pages'''

    def __init__(self, category_name: str, build_dir: Path) -> None:
        self.build_dir: Path = build_dir
        self.category_name = category_name

        self.title: str = self.generate_title()
        self.html_path: Path = self.generate_html_path()

        self.pandoc_page: Pandoc | None = None

    def generate_title(self) -> str:
        return self.category_name

    def generate_html_path(self) -> Path:
        return self.build_dir / self.category_name / "index.html"

    def render(self) -> None:
        ...
        # Generate sub-list of pages in category
        # Put in a template

    def __str__(self) -> str:
        return_str = f'''Page Type: CategoryIndex
        category_name = {self.category_name}
        build_dir = {self.build_dir}
        title = {self.title}
        html_path = {self.html_path}
        pandoc_page = {self.pandoc_page}'''
        return return_str


class SiteNote(PageObject):
    '''Class for the .md note files, each belongs to a category'''

    def __init__(self, md_path: Path, category_name: str, build_dir: Path) -> None:
        self.category_name = category_name
        super().__init__(md_path, build_dir)

    def generate_title(self) -> str:
        stripper = PandocStripper(self.md_path)
        return stripper.strip_title()

    def generate_html_path(self) -> Path:
        return self.build_dir / self.category_name / (self.md_path.stem+".html")

    def render(self) -> None:
        # Convert file to html
        # TODO - should we make this a try?
        with self.md_path.open() as file:
            read_file = file.read()
            self.pandoc_page = pandoc.read(read_file, format="markdown")

            # Get list of images
            # Move images
            # Update image locations
            # Generate header
            # Templetize

            pandoc.write(self.pandoc_page, self.html_path, "html")

    def __str__(self) -> str:
        return_str = f'''Page Type: SiteNote
        md_path = {self.md_path}
        category_name = {self.category_name}
        build_dir = {self.build_dir}
        title = {self.title}
        html_path = {self.html_path}
        images = {self.images}
        pandoc_page = {self.pandoc_page}'''
        return return_str


if __name__ == '__main__':
    index = MainIndex(Path('test.md'), Path('build'))
    print(index)
