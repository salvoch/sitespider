from main import MainIndex, CategoryIndex, SiteNote
import pandoc
from pandoc.types import Pandoc


def render_main_index(page: MainIndex) -> None:
    '''Render the main index page.'''
    ...


def render_category_index(page: CategoryIndex) -> None:
    '''Render the category index page.'''
    ...


def render_note(page: SiteNote) -> None:
    '''Render the site note page under a category'''
    ...


def __move_images(page: MainIndex | SiteNote) -> None:
    '''Look for images in a PageObject, move them to the build/image directory'''
    ...


def __update_image_ref(pandoc_file: Pandoc) -> Pandoc:
    '''Update the image references in a .md file to point to the new location under build/image'''
    # Figure out a good structure for this.
    ...
