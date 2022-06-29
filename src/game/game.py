import json

from pathlib import Path
from dataclasses import dataclass

from typing import List, Tuple, Union


Number = Union[float, int]
JsonPayoffMatrix = List[List[List[Number]]]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]


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

    def __init__(self, json_filepath: Path) -> None:

        """
        Given a filepath to a .json file, it constructs a Game.
        """

        with open(json_filepath, "r") as file:
            self.json_dict = json.load(file)


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


    def _convert_payoff_row_to_col(self) -> PayoffMatrix:

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

        transposed_row: JsonPayoffMatrix = transpose_list_of_lists(self.json_dict["payoff_matrix"])

        self.__invert_row_col_payoffs_order(transposed_row)

        return nested_list_to_nested_tuple(transposed_row)


    def create_game(self):
        
        """
        It creates the game from data inside .json file.
        """

        payoff_row: PayoffMatrix = nested_list_to_nested_tuple(
            self.json_dict["payoff_matrix"]
        )

        payoff_col: PayoffMatrix = self._convert_payoff_row_to_col()

        return Game(
            id = self.json_dict["id"],
            type = self.json_dict["type"],
            symmetric = (payoff_row == payoff_col),
            payoff_row = payoff_row,
            payoff_col = payoff_col
        )
   

if __name__ == '__main__':

    game = GameFactoryFromJson("src/game/game_test_asym.json").create_game() 
    print(game)

    game = GameFactoryFromJson("src/game/game_test_sym.json").create_game() 
    print(game)