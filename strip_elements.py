import pandoc
import pandoc.types
from pathlib import Path
from typing import TypeAlias
from dataclasses import dataclass

PandocFileType: TypeAlias = pandoc.types.Pandoc


@dataclass
class ImageReference:
    inline_text: str
    md_target: str


def pandify_file(file_path: Path) -> PandocFileType:
    '''Given a Path object to a markdown file, return the file converted into a Pandoc object'''

    # TODO - This is reused from render_html.convert_md_file_to_html, how to avoid?
    # Check to make sure file exists
    if not file_path.exists():
        raise Exception  # TODO - create actual exception

    # Check to make sure .md file was passed
    if file_path.suffix != ".md":
        raise Exception  # TODO - create actual exception

    with file_path.open() as file:
        read_file = file.read()
        pan_doc = pandoc.read(read_file, format="markdown")

    return pan_doc


def strip_title(pandoc_file: PandocFileType) -> str:
    '''Return the first H1 header as a string, can safely be assumed this is the title'''

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

    print("No title (aka an H1 (#)) element found in file ")  # TODO - do this in a logger.warning()
    return ""


def strip_local_image_locations(pandoc_file: PandocFileType) -> list[ImageReference]:
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
                    md_target = sub_element[2][0]
                    image_list.append(ImageReference(
                        inline_text=inline_text,
                        md_target=md_target))

    # Remove images from the web, since these will be unused
    url_check = lambda a: a[0:8].lower() == "https://" or a[0:7].lower() == "http://"
    return [x for x in image_list if not url_check(x.md_target)]


if __name__ == '__main__':
    pan_obj = pandify_file(Path('test.md'))
    print(strip_title(pan_obj))
    print(strip_local_image_locations(pan_obj))
