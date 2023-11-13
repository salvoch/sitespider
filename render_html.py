from abc import ABC, abstractmethod
from pathlib import Path
import pandoc
from pandoc.types import Pandoc
from strip_elements import PandocStripper, ImageReference


class PageObject(ABC):
    '''Generic page class'''

    def __init__(self, md_path: Path, build_dir: Path) -> None:
        self.md_path: Path = md_path
        self.build_dir: Path = build_dir

        self.title: str = self.generate_title()
        self.html_path: Path = self.generate_html_path()

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
        ...

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
        ...

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
