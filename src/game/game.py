import json

from pathlib import Path
from glob import glob
from dataclasses import dataclass

from typing import Dict, List, Set, Tuple, Union, Any
from typing_extensions import TypedDict

Number = Union[float, int]
JsonPayoffMatrix = List[List[List[Number]]]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]

class GameDict(TypedDict):
    id: int 
    type: str 
    payoff_matrix: PayoffMatrix

@dataclass(frozen=True)
class Game:

    """
    Dataclass with all important information about a game.
    """

    id: int
    type: str
    symmetric: bool
    payoff_row: PayoffMatrix
    payoff_col: PayoffMatrix
    payoff_matrix: JsonPayoffMatrix


def nested_list_to_nested_tuple(lists: List) -> Tuple:

    """
    Given a nested list, it returns an equivalent nested tuple.
    """

    return tuple(
        nested_list_to_nested_tuple(lst) 
        if isinstance(lst, list) 
        else lst 
        for lst in lists
    )


def transpose_list_of_lists(lists: List) -> List:

    """
    Given a list of lists, it returns its transpose (still a list of lists).
    """

    return list(map(list, zip(*lists)))


class GameFactoryFromJson:
    def __invert_row_col_payoffs_order(self, transposed_row: JsonPayoffMatrix) -> None:
        
        """
        It inverts payoffs ordering.

        Example:
            Input:

                [
                    [[1,2], [2,3]],
                    [[3,4], [4,5]]
                ]
                 
            Output:
                
                [
                    [[2,1], [3,2]],
                    [[4,3], [5,4]]
                ]

        """

        for action_payoffs in transposed_row:
            for payoffs in action_payoffs:
                payoffs.reverse()


    def _convert_payoff_row_to_col(self, game_dict: Dict[Any, Any]) -> PayoffMatrix:

        """
        Given a payoff matrix, it constructs and returns a payoff 
        matrix with the col player as the row one.

        Example:
            Input:
                               Col
                            0      1                    
                        ( 
                Row  0    ((1,2), (3,4)),
                     1    ((5,6), (7,8))
                        )

            Output:
                               Row
                            0      1                    
                        ( 
                Col  0    ((2,1), (6,5)),
                     1    ((4,3), (8,7))
                        )
        """

        transposed_row: JsonPayoffMatrix = transpose_list_of_lists(game_dict["payoff_matrix"])

        self.__invert_row_col_payoffs_order(transposed_row)

        return nested_list_to_nested_tuple(transposed_row)


    def create_game(self, game_dict: GameDict):
        
        """
        It creates the game from data inside .json file.
        """

        payoff_row: PayoffMatrix = nested_list_to_nested_tuple(
            game_dict["payoff_matrix"]
        )

        payoff_col: PayoffMatrix = self._convert_payoff_row_to_col(game_dict)

        return Game(
            id = game_dict["id"],
            type = game_dict["type"],
            symmetric = (payoff_row == payoff_col),
            payoff_row = payoff_row,
            payoff_col = payoff_col,
            payoff_matrix = game_dict["payoff_matrix"]
        )


def create_game_class_instance_entire_folder(path_to_folder: Path, filenames_to_exclude: Set[str] = set()) -> List[Game]:
    
    json_filepaths = glob(str(path_to_folder / '*.json'))

    json_filepaths = [
        json_file 
        for json_file in json_filepaths
        if Path(json_file).name not in filenames_to_exclude
    ]

    game_factory_from_json: GameFactoryFromJson = GameFactoryFromJson()

    games: List[Game] = []
    for json_filepath in json_filepaths:
        with open(json_filepath, "r") as file:
            json_dict = json.load(file)
            game = game_factory_from_json.create_game(json_dict)
            games.append(game)
        
    return games