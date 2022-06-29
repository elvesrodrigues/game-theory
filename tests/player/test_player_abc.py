import pytest
from src.player.player import Player, PayoffMatrixType, MatchHistoryType

from typing import Tuple, Dict, Union, Optional

PlayerFuncParam = Union[str, Tuple[str], Dict[str, Dict[str, Union[float, int]]]]


class EmptyClass (Player):
    
    
    def __init__(self) -> None:
        self.name = ""
        self.match_history = dict()


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrixType,
        adversary_id: str,
        match_history: Optional[MatchHistoryType],
        row_or_col: str
    ) -> int:
                        
        return ""


@pytest.fixture(scope="function")
def empty_class() -> EmptyClass:
    return EmptyClass()


@pytest.fixture(scope="function")
def empty_get_action_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "payoff_matrix": dict(),
        "match_history": None,
        "row_or_col": ""
    }


class TestEmpty:

    def test_all_is_empty(
        self, 
        empty_class: EmptyClass, 
        empty_get_action_params: Dict[str, PlayerFuncParam]
    ):
        
        assert empty_class.name == ""
        assert empty_class.match_history == dict()
        assert empty_class.get_action(**empty_get_action_params) == ""
