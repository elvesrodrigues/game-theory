import re

from os import walk
from pathlib import Path
from importlib import import_module

from typing import List, Optional, Set, Type
from types import ModuleType

from .player import Player


PATH_PLAYERS = Path("src/player/")


def _get_player_class_name(path_to_file: Path) -> str:

    """
        Given a .py file, returns its class' name.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    regex_pattern = re.compile(r"class\s*(?P<class_name>.+?)\s*\(Player\)")

    with path_to_file.open("r") as file:

        for line in file:
            regex_match = re.match(regex_pattern, line)

            if regex_match is not None:
                return regex_match.group("class_name")

        raise NameError(f"No class has been found in {path_to_file}.")


def import_class_from_from_file(
    filename: str, class_name: str, package: str
) -> Type:
    
    module: ModuleType = import_module(
        "." + filename.strip(".py"), package
    )
    class_: Type = getattr(module, class_name)

    return class_


def create_player_class_instance_from_file(
    path_to_file: Path, package: str
) -> Player:

    """
        Given a .py file, create an instance of its class.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filename: str = path_to_file.name
    class_name: str = _get_player_class_name(path_to_file)

    class_: Type[Player] = import_class_from_from_file(
        filename, class_name, package
    )
    return class_()


def _are_filenames_unique(filenames: List[str]):
    return len(filenames) == len(set(filenames))


def _get_filenames(path_to_folder: Path) -> List[Path]:

    (_, _, filenames) = next(walk(path_to_folder))

    if not _are_filenames_unique(filenames):
        raise RuntimeError("Some of the provided files have the same name.")

    filenames = [Path(file) for file in sorted(filenames)]

    return filenames


def create_player_class_instance_entire_folder(
    path_to_folder: Path = Path("src/player/"), 
    filenames_to_exclude: Set[Path] = {
        Path("__init__.py"),
        Path("player.py"),
        Path("dynamic_imports.py")
    },
    package: str = "src.player"
) -> List[Player]:

    """
        Given a folder, return a list with an instance of all
        of its file's classes. If there are any files which do 
        not have a class, add its name to "filenames_to_exclude".

        It is assumed that the classes inherit from Player, 
        i.e. the line with their declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filenames: Optional[List[Path]] = None

    if path_to_folder.is_dir():
        filenames = _get_filenames(path_to_folder)

    if filenames is not None:
        return [
            create_player_class_instance_from_file(path_to_folder / file, package) 
            for file in filenames
            if file not in filenames_to_exclude
        ]
        
    return []