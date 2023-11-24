import pandoc
import pandoc.types
import copy
from pathlib import Path
from typing import TypeAlias
from dataclasses import dataclass

PandocFileType: TypeAlias = pandoc.types.Pandoc


@dataclass
class ImageReference:
    inline_text: str
    attributes: list[str]
    image_path: Path


def pandify_md_path(file_path: Path) -> pandoc.types.Pandoc:
    '''Given a Path object to a markdown file, return the file converted into a Pandoc object, this
    function includes error handling for non-existent files, or files that are not .md'''

    # TODO - This is reused from render_html.convert_md_file_to_html, how to avoid?
    # Check to make sure file exists
    if not file_path.exists():
        raise Exception  # TODO - create actual exception

    # Check to make sure .md file was passed
    if file_path.suffix != ".md":
        raise Exception  # TODO - create actual exception

    with file_path.open() as file:
        read_file = file.read()
        pandoc_file = pandoc.read(read_file, format="markdown")

    return pandoc_file


def strip_title(pandoc_file: pandoc.types.Pandoc) -> str:
    '''Given a pandoc file, return the first H1 header as a string, can safely be assumed this is the title'''

    if len(pandoc_file) < 2:
        print("Empty .md file, no title to strip")  # TODO - do this in a logger.warning()
        return ""

    # Iterate through each element, find a #H1 header
    for element in pandoc_file[1]:
        if isinstance(element, pandoc.types.Header):
            if element[0] == 1:
                # Remove the preceding "# ", and strip the \n, \r, and \t's.
                # Also, preserve any additional # and \ found within the sentence
                pan_string = pandoc.write(element, format="markdown")
                return "# ".join(pan_string.strip().split('# ')[1:]).replace("\\", "")

    print(f"No title (aka an H1 (#)) element found in file {pandoc_file.stem}")  # TODO - do this in a logger.warning()
    # TODO - Also, specify which file!
    return ""


def strip_local_image_locations(pandoc_file: pandoc.types.Pandoc) -> list[ImageReference]:
    '''Find all local images (that do not contain a url) in a file and return a list of their locations
    This will be useful when converting old references to the new file structure reference

    This will not be used for converting images themselves to HTML, pandoc does this. However, this will
    be used to copy the existing images to their expected location'''

    if len(pandoc_file) < 2:
        print("Empty .md file, no images to strip")  # TODO - do this in a logger.warning()
        return []

    # Find all paragraphs first, images are only inside paragraphs, not standalone
    # Then, iterate through each element inside each paragraph, looking for images
    image_list = []
    for element in pandoc_file[1]:
        if isinstance(element, pandoc.types.Para):
            for sub_element in element[0]:
                if isinstance(sub_element, pandoc.types.Image):
                    inline_text = sub_element[1][0].__dict__['_args'][0]
                    image_path = Path(sub_element[2][0])
                    img_attributes: list[str] = []
                    image_list.append(ImageReference(
                        inline_text=inline_text,
                        attributes=img_attributes,
                        image_path=image_path))

    # Remove images from the web, since these will be unused
    url_check = lambda a: a[0:8].lower() == "https://" or a[0:7].lower() == "http://"
    return [x for x in image_list if not url_check(str(x.image_path))]


def extract_image_attributes(images: list[ImageReference]) -> list[ImageReference]:
    '''Pull out the special attributes that an .md image could have, and add them to the attributes list.
    change the image_path to not have the attrubute. Attributes are denoted by # and ! after file extension'''

    updated_images = []
    for image_reference in images:
        image = copy.deepcopy(image_reference)
        if '#' in image.image_path.suffix:
            extension = image.image_path.suffix.split('#')[0]
            attribute = image.image_path.suffix.split('#')[1]
            image.image_path = image.image_path.with_suffix(extension)
            image.attributes.append(attribute)
        elif '?' in image.image_path.suffix:
            extension = image.image_path.suffix.split('?')[0]
            attribute = image.image_path.suffix.split('?')[1]
            image.image_path = image.image_path.with_suffix(extension)
            image.attributes.append(attribute)

        updated_images.append(image)

    return updated_images


if __name__ == '__main__':
    pan_obj = pandify_md_path(Path('test.md'))
    print("title")
    print(strip_title(pan_obj))
    images = strip_local_image_locations(pan_obj)
    print("images before attributes")
    print(images)
    images = extract_image_attributes(images)
    print("images after attributes")
    print(images)
