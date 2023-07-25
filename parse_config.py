'''
Parse the config.yaml file
'''
import yaml
from dataclasses import dataclass
from typing import TypeAlias

#Defined exceptions
#TODO - make these properly
class ConfigFileError(Exception):
    pass

#Defined types
#TODO - Look into making a proper data structure
MarkdownFileName:  TypeAlias = str
CategoryName:      TypeAlias = str
CategoryStructure: TypeAlias = dict[CategoryName, list[MarkdownFileName]]

#Defined data structures
@dataclass
class ConfigFile:
    '''Parsed config file'''
    index: MarkdownFileName
    categories: list[CategoryStructure]
    style: str

def parse_config_file(filename: str = "config.yaml") -> ConfigFile:
    '''Parse the yaml config file for a project'''
    
    with open(filename, 'r') as f:
        yaml_data = yaml.safe_load(f)

    try:
        config_file = ConfigFile(
            index = str(yaml_data['index']),
            categories = yaml_data['categories'], #TODO- type check this
            style = str(yaml_data['style'])
        )
    except KeyError as exc:
        raise ConfigFileError(exc) #TODO - Raise these correctly
    except Exception as exc:
        raise ConfigFileError(exc)

    return config_file

if __name__ == '__main__':
    a = parse_config_file()
    print(a)