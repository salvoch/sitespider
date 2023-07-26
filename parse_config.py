'''
Parse the config.yaml file
'''
import yaml
from dataclasses import dataclass
from typing import TypeAlias, NewType

# Defined types
MarkdownFileName = NewType('MarkdownFileName', str)
CategoryName = NewType('CategoryName', str)
CategoryStructure: TypeAlias = dict[CategoryName, list[MarkdownFileName]]


# Defined data structure
@dataclass
class ConfigFile:
    '''Parsed config file'''
    index: MarkdownFileName
    categories: list[CategoryStructure]
    style: str

    def __post_init__(self) -> None:
        '''Runs after init, validates types match and format'''
        # NOTE - Cannot check instance of MarkdownFileName in isinstance()
        if not isinstance(self.index, str):
            raise TypeError("Config 'index' field"
                            " should be the name of a markdown file")

        if not isinstance(self.style, str):
            raise TypeError("Config 'style' field"
                            " should be a string denoting style option.")

        if not isinstance(self.categories, list):
            raise TypeError("Categories field is formed"
                            " incorrectly, should result in list.")


def parse_config_file(filename: str = "config.yaml") -> ConfigFile:
    '''Parse the yaml config file for a project'''

    with open(filename, 'r') as f:
        yaml_data = yaml.safe_load(f)

    # Load config file
    config_file = ConfigFile(
        index=MarkdownFileName(yaml_data['index']),
        categories=yaml_data['categories'],
        style=str(yaml_data['style'])
    )

    return config_file


if __name__ == '__main__':
    a = parse_config_file()
    print(a)
