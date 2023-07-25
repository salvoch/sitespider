#!/Users/msalvoch/Personal/sitespider/.venv/bin/python3
import pandoc
import os
import pathlib
import sys
default_output_directory = 'build'

def convert_to_html(file_name: str) -> None:
    '''Convert single .md file to HTML.'''

    #Check to make sure .md file was passed
    pathlib.Path(file_name).suffix
    if pathlib.Path(file_name).suffix != ".md":
        raise Exception #TODO - create actual exception

    #Convert to html
    with open(file_name, 'r') as file:
        read_file = file.read()
        pan_doc = pandoc.read(read_file, format="markdown")
        file_path = default_output_directory+"/"+pathlib.Path(file_name).stem+".html" #TODO - check pathlib, proper path between OSs, create proper paths
        #TODO - make it work for nested directories
        pandoc.write(pan_doc, file_path, "html")

def convert_all_md(file_name: str|None = None) -> None:
    '''Convert all .md to HTML, optional file for converting just one'''

    #Check if a single filename was provided
    #TODO - make it more elegant?
    if file_name:
        file_list = [file_name]
    else:
        file_list = os.listdir()

    #Iterate for all .md files
    for file_name in file_list:
        if pathlib.Path(file_name).suffix == ".md":
            convert_to_html(file_name)

def main(file_name: str|None = None, directory_name: str|None = None) -> None:

    #Check if user passed directory_name to override global
    if directory_name:
        global default_output_directory
        default_output_directory = directory_name

    if not os.path.exists(default_output_directory):
        os.mkdir(default_output_directory)

    convert_all_md(file_name)


if __name__ == '__main__':
    main(*sys.argv[1:])
    #TODO - proper CLI argument parsing (--build_directory, -f, etc)